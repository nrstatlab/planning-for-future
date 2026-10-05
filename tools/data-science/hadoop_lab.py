"""A small Hadoop cluster on one machine, for the Course 12 B labs, and a way to run their scripts.

    with cluster() as c:            # HDFS (a NameNode and three DataNodes) and YARN, in a temp dir
        c.run_script("02_hdfs_commands.sh")

The cluster is "pseudo-distributed", as experiment 1 sets one up, with two differences, each
for a reason the lab page gives:
  * four DataNodes, the first with the default settings and the others on ports of their own,
    so replication 3 means something and experiment 5 can kill one and see its blocks copied
    to the fourth; the first is the one `hdfs --daemon start datanode` starts; and
  * the daemons are started one by one with `hdfs --daemon start` and `yarn --daemon start`.
    start-dfs.sh does exactly that on each host it lists, over ssh; there is one host here.
A DataNode is declared dead after 60 s instead of the default 630 s (experiment 5 waits for it).

Tools come from tools/data-science/setup_hadoop.sh, in $HADOOP_PREFIX (default /tmp/hadoop), and
run on Java 8, which every tool in the course supports.

run_script() runs a lab's shell script as a student types it: each command is printed, after
"$ ", before it runs, and the comments are left out (they are on the lab page, in the file).
"""
import contextlib
import os
import pathlib
import re
import shutil
import socket
import subprocess
import tempfile
import time

PREFIX = pathlib.Path(os.environ.get("HADOOP_PREFIX", "/tmp/hadoop"))
JAVA8 = os.environ.get("JAVA8_HOME", "/usr/lib/jvm/java-8-openjdk-amd64")
HADOOP = PREFIX / "hadoop-3.3.6"
TOOLS = {"pig": "pig-0.17.0", "hive": "apache-hive-3.1.3-bin", "hbase": "hbase-2.5.10-hadoop3",
         "zookeeper": "apache-zookeeper-3.8.4-bin", "sqoop": "sqoop-1.4.7.bin__hadoop-2.6.0",
         "flume": "apache-flume-1.11.0-bin"}
DATANODES = 4                  # so a block can be re-replicated when one dies
RECHECK_MS = 15000             # dead after 2 x 15 s + 10 x 3 s heartbeats = 60 s


def site(props):
    rows = "".join(f"  <property><name>{k}</name><value>{v}</value></property>\n" for k, v in props.items())
    return f'<?xml version="1.0"?>\n<configuration>\n{rows}</configuration>\n'


def free(port):
    with socket.socket() as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def env(base, conf, extra=None):
    """The environment every command sees: Java 8, the tools on PATH, and this cluster's conf."""
    e = dict(os.environ)
    e.pop("JAVA_TOOL_OPTIONS", None)          # the proxy settings print a line on every JVM start
    e.update({
        "JAVA_HOME": JAVA8, "HADOOP_HOME": str(HADOOP), "HADOOP_CONF_DIR": str(conf),
        "HADOOP_MAPRED_HOME": str(HADOOP), "HADOOP_LOG_DIR": str(base / "logs"),
        "HADOOP_PID_DIR": str(base / "pids"),
        "HADOOP_OPTS": "-Djava.net.preferIPv4Stack=true",
        # Hadoop 3 refuses to start a daemon as root unless told which user runs it
        **{f"{d}_USER": "root" for d in ("HDFS_NAMENODE", "HDFS_DATANODE", "HDFS_SECONDARYNAMENODE",
                                         "YARN_RESOURCEMANAGER", "YARN_NODEMANAGER")},
    })
    path = [str(HADOOP / "bin"), str(HADOOP / "sbin"), f"{JAVA8}/bin"]
    for name, d in TOOLS.items():
        home = PREFIX / d
        e[f"{name.upper()}_HOME"] = str(home)
        path.append(str(home / "bin"))
    e["PATH"] = ":".join(path + [e.get("PATH", "")])
    e.update(extra or {})
    return e


class Cluster:
    def __init__(self, base):
        self.base = base
        self.conf = base / "conf"
        self.env = env(base, self.conf)
        self.datanodes = {}

    def sh(self, cmd, conf=None, check=True, extra=None, **kw):
        e = dict(self.env, HADOOP_CONF_DIR=str(conf or self.conf), **(extra or {}))
        r = subprocess.run(cmd, shell=isinstance(cmd, str), env=e, cwd=kw.pop("cwd", self.base),
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, **kw)
        if check and r.returncode:
            raise RuntimeError(f"{cmd}: exit {r.returncode}\n{r.stdout[-3000:]}")
        return r.stdout

    def write_conf(self):
        hdfs = {"dfs.replication": 3, "dfs.namenode.name.dir": f"file://{self.base}/nn",
                "dfs.namenode.heartbeat.recheck-interval": RECHECK_MS,
                "dfs.permissions.enabled": "false"}
        core = {"fs.defaultFS": "hdfs://localhost:9000", "hadoop.tmp.dir": str(self.base / "tmp"),
                "fs.trash.interval": 1440}
        mapred = {"mapreduce.framework.name": "yarn",
                  **{k: f"HADOOP_MAPRED_HOME={HADOOP}" for k in (
                      "yarn.app.mapreduce.am.env", "mapreduce.map.env", "mapreduce.reduce.env")},
                  "mapreduce.map.memory.mb": 512, "mapreduce.reduce.memory.mb": 512,
                  "yarn.app.mapreduce.am.resource.mb": 512}
        yarn = {"yarn.nodemanager.aux-services": "mapreduce_shuffle",
                "yarn.nodemanager.resource.memory-mb": 6144, "yarn.nodemanager.resource.cpu-vcores": 4,
                "yarn.scheduler.minimum-allocation-mb": 256,
                "yarn.nodemanager.vmem-check-enabled": "false",
                # the default marks a node UNHEALTHY when its disk is 90% full, and a shared
                # build machine's often is; the lab's jobs need megabytes
                "yarn.nodemanager.disk-health-checker.max-disk-utilization-per-disk-percentage": 99.5,
                "yarn.log-aggregation-enable": "true",
                "yarn.nodemanager.local-dirs": str(self.base / "nm-local"),
                "yarn.nodemanager.log-dirs": str(self.base / "nm-logs")}
        shutil.copytree(HADOOP / "etc" / "hadoop", self.conf)
        main_hdfs = {**hdfs, "dfs.datanode.data.dir": f"file://{self.base}/dn1"}
        # experiment 6's queues: production 75%, adhoc 25% and allowed to grow to 50%; a job that
        # names no queue goes to production
        mapred["mapreduce.job.queuename"] = "production"
        capacity = {"yarn.scheduler.capacity.root.queues": "production,adhoc",
                    "yarn.scheduler.capacity.root.production.capacity": 75,
                    "yarn.scheduler.capacity.root.adhoc.capacity": 25,
                    "yarn.scheduler.capacity.root.adhoc.maximum-capacity": 50,
                    "yarn.scheduler.capacity.maximum-am-resource-percent": 0.5}
        for name, props in (("core", core), ("hdfs", main_hdfs), ("mapred", mapred), ("yarn", yarn),
                            ("capacity-scheduler", capacity)):
            fname = name + ".xml" if name == "capacity-scheduler" else f"{name}-site.xml"
            (self.conf / fname).write_text(site(props))
        with open(self.conf / "hadoop-env.sh", "a") as fh:
            fh.write(f"\nexport JAVA_HOME={JAVA8}\n")
        self.datanodes[1] = self.conf
        for i in range(2, DATANODES + 1):         # the others: their own directory and ports
            d = self.base / f"dn{i}-conf"
            shutil.copytree(self.conf, d)
            (d / "hdfs-site.xml").write_text(site({
                **hdfs, "dfs.datanode.data.dir": f"file://{self.base}/dn{i}",
                "dfs.datanode.address": f"127.0.0.1:{9866 + 10 * i}",
                "dfs.datanode.http.address": f"127.0.0.1:{9864 + 10 * i}",
                "dfs.datanode.ipc.address": f"127.0.0.1:{9867 + 10 * i}"}))
            self.datanodes[i] = d

    def start_datanode(self, i):
        self.sh("hdfs --daemon start datanode", conf=self.datanodes[i],
                extra={} if i == 1 else {"HADOOP_IDENT_STRING": f"dn{i}"})

    def wait_for_datanodes(self, n, seconds=120):
        for _ in range(seconds):
            out = self.sh("hdfs dfsadmin -report -live", check=False)
            m = re.search(r"Live datanodes \((\d+)\)", out)
            if m and int(m.group(1)) >= n:
                return
            time.sleep(1)
        raise RuntimeError(f"fewer than {n} DataNodes came up")

    def start(self, yarn=True):
        for port in (9000, 9870, 8088, 8032):
            if not free(port):
                raise RuntimeError(f"port {port} is in use: is another cluster running?")
        self.write_conf()
        self.sh("hdfs namenode -format -nonInteractive -force")
        self.sh("hdfs --daemon start namenode")
        for i in self.datanodes:
            self.start_datanode(i)
        self.wait_for_datanodes(DATANODES)
        self.sh("hdfs dfsadmin -safemode wait")
        self.sh("hdfs --daemon start secondarynamenode")
        if yarn:
            self.sh("yarn --daemon start resourcemanager")
            self.sh("yarn --daemon start nodemanager")
            # the JobHistory server, which Pig and Hive ask for a finished job's counters --
            # without it they retry port 10020 again and again before giving up
            self.sh("mapred --daemon start historyserver")
            for _ in range(120):
                if "RUNNING" in self.sh("yarn node -list", check=False):
                    break
                time.sleep(1)
            else:
                raise RuntimeError("the NodeManager did not register")

    def stop(self):
        for pid in (self.base / "pids").glob("*.pid"):
            try:
                os.kill(int(pid.read_text().strip()), 15)
            except (ProcessLookupError, ValueError):
                pass
        for _ in range(30):
            alive = [p for p in (self.base / "pids").glob("*.pid") if _alive(p)]
            if not alive:
                return
            time.sleep(1)
        for p in alive:
            with contextlib.suppress(ProcessLookupError, ValueError):
                os.kill(int(p.read_text().strip()), 9)

    def run_script(self, script, cwd, extra_env=None):
        """Run a lab script as typed: "$ command" printed before each one runs. Returns the transcript."""
        e = dict(self.env, **(extra_env or {}))
        r = subprocess.run(["bash", "-c", echoed(pathlib.Path(script).read_text())], env=e, cwd=cwd,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=3600)
        return r.returncode, r.stdout


def _alive(pidfile):
    try:
        os.kill(int(pidfile.read_text().strip()), 0)
        return True
    except (ProcessLookupError, ValueError):
        return False


OPENS = re.compile(r"^\s*(for|while|until|if|case)\b|\{\s*$")
CLOSES = re.compile(r"^\s*(done|fi|esac)\b|\b(done|fi|esac)\s*;?\s*$|(^|;)\s*\}\s*$")


def open_quote(text):
    """Whether a quoted string is still open at the end of these lines -- a SQL query or a mysql -e
    argument that runs over several lines is one command."""
    import shlex
    body = "\n".join(ln for ln in text.split("\n") if not ln.lstrip().startswith("#"))
    try:
        shlex.split(body, comments=True)
        return False
    except ValueError:
        return True


def commands(text):
    """The script's commands, each whole: with its continuation lines, its here-documents, and --
    for a loop, an if or a { } group -- everything up to the line that closes it."""
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        if not lines[i].strip() or lines[i].lstrip().startswith("#"):
            i += 1
            continue
        cmd, depth = [], 0
        while i < len(lines):
            ln = lines[i]
            cmd.append(ln)
            code = "" if ln.lstrip().startswith("#") else re.sub(r"\s#\s.*$", "", ln)
            m = re.search(r"<<-?\s*'?(\w+)'?", code)
            if m:                               # a here-document runs to its terminator
                while i + 1 < len(lines) and lines[i + 1].strip() != m.group(1):
                    i += 1
                    cmd.append(lines[i])
                i += 1
                if i < len(lines):
                    cmd.append(lines[i])
            depth += bool(OPENS.search(code)) - bool(CLOSES.search(code))
            i += 1
            if depth <= 0 and not code.rstrip().endswith("\\") and not open_quote("\n".join(cmd)):
                break
        out.append("\n".join(cmd))
    return out


def shown(cmd):
    """A command as printed: trailing comments and the continuations' own comments dropped."""
    first = []
    for part in cmd.split("\n"):
        if re.match(r"^\s*#", part):
            continue
        first.append(re.sub(r"\s+#\s.*$", "", part).rstrip())
    return "\n".join(first)


def echoed(text):
    """The script with a printf of each command before it, so the transcript reads as typed."""
    body = ["set -o pipefail"]
    for cmd in commands(text):
        body.append("printf '%s\\n' " + _q("$ " + shown(cmd).replace("\n", "\n  ")))
        body.append(cmd)
    return "\n".join(body) + "\n"


def _q(s):
    return "'" + s.replace("'", "'\\''") + "'"


@contextlib.contextmanager
def mariadb(sql, port=3306):
    """A MySQL server (MariaDB, from the Ubuntu archive) in a temporary folder, on localhost, with
    `sql` run as root first -- the database a Sqoop experiment imports from. Stopped at the end."""
    data = pathlib.Path(tempfile.mkdtemp(prefix="mariadb_lab_"))
    sock = data / "mysqld.sock"
    subprocess.run(["mariadb-install-db", f"--datadir={data / 'db'}", "--user=root",
                    "--auth-root-authentication-method=normal"], check=True, capture_output=True)
    server = subprocess.Popen(["mariadbd", f"--datadir={data / 'db'}", f"--socket={sock}",
                               f"--port={port}", "--bind-address=127.0.0.1", "--user=root",
                               "--skip-log-error", f"--pid-file={data / 'mysqld.pid'}"],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            if sock.exists() and subprocess.run(["mysql", f"--socket={sock}", "-uroot", "-e", "SELECT 1"],
                                                capture_output=True).returncode == 0:
                break
            time.sleep(1)
        else:
            raise RuntimeError("MariaDB did not start")
        subprocess.run(["mysql", f"--socket={sock}", "-uroot"], input=sql, text=True, check=True,
                       capture_output=True)
        yield sock
    finally:
        server.terminate()
        server.wait(timeout=60)
        shutil.rmtree(data, ignore_errors=True)


@contextlib.contextmanager
def cluster(yarn=True):
    if not (HADOOP / "bin" / "hdfs").exists():
        raise SystemExit(f"Hadoop not found in {PREFIX}: run tools/data-science/setup_hadoop.sh")
    base = pathlib.Path(tempfile.mkdtemp(prefix="hadoop_lab_"))
    c = Cluster(base)
    try:
        c.start(yarn=yarn)
        yield c
    finally:
        c.stop()
        shutil.rmtree(base, ignore_errors=True)


def job(lab_file, commands, extra_env=None, yarn=True, then_file=False, hadoop=True):
    """Run a lab file the way its experiment does: the lab's inputs written beside it, a cluster
    started, then `commands` -- the setup the file assumes, and the command that runs it -- each
    printed as typed; with then_file, the lab script's own commands follow, printed the same way.
    A driver's whole job; it exits with the last command's status."""
    import sys
    lab_file = pathlib.Path(lab_file).resolve()
    sys.path.insert(0, str(lab_file.parent))
    import _inputs
    _inputs.write(pathlib.Path.cwd())
    runner = pathlib.Path.cwd() / ("_run_" + lab_file.stem + ".sh")
    text = "\n".join(commands) + "\n"
    if then_file:                       # then the lab script itself, each of its commands printed
        text += lab_file.read_text()
    runner.write_text(text)
    if hadoop:
        with cluster(yarn=yarn) as c:
            code, out = c.run_script(runner, pathlib.Path.cwd(), {"USER": "root", **(extra_env or {})})
            out = out.replace(str(c.base), "/tmp/hadoop-lab")
    else:                               # a tool that needs no cluster: the same environment, alone
        base = pathlib.Path(tempfile.mkdtemp(prefix="hadoop_lab_"))
        e = dict(env(base, base / "conf"), USER="root", **(extra_env or {}))
        r = subprocess.run(["bash", "-c", echoed(runner.read_text())], env=e, cwd=pathlib.Path.cwd(),
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=3600)
        code, out = r.returncode, r.stdout.replace(str(base), "/tmp/hadoop-lab")
        shutil.rmtree(base, ignore_errors=True)
    sys.stdout.write(out)
    runner.unlink()
    sys.exit(code)


def java_job(java_file):
    """Run a lab's MapReduce program as its header says -- the "Build and run:" lines -- after
    loading the six documents into HDFS, then print what it wrote."""
    header = pathlib.Path(java_file).read_text().split("// Build and run:", 1)[1].split("\n\n", 1)[0]
    build = [ln[len("//   "):] for ln in header.split("\n") if ln.startswith("//   ")]
    out_dir = build[-1].split()[-1]
    job(java_file, [
        "hdfs dfs -mkdir -p /user/student/docs",
        "hdfs dfs -put docs/*.txt /user/student/docs/",
        "hdfs dfs -ls /user/student/docs | awk 'NR>1{print $NF}'",
        "mkdir -p classes",
        *build[:-1],
        build[-1] + " 2>&1 | grep -E \"completed successfully|Map input records|Map output records|"
                    "Combine input records|Combine output records|Reduce input groups|Reduce output records\"",
        f"hdfs dfs -cat {out_dir}/part-r-00000",
    ])


if __name__ == "__main__":
    # python3 hadoop_lab.py SCRIPT.sh -- the lab's inputs written beside it, a cluster started,
    # the script run as typed, the cluster stopped. Its temporary folder is named as the
    # lab page names it, so the transcript is the same on every run.
    import sys
    script = pathlib.Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(script.parent))
    import _inputs
    _inputs.write(pathlib.Path.cwd())
    with cluster() as c:
        code, out = c.run_script(script, pathlib.Path.cwd(), {"USER": "root"})
        sys.stdout.write(out.replace(str(c.base), "/tmp/hadoop-lab"))
    sys.exit(code)

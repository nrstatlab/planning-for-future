"""Run a Course 10 mongosh script as a student would type it, on a fresh server, for
capture_lab_outputs.py.

    python3 mongo_lab.py 03_find_compare.js        # from the course folder

It starts a new mongod on the default port, 27017, in a temporary data directory, types
the script into mongosh line by line (on standard input, so `use` and `show` work as
they do at the prompt), stops the server, and prints the session: each statement after
the prompt it was typed at, then what mongosh printed for it. Comment and blank lines,
which print nothing, are left out of the transcript; they are in the programme.

The server is a one-member replica set when a script needs one (transactions do), and a
standalone otherwise, as a fresh install is. A driver beside a script
(_drive_17_replication.py) uses server() and session() to do more: start three members,
or run a command-line tool between shell sessions.

The binaries come from $MONGODB_HOME/bin (tools/data-science/setup_mongodb.sh puts them
in /tmp/mongodb), and mongosh from tools/data-science/node_modules (npm install).
"""
import contextlib
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = pathlib.Path(__file__).resolve().parent
BIN = pathlib.Path(os.environ.get("MONGODB_HOME", "/tmp/mongodb")) / "bin"
MONGOSH = HERE / "node_modules/.bin/mongosh"
REPLICA_SET = {"19_transactions.js"}        # the scripts that need one
# The prompt mongosh prints before reading each line: "collegeDB> ", or on a replica set
# "rs0 [direct: primary] collegeDB> ". A statement's continuation lines get "... ".
PROMPT = re.compile(r"((?:[\w-]+ \[[^\]]*\] )?[\w-]+)> ")


def tool(name):
    path = MONGOSH if name == "mongosh" else BIN / name
    if not path.exists():
        sys.exit(f"{name} not found at {path}: run tools/data-science/setup_mongodb.sh "
                 "and npm --prefix tools/data-science install")
    return str(path)


_HOME = None


def quiet_env():
    """mongosh's environment: a home folder of its own, in which disableTelemetry() has been
    run, so that no session reports usage to MongoDB -- which the shell does by default."""
    global _HOME
    if _HOME is None:
        _HOME = tempfile.mkdtemp(prefix="mongosh-home-")
        subprocess.run([tool("mongosh"), "--nodb", "--quiet", "--eval", "disableTelemetry()"],
                       env=dict(os.environ, HOME=_HOME), capture_output=True, text=True)
    return dict(os.environ, HOME=_HOME)


def shell(js, port=27017):
    """Evaluate one expression in a quiet mongosh, for set-up: its output is not shown."""
    return subprocess.run([tool("mongosh"), "--quiet", "--norc",
                           f"mongodb://127.0.0.1:{port}/?directConnection=true", "--eval", js],
                          capture_output=True, text=True, env=quiet_env()).stdout.strip()


@contextlib.contextmanager
def server(port=27017, replica_set=None, members=None):
    """A fresh mongod on `port`, stopped and deleted afterwards. With replica_set, it is
    initiated as a set of one, or of `members` (a list of ports, all started here)."""
    ports = members or [port]
    with tempfile.TemporaryDirectory() as tmp:
        for p in ports:
            data = pathlib.Path(tmp) / str(p)
            data.mkdir()
            cmd = [tool("mongod"), "--dbpath", str(data), "--port", str(p), "--bind_ip", "127.0.0.1",
                   "--fork", "--logpath", str(data / "mongod.log"), "--pidfilepath", str(data / "pid")]
            if replica_set:
                cmd += ["--replSet", replica_set]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode:
                sys.exit(f"mongod would not start on port {p}:\n{r.stdout}{r.stderr}")
        try:
            if replica_set and not members:
                shell(f"rs.initiate({{_id: '{replica_set}', members: [{{_id: 0, host: '127.0.0.1:{port}'}}]}})", port)
                for _ in range(150):
                    if shell("db.hello().isWritablePrimary", port) == "true":
                        break
                    time.sleep(0.2)
                else:
                    sys.exit("the replica set elected no primary")
            yield ports
        finally:
            for p in ports:
                shell("db.getSiblingDB('admin').shutdownServer({force: true})", p)
            for p in ports:                              # wait for each to exit before deleting its data
                pid = int((pathlib.Path(tmp) / str(p) / "pid").read_text())
                for _ in range(200):
                    try:
                        os.kill(pid, 0)
                    except ProcessLookupError:
                        break
                    time.sleep(0.05)


def session(src, port=27017, full_prompt=False):
    """Type `src` into mongosh, and return the transcript: each statement, then its output."""
    out = subprocess.run([tool("mongosh"), "--quiet", "--norc",
                          f"mongodb://127.0.0.1:{port}/?directConnection=true"],
                         input=src, capture_output=True, text=True, timeout=600, env=quiet_env()).stdout
    out = out.replace("\r", "")
    lines = src.split("\n")
    parts = PROMPT.split(out)                   # [before, prompt1, chunk1, prompt2, chunk2, ...]
    shown, i = [], 0
    for k in range(1, len(parts) - 1, 2):
        prompt, chunk = parts[k], parts[k + 1]
        more = 0
        while chunk.startswith("... "):          # one per continuation line of the statement
            chunk = chunk[4:]
            more += 1
        statement = lines[i:i + 1 + more]
        i += 1 + more
        text = chunk.rstrip("\n")
        if not text.strip() and all(re.fullmatch(r"\s*(//.*)?", ln) for ln in statement):
            continue                               # a comment or a blank line
        if not full_prompt:
            prompt = prompt.split(" ")[-1]
        shown.append(f"{prompt}> " + "\n... ".join(statement) + ("\n" + text if text.strip() else ""))
    if i < len(lines) - 1:
        sys.exit(f"mongosh stopped after line {i} of {len(lines)}:\n{out[-2000:]}")
    return "\n".join(shown) + "\n"


def run(script):
    """The usual case: a fresh server, the script typed in, the transcript printed."""
    src = pathlib.Path(script).read_text()
    rs = "rs0" if pathlib.Path(script).name in REPLICA_SET else None
    with server(replica_set=rs):
        print(session(src, full_prompt=bool(rs)), end="")


if __name__ == "__main__":
    run(sys.argv[1])

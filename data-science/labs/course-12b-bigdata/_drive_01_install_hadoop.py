"""Run 01_install_hadoop.sh as a student would, in an empty home directory.

The script downloads Hadoop unless the tarball is already in the folder; setup_hadoop.sh has
fetched it, checked, so it is linked in rather than downloaded a second time. Java 11 comes first
on the PATH, as the script's JAVA_HOME expects. Any daemon left running is stopped at the end.
"""
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

import hadoop_lab as H

here = pathlib.Path.cwd()
tarball = H.PREFIX / "downloads" / "hadoop-3.3.6.tar.gz"
if not tarball.exists():
    sys.exit(f"{tarball} not found: run tools/data-science/setup_hadoop.sh")
os.symlink(tarball, here / "hadoop-3.3.6.tar.gz")
home = pathlib.Path(tempfile.mkdtemp(prefix="hadoop_home_"))
java11 = "/usr/lib/jvm/java-11-openjdk-amd64"
env = {k: v for k, v in os.environ.items()
       if not k.startswith(("HADOOP", "YARN", "HDFS", "JAVA")) and k != "CLASSPATH"}
env.update(HOME=str(home), USER="root", PATH=f"{java11}/bin:/usr/bin:/bin:/usr/sbin:/sbin",
           HDFS_NAMENODE_USER="root", HDFS_DATANODE_USER="root", HDFS_SECONDARYNAMENODE_USER="root",
           YARN_RESOURCEMANAGER_USER="root", YARN_NODEMANAGER_USER="root")
try:
    r = subprocess.run(["bash", "-c", H.echoed((here / "01_install_hadoop.sh").read_text())], env=env,
                       cwd=here, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=900)
    sys.stdout.write(r.stdout.replace(str(home), "~"))
finally:
    for pid in pathlib.Path("/tmp").glob("hadoop-root-*.pid"):     # the default pid directory
        try:
            os.kill(int(pid.read_text().strip()), 9)
        except (ProcessLookupError, ValueError):
            pass
        pid.unlink(missing_ok=True)
    shutil.rmtree(home, ignore_errors=True)
    (here / "hadoop-3.3.6.tar.gz").unlink(missing_ok=True)

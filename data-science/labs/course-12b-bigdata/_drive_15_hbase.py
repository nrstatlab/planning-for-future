"""Run 15_hbase.rb in the HBase shell, against HBase in standalone mode: one JVM holding the
master, a RegionServer and its own ZooKeeper, storing to a folder here -- which needs no Hadoop
cluster.

The shell reads the commands from stdin, as if typed, and echoes each after its prompt; the
comment lines are left out of what it is fed (they are in the file, on the lab page). Its INFO
logging is turned down to errors. Every command's "Took 0.0xxx seconds" is the time it took on
this machine. Snappy compression uses HBase's own codec (snappy-java), because Hadoop's native
library is not installed: without it, create fails with UnsatisfiedLinkError in
NativeCodeLoader.buildSupportsSnappy."""
import pathlib
import re

import hadoop_lab

here = pathlib.Path.cwd()
conf = here / "hbase-conf"
conf.mkdir(exist_ok=True)
(conf / "hbase-site.xml").write_text(hadoop_lab.site({
    "hbase.cluster.distributed": "false",
    "hbase.rootdir": f"file://{here}/hbase-root",
    "hbase.zookeeper.property.dataDir": f"{here}/hbase-zk",
    "hbase.unsafe.stream.capability.enforce": "false",
    "hbase.io.compress.snappy.codec": "org.apache.hadoop.hbase.io.compress.xerial.SnappyCodec",
}))
typed = [ln for ln in pathlib.Path("15_hbase.rb").read_text().split("\n")
         if ln.strip() and not re.match(r"\s*#", ln)]
pathlib.Path("15_hbase.typed").write_text("\n".join(typed) + "\n")
hadoop_lab.job("15_hbase.rb", [
    "start-hbase.sh > /dev/null 2>&1",
    "sleep 20",
    "hbase shell -n < 15_hbase.typed 2>&1",
    "stop-hbase.sh 2>&1 | tail -1",
], hadoop=False, extra_env={"HBASE_CONF_DIR": str(conf), "HBASE_LOG_DIR": str(here / "hbase-logs"),
                            "HBASE_PID_DIR": str(here / "hbase-pids"),
                            "HBASE_ROOT_LOGGER": "ERROR,console",
                            # HBase ships the Hadoop client it was built with; it is told not to
                            # add the cluster's own as well, whose logging and codecs differ
                            "HBASE_DISABLE_HADOOP_CLASSPATH_LOOKUP": "true"})

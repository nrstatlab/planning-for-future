"""Run the 12_flume.conf agent against a cluster: the lab's 40 access-log lines placed where its
TAILDIR source looks, the agent run for 45 seconds and stopped, then what reached each sink --
the logger sink writes its events to the agent's console, kept in agent.log, and their headers
are counted there. The HDFS sink names its folder for the date and hour of the run, and its file
for the millisecond it opened it."""
import hadoop_lab

hadoop_lab.job("12_flume.conf", [
    "rm -rf /tmp/flume-lab && mkdir -p /tmp/flume-lab/logs",
    "cp access.log /tmp/flume-lab/logs/access.log.1",
    "wc -l < /tmp/flume-lab/logs/access.log.1",
    "timeout 45 flume-ng agent --conf $FLUME_HOME/conf --conf-file 12_flume.conf "
    "--name a1 -Dflume.root.logger=INFO,console > agent.log 2>&1",
    "grep -c 'LoggerSink: Event:' agent.log",
    "grep 'LoggerSink: Event:' agent.log | grep -oE 'path=[^,]+|status=[0-9]+' | paste - - | sort | uniq -c",
    "hdfs dfs -ls -R /logs | awk '{print $NF}'",
    "hdfs dfs -cat '/logs/*/*/*' | wc -l",
    "hdfs dfs -cat '/logs/*/*/*' | awk '{print $9}' | sort | uniq -c",
    "awk '/ (ERROR|FATAL) /' agent.log | sed -E 's/^[0-9T:,-]+ //' | sort -u | head -5",
])

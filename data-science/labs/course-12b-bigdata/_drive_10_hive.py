"""Run 10_hive.hql on a cluster: the sales file where its EXTERNAL table looks, Hive's metastore
created (embedded Derby, in this folder), then hive -f. Hive prints results to stdout and its
"OK / Time taken" lines to stderr, which is kept in hive.log; its errors would be shown from there,
and there are none. On leaving, it prints two WARN lines about its logging library to stdout,
which are left out."""
import hadoop_lab

hadoop_lab.job("10_hive.hql", [
    "hdfs dfs -mkdir -p /user/student/sales /user/hive/warehouse /tmp/hive",
    "hdfs dfs -chmod 733 /tmp/hive && hdfs dfs -chmod g+w /user/hive/warehouse",
    "hdfs dfs -put sales.csv /user/student/sales/",
    "schematool -dbType derby -initSchema 2>&1 | grep -E 'schemaTool completed'",
    "hive -f 10_hive.hql 2>hive.log | grep -v '^WARN: '",
    "awk '/^FAILED|^Error|Exception/' hive.log | head -5",
])

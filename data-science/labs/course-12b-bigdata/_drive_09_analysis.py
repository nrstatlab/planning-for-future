"""Run 09_analysis.pig on a cluster: the files it LOADs put where it looks, then pig -x mapreduce."""
import hadoop_lab

hadoop_lab.job("09_analysis.pig", [
    "hdfs dfs -mkdir -p /user/student/sales /user/student/dim",
    "hdfs dfs -put sales.csv /user/student/sales/",
    "hdfs dfs -put stores.csv /user/student/dim/",
    "hdfs dfs -put tags.tsv /user/student/tags.csv",
    "pig -x mapreduce 09_analysis.pig 2>pig.log",
    "grep -E 'ERROR|Success|Failed' pig.log | sed -E 's/^[0-9-]+ [0-9:,]+ //' | head -12",
    "hdfs dfs -cat /user/student/out/by_category/part-r-00000",
])

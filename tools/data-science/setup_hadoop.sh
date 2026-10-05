#!/usr/bin/env bash
# Install the Hadoop stack for Course 12 B: Hadoop, Pig, Hive, HBase, ZooKeeper, Sqoop and Flume.
#
# Every release is kept at archive.apache.org (dlcdn.apache.org keeps only the current ones), and
# each file is checked against the SHA-256 below -- computed here after checking the SHA-512,
# SHA-256 or MD5 that Apache publishes beside each one. Java 8 and 11 and MariaDB come from the
# Ubuntu archive; Java 8 runs every tool here, and Java 11 is the one experiment 1 installs Hadoop
# with. Spark is separate: tools/data-science/setup_spark.sh.
#
# Two fixes are applied after unpacking, each a known incompatibility of these releases:
#   * Hive 3.1.3 ships Guava 19 and Hadoop 3.3.6 needs Guava 27: Hive's copy is replaced by
#     Hadoop's, or Hive stops with NoSuchMethodError in com.google.common.base.Preconditions.
#   * Sqoop 1.4.7 calls commons-lang 2, which Hadoop 3 no longer ships; it needs the MySQL JDBC
#     driver; and its saved jobs (sqoop job) need org.json, which it does not ship -- without it
#     `sqoop job --create` fails with NoClassDefFoundError: org/json/JSONObject, after storing
#     the job's name but none of its options. All three come from Maven Central.
#
# The tools go in ${HADOOP_PREFIX:-/tmp/hadoop}; tools/data-science/hadoop_lab.py finds them there.
set -euo pipefail

PREFIX="${HADOOP_PREFIX:-/tmp/hadoop}"
ARCHIVE="https://archive.apache.org/dist"
MAVEN="https://repo1.maven.org/maven2"

TARBALLS=(    # sha256, path in the archive, the folder it unpacks to
  "f5195059c0d4102adaa7fff17f7b2a85df906bcb6e19948716319f9978641a04 hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz hadoop-3.3.6"
  "6d613768e9a6435ae8fa758f8eef4bd4f9d7f336a209bba3cd89b843387897f3 pig/pig-0.17.0/pig-0.17.0.tar.gz pig-0.17.0"
  "0c9b6a6359a7341b6029cc9347435ee7b379f93846f779d710b13f795b54bb16 hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz apache-hive-3.1.3-bin"
  "5cd67fb04b2182b37e9befc6b91ad5df4b634b300a08e7875470b997bde08633 hbase/2.5.10/hbase-2.5.10-hadoop3-bin.tar.gz hbase-2.5.10-hadoop3"
  "284cb4675adb64794c63d95bf202d265cebddc0cda86ac86fb0ede8049de9187 zookeeper/zookeeper-3.8.4/apache-zookeeper-3.8.4-bin.tar.gz apache-zookeeper-3.8.4-bin"
  "64111b136dbadcb873ce17e09201f723d4aea81e5e7c843e400eb817bb26f235 sqoop/1.4.7/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz sqoop-1.4.7.bin__hadoop-2.6.0"
  "6eb7806076bdc3dcadb728275eeee7ba5cb12b63a2d981de3da9063008dba678 flume/1.11.0/apache-flume-1.11.0-bin.tar.gz apache-flume-1.11.0-bin"
)
JARS=(
  "d77962877d010777cff997015da90ee689f0f4bb76848340e1488f2b83332af5 com/mysql/mysql-connector-j/8.4.0/mysql-connector-j-8.4.0.jar"
  "50f11b09f877c294d56f24463f47d28f929cf5044f648661c0f0cfbae9a2f49c commons-lang/commons-lang/2.6/commons-lang-2.6.jar"
  "0f18192df289114e17aa1a0d0a7f8372cc9f5c7e4f7e39adcf8906fe714fa7d3 org/json/json/20231013/json-20231013.jar"
)

sudo=""; [ "$(id -u)" -ne 0 ] && sudo="sudo"
for pkg in openjdk-8-jdk-headless openjdk-11-jdk-headless mariadb-server; do
    dpkg -s "$pkg" >/dev/null 2>&1 || $sudo apt-get install -y "$pkg"
done

mkdir -p "$PREFIX/downloads"
fetch() {    # sha256, url, destination
    if [ ! -f "$3" ] || ! echo "$1  $3" | sha256sum -c --quiet - 2>/dev/null; then
        curl -sSf --retry 3 -o "$3" "$2"
        echo "$1  $3" | sha256sum -c --quiet - || { echo "checksum mismatch: $3"; exit 1; }
    fi
}
for entry in "${TARBALLS[@]}"; do
    read -r sum path dir <<< "$entry"
    tarball="$PREFIX/downloads/$(basename "$path")"
    # experiment 1 installs Hadoop from its tarball, so that one is kept; the rest are deleted
    # once unpacked, and a tool already unpacked is not fetched again
    case "$path" in hadoop/*) fetch "$sum" "$ARCHIVE/$path" "$tarball" ;; esac
    [ -d "$PREFIX/$dir" ] && continue
    fetch "$sum" "$ARCHIVE/$path" "$tarball"
    tar -xzf "$tarball" -C "$PREFIX"
    [ -d "$PREFIX/$dir" ] || { echo "$tarball did not unpack to $dir"; exit 1; }
    case "$path" in hadoop/*) ;; *) rm -f "$tarball" ;; esac
done

SQOOP="$PREFIX/sqoop-1.4.7.bin__hadoop-2.6.0"
for entry in "${JARS[@]}"; do
    read -r sum path <<< "$entry"
    fetch "$sum" "$MAVEN/$path" "$SQOOP/lib/$(basename "$path")"
done

HIVE="$PREFIX/apache-hive-3.1.3-bin"
if [ -f "$HIVE/lib/guava-19.0.jar" ]; then
    rm "$HIVE/lib/guava-19.0.jar"
    cp "$PREFIX/hadoop-3.3.6/share/hadoop/common/lib/guava-27.0-jre.jar" "$HIVE/lib/"
fi

echo "Hadoop stack ready in $PREFIX:"
ls -1 "$PREFIX" | grep -v downloads

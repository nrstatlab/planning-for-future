#!/usr/bin/env bash
# Install WEKA 3.8.7 and its standard datasets, for Course 8.
#
# WEKA's own site cannot be reached where these labs are checked, but Maven Central serves
# the WEKA jar and its libraries, and the Waikato weka-3.8 repository serves the datasets
# that come with WEKA (wekadocs/data), so they come from there. Every file is checked
# against the SHA-256 below, so a run elsewhere uses exactly these. Java 11 or later.
#
# The labs' _weka.sh scripts run WEKA from the command line, which prints what the
# Explorer's output pane shows; labs/course-8-datamining/weka.sh finds it in $WEKA_HOME.
set -euo pipefail

HOME_DIR="${WEKA_HOME:-/tmp/weka}"
MAVEN="https://repo1.maven.org/maven2"
DATA="https://raw.githubusercontent.com/Waikato/weka-3.8/master/wekadocs/data"

JARS=(
  "af190b26a22051aeafc0483772faebf4b378d0ebda7b338feb3c34206b812b24 nz/ac/waikato/cms/weka/weka-stable/3.8.7/weka-stable-3.8.7.jar"
  "bffff1505335c02256b7ab2ccffbe4aa4d3ac9fe14c17557809b7c9d99d666ca nz/ac/waikato/cms/weka/thirdparty/bounce/0.18/bounce-0.18.jar"
  "27a53db335bc6af524b30f97ec3fb4b6df65e7648d70e752447c7dd9bc4697c8 com/googlecode/matrix-toolkits-java/mtj/1.0.4/mtj-1.0.4.jar"
  "9964fb948ef213548a79b23dd480af9d72f1450824fa006bbfea211ac1ffa6dc net/sourceforge/f2j/arpack_combined_all/0.1/arpack_combined_all-0.1.jar"
  "814b9cf2425bd05d836055a7293a227c297c65126bb091fa50230905421b8126 com/googlecode/netlib-java/netlib-java/1.1/netlib-java-1.1.jar"
  "5c01edb6a4371f601a1de816f36cd7da47cb8a34ecc99eac5fe7ed660854b559 com/github/vbmacher/java-cup-runtime/11b-20160615/java-cup-runtime-11b-20160615.jar"
  "e1522945218456f3649a39bc4afd70ce4bd466221519dba7d378f2141a4642ca org/apache/commons/commons-compress/1.28.0/commons-compress-1.28.0.jar"
  "5ffaddee0a3f8d09a56064aa05feb95837ddad9d42d9dcc37479c66e869aa139 com/github/fommil/netlib/core/1.1.2/core-1.1.2.jar"
  "2f1def54f30e1db5f1e7f2fd600fe2ab331bd6b52037e9a21505c237020b5573 com/github/fommil/jniloader/1.1/jniloader-1.1.jar"
  "07d946b36edbf5e3c613ed38787ced7853a5eaf3af93c91a27a943ad62efe802 com/github/fracpete/jfilechooser-bookmarks/0.1.11/jfilechooser-bookmarks-0.1.11.jar"
)
DATASETS=(
  "eadeb79b8a0d341e1fdc6314aded92ada89b4f6cb41fdd38fead3c82bd4f45a7 weather.nominal.arff"
  "1453f37518d1320241cb8558fa7d0b01537db9e4cb45cea277fd898c1e8b881d weather.numeric.arff"
  "7d34ba556497e9dc28335ea6628a37d1dbcba090a1ae20dc2de9c7032d199153 iris.arff"
  "c45f18f90f27f9b2306671f4f0ec28341edcff78136b32b202cdc7b46ce1f9f8 supermarket.arff"
  "5d2733aa879fdab2c2108efeedc874e6ffee6bcc121472eda9002096dddab36f labor.arff"
  "77d2ed4b3cc5c1b5d54464ab4776bee797953b57f3e96e3fcc91df48f69e945b contact-lenses.arff"
  "ee647a77207729d73d02cea20646afcd274fe9de95711cbf9909c903636cd65f vote.arff"
  "1855af1b69c21491a103ae414a1ffe5103c633aa5ad920abde2115aac9f55322 ReutersCorn-train.arff"
)

command -v java >/dev/null || { echo "java not found: WEKA needs Java 11 or later"; exit 1; }
mkdir -p "$HOME_DIR/data"

fetch() {    # sha256, url, destination
    if [ ! -f "$3" ] || ! echo "$1  $3" | sha256sum -c --quiet - 2>/dev/null; then
        curl -sSf --retry 3 -o "$3" "$2"
        echo "$1  $3" | sha256sum -c --quiet - || { echo "checksum mismatch: $3"; exit 1; }
    fi
}
for entry in "${JARS[@]}"; do
    read -r sum path <<< "$entry"
    fetch "$sum" "$MAVEN/$path" "$HOME_DIR/$(basename "$path")"
done
for entry in "${DATASETS[@]}"; do
    read -r sum name <<< "$entry"
    fetch "$sum" "$DATA/$name" "$HOME_DIR/data/$name"
done

# Maven Central publishes this jar as 3.8.7; the jar's own version file says 3-8-8-snapshot.
echo "WEKA 3.8.7 (its version.txt: $(unzip -p "$HOME_DIR/weka-stable-3.8.7.jar" weka/core/version.txt))"
echo "WEKA ready in $HOME_DIR, with ${#DATASETS[@]} datasets in $HOME_DIR/data"

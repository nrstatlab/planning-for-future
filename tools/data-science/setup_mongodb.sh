#!/usr/bin/env bash
# Install a real MongoDB server and its tools, for Course 10.
#
# MongoDB's own download hosts (fastdl.mongodb.org, repo.mongodb.org) are
# blocked where these labs are checked, but conda-forge's builds of the same
# server can be reached, so the packages come from there. No conda is needed:
# a .conda package is a zip of two zstd tarballs, and the binaries in it link
# only against libraries Ubuntu 24.04 already has (libcurl, libssl3, libsasl2,
# libstdc++).
#
#   mongod 8.3.7       the server
#   mongo-tools 100.13 mongofiles, mongoimport, mongodump and the rest
#   mongosh 2.12.0     the shell, from npm (npm --prefix tools/data-science install)
#
# tools/data-science/mongo_lab.py finds them in $MONGODB_HOME/bin.
set -euo pipefail

HOME_DIR="${MONGODB_HOME:-/tmp/mongodb}"
CHANNEL="https://conda.anaconda.org/conda-forge/linux-64"
PACKAGES=("mongodb-8.3.7-hc064ac0_0.conda" "mongo-tools-100.13.0-ha770c72_0.conda")

command -v zstd >/dev/null || { echo "zstd not found: apt-get install zstd"; exit 1; }
mkdir -p "$HOME_DIR"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

for pkg in "${PACKAGES[@]}"; do
    echo "fetching $pkg"
    curl -sSf --retry 3 -o "$work/$pkg" "$CHANNEL/$pkg"
    python3 -c "import sys, zipfile; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" \
        "$work/$pkg" "$work/${pkg%.conda}"
    for t in "$work/${pkg%.conda}"/pkg-*.tar.zst; do
        zstd -dqc "$t" | tar -x -C "$HOME_DIR"
    done
done

"$HOME_DIR/bin/mongod" --version | head -1
"$HOME_DIR/bin/mongofiles" --version | head -1
echo "MongoDB ready in $HOME_DIR/bin"

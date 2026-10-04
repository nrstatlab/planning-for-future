"""Drives 18_gridfs.js against a real server, with the real mongofiles.

Run by tools/data-science/capture_lab_outputs.py, with tools/data-science/mongo_lab.py. It
makes a 10 MB file, lecture.mp4 (10,485,760 bytes of a fixed pattern, not a video: GridFS
does not look inside), and runs the mongofiles commands of section 1 -- put, list, get to a
copy, which is compared with the original byte for byte. Then it types sections 2 to 4 of
the script into mongosh, and last runs mongofiles delete, as section 5 recommends, and
counts what is left.

mongofiles cannot attach metadata, so section 4's queries on metadata.course find nothing,
as they would after any mongofiles put; a driver upload, as in section 3, sets it.
"""
import hashlib
import pathlib
import subprocess

from mongo_lab import server, session, shell, tool

SRC = open("18_gridfs.js").read()
lines = SRC.split("\n")
start = next(i for i, ln in enumerate(lines) if ln.startswith("use collegeDB"))
end = next(i for i, ln in enumerate(lines) if "// 5. Deleting" in ln)

data = bytes(range(256)) * (10 * 1024 * 1024 // 256)          # exactly 10 MB
pathlib.Path("lecture.mp4").write_bytes(data)


def mongofiles(*args):
    print("$ mongofiles " + " ".join(args))
    r = subprocess.run([tool("mongofiles"), "--quiet", *args], capture_output=True, text=True)
    print((r.stdout + r.stderr).rstrip() or "(nothing printed)")
    assert r.returncode == 0, f"mongofiles {args[2]} failed"


with server():
    print(f"made lecture.mp4: {len(data):,} bytes\n")
    mongofiles("-d", "collegeDB", "put", "lecture.mp4")
    mongofiles("-d", "collegeDB", "list")
    mongofiles("-d", "collegeDB", "--local", "./copy.mp4", "get", "lecture.mp4")
    same = hashlib.sha256(pathlib.Path("copy.mp4").read_bytes()).hexdigest() == hashlib.sha256(data).hexdigest()
    print(f"copy.mp4 is the same as lecture.mp4, byte for byte: {same}\n")
    assert same

    print(session("\n".join(lines[start:end])))

    chunks = shell("db.getSiblingDB('collegeDB').fs.chunks.countDocuments()")
    assert chunks == "41", f"expected 41 chunks, found {chunks}"
    mongofiles("-d", "collegeDB", "delete", "lecture.mp4")
    left = shell("const d = db.getSiblingDB('collegeDB'); d.fs.files.countDocuments() + ' files, ' + d.fs.chunks.countDocuments() + ' chunks'")
    print(f"after mongofiles delete: {left} -- the metadata document AND its chunks")
    assert left == "0 files, 0 chunks", left

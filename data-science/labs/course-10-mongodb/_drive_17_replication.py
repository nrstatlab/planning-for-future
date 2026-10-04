"""Drives 17_replication.js on a real three-member replica set, as section 0 of the script
describes for a machine without Docker: three mongod processes on ports 27017, 27018 and
27019, and a fourth on 27020 for the arbiter of section 6.

Run by tools/data-science/capture_lab_outputs.py, with tools/data-science/mongo_lab.py. The
script's parts are typed into mongosh on the member each one names: most on the primary,
section 2's reads on the secondary at 27018. Two waits stand in for the moments a student
would wait at the shell: for the election after rs.initiate(), and for a new primary after
rs.stepDown().

An election, the oplog and every time in rs.status() differ from one run to the next, so
this output is one run's, recorded. What the experiment demonstrates is asserted on every
run instead: one PRIMARY and two SECONDARY members, the write replicated to a secondary,
a new primary after the step-down, and the reconfiguration and the arbiter accepted.
"""
import re
import time

from mongo_lab import server, session, shell

SRC = open("17_replication.js").read()


def cut(src, start, end=None):
    """The lines of src from the line containing `start` up to the one containing `end`."""
    lines = src.split("\n")
    a = next(i for i, ln in enumerate(lines) if start in ln)
    b = next(i for i in range(a + 1, len(lines)) if end in lines[i]) if end else len(lines)
    return "\n".join(lines[a:b])


def primary_port():
    for _ in range(300):
        for port in (27017, 27018, 27019):
            if shell("db.hello().isWritablePrimary", port) == "true":
                return port
        time.sleep(0.2)
    raise SystemExit("no primary was elected")


def settled():
    """One primary and two secondaries, as rs.status() should show the examiner."""
    for _ in range(300):
        states = shell("rs.status().members.map(m => m.stateStr).sort().join(',')", 27017)
        if states == "PRIMARY,SECONDARY,SECONDARY":
            return states
        time.sleep(0.2)
    raise SystemExit(f"the set did not settle: {states}")


def printed(out):
    """What mongosh printed, without the statements typed: the comments must not count."""
    return "\n".join(ln for ln in out.split("\n")
                     if not re.match(r"(rs0 \[[^\]]*\] )?[\w-]+> |\.\.\. ", ln))


def show(part, port, what):
    print(f"[mongosh connected to 127.0.0.1:{port}, {what}]")
    out = session(part, port=port, full_prompt=True)
    print(out)
    return out


with server(replica_set="rs0", members=[27017, 27018, 27019, 27020]):
    show(cut(SRC, "// 1. Initiating the set", "// The shell prompt changes"), 27017, "not yet in a set")
    print(f"[waited for the election: {settled()}]\n")
    p = primary_port()
    show(cut(SRC, "// The shell prompt changes", "// On a SECONDARY"), p, "the primary")

    out = printed(show(cut(SRC, "// On a SECONDARY", "// 3. The oplog"), 27018, "a secondary"))
    assert "Asha" in out, "the write did not reach the secondary"
    assert "mode: 'primary'" in out, "the read preference was not 'primary'"

    p = primary_port()
    show(cut(SRC, "// 3. The oplog", "// Watch: an election starts"), p, "the primary")
    for _ in range(300):                                  # the old primary steps down
        q = primary_port()
        if q != p:
            break
        time.sleep(0.2)
    assert q != p, "rs.stepDown() did not move the primary"
    print(f"[waited for the election after the step-down: the primary is now 127.0.0.1:{q}]\n")
    out = printed(show(cut(SRC, "// Watch: an election starts"), q, "the new primary"))
    assert "Uncaught" not in out, "a command in sections 5 and 6 failed"
    members = shell("rs.status().members.map(m => m.name.split(':')[1] + ' ' + m.stateStr).join(', ')", q)
    print(f"[rs.status() at the end: {members}]")
    assert "27020 ARBITER" in members, members
    print(f"checked: one PRIMARY and two SECONDARY members; Asha replicated to the secondary,"
          f" which read her with the read preference 'primary'; after rs.stepDown() the"
          f" primary moved from {p} to {q}; the reconfiguration and the arbiter were accepted")

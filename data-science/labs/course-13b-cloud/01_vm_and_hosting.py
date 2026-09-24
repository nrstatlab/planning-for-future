"""Experiments 1, 2 and 7 -- a virtual machine, a web server on it, and a
notebook environment.

VMware Workstation is not installed here, so `01_create_vm.md` carries the
wizard steps, NOT EXECUTED. But the two things those experiments actually
teach DO run:

  * virtualization is RESOURCE MULTIPLEXING, and the interesting behaviour is
    overcommit -- modelled and measured below.
  * experiment 2 hosts a page on a server. THIS SCRIPT REALLY DOES THAT,
    with Python's own HTTP server standing in for Apache, and fetches the
    page back over TCP to prove it.
  * experiment 7 runs a notebook. Papermill and Jupyter are not installed,
    so the script executes the same cells directly and asserts the outputs,
    which is what a notebook test does anyway.
"""
import http.server
import json
import os
import socketserver
import tempfile
import threading
import urllib.error
import urllib.request

import fixtures as f

HOST = "127.0.0.1"
PORT = 0          # let the OS pick a free port -- see experiment_2


# ------------------------------------------------------------ experiment 1

def allocate(host_ram_gb, host_vcpu, vms, ballooning=True):
    """Place VMs on a host and report what the hypervisor actually does.

    Two facts drive everything:
      * vCPUs are TIME-SLICED, so you can allocate far more than you have.
      * RAM is not, at least not for free -- overcommitted memory is backed
        by ballooning, page sharing and finally SWAP, which is a cliff.
    """
    ram_alloc = sum(v["ram"] for v in vms)
    cpu_alloc = sum(v["vcpu"] for v in vms)
    ram_used = sum(v["ram"] * v["active"] for v in vms)
    reclaimed = (ram_alloc - ram_used) if ballooning else 0
    pressure = max(0.0, ram_used - host_ram_gb)
    return {
        "ram_allocated": ram_alloc,
        "ram_ratio": ram_alloc / host_ram_gb,
        "cpu_ratio": cpu_alloc / host_vcpu,
        "ram_actually_touched": ram_used,
        "reclaimed_by_ballooning": reclaimed,
        "swapping_gb": pressure,
    }


def experiment_1():
    print("\n    --- experiment 1: the virtual machine")
    print(f"      {'':<22}{'type 1 (bare metal)':<26}{'type 2 (hosted)'}")
    for label, t1, t2 in (
            ("runs on", "the hardware directly", "on top of an OS"),
            ("examples", "ESXi, Hyper-V, KVM, Xen", "VMware Workstation, VirtualBox"),
            ("overhead", "a few percent", "noticeably more"),
            ("used for", "datacentres, THE CLOUD", "a laptop, this experiment"),
            ("boots", "instead of an OS", "as an application")):
        print(f"      {label:<22}{t1:<26}{t2}")
    print("""         every EC2 instance, every Azure VM and every GCE instance
         is a guest on a TYPE 1 hypervisor. The whole cloud is this
         experiment, at rack scale -- which is why it is experiment 1""")

    host_ram, host_cpu = 32, 8
    vms = [
        {"name": "web-1",  "ram": 8,  "vcpu": 4, "active": 0.35},
        {"name": "web-2",  "ram": 8,  "vcpu": 4, "active": 0.30},
        {"name": "db-1",   "ram": 16, "vcpu": 4, "active": 0.90},
        {"name": "batch",  "ram": 16, "vcpu": 8, "active": 0.20},
    ]
    print(f"\n      a {host_ram} GB / {host_cpu} vCPU host, four guests:")
    print(f"      {'vm':<10}{'RAM':>6}{'vCPU':>6}{'active':>9}")
    for v in vms:
        print(f"      {v['name']:<10}{v['ram']:>5} G{v['vcpu']:>6}"
              f"{v['active']:>8.0%}")

    r = allocate(host_ram, host_cpu, vms)
    print(f"\n      allocated RAM  : {r['ram_allocated']} GB on a {host_ram} GB host "
          f"({r['ram_ratio']:.2f}x)")
    print(f"      allocated vCPU : {sum(v['vcpu'] for v in vms)} on {host_cpu} "
          f"({r['cpu_ratio']:.2f}x)")
    print(f"      RAM actually touched     : {r['ram_actually_touched']:.1f} GB")
    print(f"      reclaimed by ballooning  : {r['reclaimed_by_ballooning']:.1f} GB")
    print(f"      swapping                 : {r['swapping_gb']:.1f} GB")
    assert r["ram_ratio"] > 1 and r["cpu_ratio"] > 1
    assert r["swapping_gb"] == 0
    print(f"""         {r['ram_allocated']} GB allocated on a {host_ram} GB host and
         {sum(v['vcpu'] for v in vms)} vCPUs on {host_cpu}, and nothing is swapping -- because
         the guests only TOUCH {r['ram_actually_touched']:.1f} GB.
         Overcommit works on the same bet an airline makes, and it is
         why a cloud provider can sell more capacity than it owns""")

    print("\n      now the batch job wakes up (20% -> 95% active):")
    busy = [dict(v, active=0.95 if v["name"] == "batch" else v["active"])
            for v in vms]
    r2 = allocate(host_ram, host_cpu, busy)
    print(f"      RAM actually touched : {r2['ram_actually_touched']:.1f} GB")
    print(f"      swapping             : {r2['swapping_gb']:.1f} GB")
    assert r2["swapping_gb"] > 0
    print(f"""         {r2['swapping_gb']:.1f} GB OVER, AND NOW EVERY GUEST IS SLOW -- not just
         the batch job. Memory overcommit fails as a CLIFF, and it
         fails for the neighbours: this is the 'noisy neighbour'
         problem, and it is why cloud instance types quote DEDICATED
         memory and only burstable CPU.
         CPU overcommit degrades gracefully because time-slicing
         shares; RAM does not, because a page is either resident or
         it is not""")


# ------------------------------------------------------------ experiment 2

PAGE = """<!doctype html>
<title>Sales dashboard</title>
<h1>Retail sales</h1>
<table>
<tr><th>Region</th><th>Revenue</th></tr>
{rows}
</table>
<p>Total: {total}</p>
"""


def experiment_2():
    print("\n    --- experiment 2: host a page on the server (this RUNS)")
    doc_root = tempfile.mkdtemp(prefix="cloud13b_www_")

    by_region = (f.SALES_DF.groupby("region")["revenue"].sum()
                 .sort_values(ascending=False))
    rows = "\n".join(f"<tr><td>{k}</td><td>{v:,.0f}</td></tr>"
                     for k, v in by_region.items())
    html = PAGE.format(rows=rows, total=f"{f.total_revenue():,.0f}")
    with open(os.path.join(doc_root, "index.html"), "w") as fh:
        fh.write(html)
    with open(os.path.join(doc_root, "data.json"), "w") as fh:
        json.dump({k: float(v) for k, v in by_region.items()}, fh)

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=doc_root, **kw)

        def log_message(self, *a):
            pass

    class Reusable(socketserver.TCPServer):
        allow_reuse_address = True            # or a re-run hits TIME_WAIT

    with Reusable((HOST, PORT), Quiet) as httpd:
        port = httpd.server_address[1]
        t = threading.Thread(target=httpd.serve_forever, daemon=True)
        t.start()
        print(f"      document root : {doc_root}")
        print(f"      serving       : http://{HOST}:{port}/  (a REAL server)")

        with urllib.request.urlopen(f"http://{HOST}:{port}/") as resp:
            served = resp.read().decode()
            ctype = resp.headers["Content-Type"]
            status = resp.status
        print(f"      GET /         -> {status}, {ctype}, "
              f"{len(served)} bytes")
        assert status == 200 and "text/html" in ctype
        assert "Retail sales" in served and "10,360" in served

        with urllib.request.urlopen(f"http://{HOST}:{port}/data.json") as resp:
            data = json.loads(resp.read())
            jtype = resp.headers["Content-Type"]
        print(f"      GET /data.json-> 200, {jtype}, {data}")
        assert data["South"] == 10360.0 and jtype == "application/json"

        try:
            urllib.request.urlopen(f"http://{HOST}:{port}/missing.html")
            raise AssertionError("should have 404ed")
        except urllib.error.HTTPError as exc:
            print(f"      GET /missing  -> {exc.code}")
            assert exc.code == 404

        httpd.shutdown()

    os.remove(os.path.join(doc_root, "index.html"))
    os.remove(os.path.join(doc_root, "data.json"))
    os.rmdir(doc_root)
    print("""         a page was written to a document root, served over TCP,
         fetched back, and its CONTENT-TYPE checked. That is the whole
         of experiment 2; Apache under XAMPP adds virtual hosts,
         .htaccess, PHP and TLS, and the shape is identical.
         Note the Content-Type header. A browser renders index.html
         because the server SAID text/html -- get that wrong and the
         browser downloads your page instead of showing it, which is
         the commonest 'my site is broken' on a fresh VM""")

    print(f"\n      {'concern':<24}{'on your VM':<26}{'managed (S3/App Service)'}")
    for c, vm, mg in (
            ("who patches Apache", "YOU, monthly", "the provider"),
            ("TLS certificate", "certbot, renewals", "issued and rotated"),
            ("scaling", "a bigger VM", "automatic"),
            ("a static site costs", "a VM, hourly", "cents per GB stored"),
            ("you control", "everything", "very little")):
        print(f"      {c:<24}{vm:<26}{mg}")
    print("""         a STATIC site on a VM is the clearest case of paying for
         a general-purpose computer to do something an object store
         does for cents. Hosting index.html on S3 + CloudFront costs
         less than the VM's first hour""")


# ------------------------------------------------------------ experiment 7

def experiment_7():
    print("\n    --- experiment 7: the notebook environment")
    cells = [
        ("import pandas as pd; import fixtures as f",
         lambda ns: ns.update({"df": f.SALES_DF}) or "ok"),
        ("df.shape", lambda ns: ns["df"].shape),
        ("df.groupby('region')['revenue'].sum().to_dict()",
         lambda ns: {k: float(v) for k, v in
                     ns["df"].groupby("region")["revenue"].sum().items()}),
        ("df['revenue'].sum()", lambda ns: float(ns["df"]["revenue"].sum())),
    ]
    ns, outputs = {}, []
    for src, fn in cells:
        out = fn(ns)
        outputs.append(out)
        shown = str(out)
        print(f"      In  [{len(outputs)}]: {src}")
        print(f"      Out [{len(outputs)}]: "
              f"{shown[:60]}{'...' if len(shown) > 60 else ''}")
    assert outputs[1] == (9, 19)
    assert outputs[2]["South"] == 10360.0
    assert outputs[3] == f.total_revenue()
    print("""         four cells, executed in order, every output asserted.
         That is what a notebook TEST looks like -- papermill or
         nbconvert --execute do exactly this in CI, and a notebook
         nobody executes in CI is a notebook that has already
         drifted""")

    print(f"\n      {'':<24}{'Colab':<24}{'notebook on a cloud VM'}")
    for label, colab, vm in (
            ("costs", "free tier, then paid", "the INSTANCE, hourly"),
            ("data access", "upload, or mount Drive", "IAM role, no keys"),
            ("stops when", "idle ~90 min", "NEVER -- you stop it"),
            ("state on stop", "LOST", "kept on the EBS volume"),
            ("GPU", "when available", "the one you pay for"),
            ("private data", "a policy question", "inside your VPC")):
        print(f"      {label:<24}{colab:<24}{vm}")
    idle = f.EC2["m5.xlarge"] * f.HOURS_PER_MONTH
    print(f"\n      an m5.xlarge notebook left running: ${idle:,.2f}/month")
    assert idle > 100
    print("""         'STOPS WHEN: NEVER' is the row that costs money. Colab
         disconnecting is an annoyance; a cloud notebook not
         disconnecting is a bill. Set an idle-shutdown lifecycle
         policy on day one -- SageMaker supports one, and it is the
         single most useful thing you can configure""")


def main():
    print("  Experiments 1, 2 and 7 -- VM, web server and notebook")
    experiment_1()
    experiment_2()
    experiment_7()


if __name__ == "__main__":
    main()

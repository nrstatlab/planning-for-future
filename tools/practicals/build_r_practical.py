#!/usr/bin/env python3
"""Write a practical page in the programming structure from a data module, running its R.

    python3 tools/practicals/build_r_practical.py dh_data           # rewrite the page and images
    python3 tools/practicals/build_r_practical.py dh_data --check   # rerun R; fail if the page differs

The data module gives PAGE (path from the repository root), TITLE, DESC, HEAD (the HTML from
<div class="wrapper"> up to the first practical; "{toc}" is replaced by the contents list and
"{version}" by the R version), PRACTICALS (as in csr2023_data.py), optional INTERLUDES
({number: HTML placed after that practical}) and TAIL (the HTML after the last practical, up
to and including the wrapper's closing </div>). Each practical's R runs in its own session,
through the driver and renderer of build_csr2023_practical.py, so every output and plot is
R's own: 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and Results.

It needs R, so it is not part of tools/build_all.sh; its output is committed.
"""
import html
import importlib
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_csr2023_practical as B  # noqa: E402

H2 = re.compile(r'<h2 id="([^"]+)">(.*?)</h2>', re.S)


def toc_of(html_text):
    return "\n".join(f'    <li><a href="#{i}">{re.sub(r"<[^>]+>", "", t)}</a></li>'
                     for i, t in H2.findall(html_text))


def build(D, img_dir):
    if not shutil.which("Rscript"):
        sys.exit("Rscript was not found: this script needs R")
    version = subprocess.run(["Rscript", "-e", "cat(paste(R.version$major, R.version$minor, sep='.'))"],
                             capture_output=True, text=True, check=True).stdout.strip()
    img_dir.mkdir(parents=True, exist_ok=True)
    parts = []
    with tempfile.TemporaryDirectory() as tmp:
        for p in D.PRACTICALS:
            _, body = B.render_practical(p, B.run_practical(p, img_dir, pathlib.Path(tmp)))
            parts.append(body)
            if p["n"] in getattr(D, "INTERLUDES", {}):
                parts.append(D.INTERLUDES[p["n"]])
    rest = "\n".join(parts) + "\n" + D.TAIL
    head = D.HEAD.replace("{version}", version)
    body = head.replace("{toc}", toc_of(head + rest)) + rest
    return body, version


def main():
    D = importlib.import_module(sys.argv[1])
    page_path = B.ROOT / D.PAGE
    img = page_path.parent / "img"
    page = page_path.read_text()
    if "--check" in sys.argv[2:]:
        with tempfile.TemporaryDirectory() as tmp:
            body, version = build(D, pathlib.Path(tmp))
        bad = [] if B.BODY.search(page).group(0) == body else [f"{D.PAGE}: the content differs from a fresh R run"]
        bad += [f"img/{n} is missing" for n in B.images(body) if not (img / n).exists()]
        if bad:
            print("FAIL\n  " + "\n  ".join(bad))
            return 1
        print(f"{D.PAGE} matches a fresh run in R {version}; {len(B.images(body))} images present")
        return 0
    body, version = build(D, img)
    B.TITLE, B.DESC = D.TITLE, html.unescape(D.DESC)
    page_path.write_text(B.splice(page, body))
    print(f"wrote {D.PAGE} and {len(B.images(body))} images (R {version})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Page shell for the ISS syllabus map, matching statistics-papers/csir-net/."""
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="NRSTATLAB">
<meta name="twitter:card" content="summary">
<style>
  * {{ box-sizing: border-box; }}
  body {{ font-family:"Segoe UI","Helvetica Neue",Arial,sans-serif; margin:0;
         background:#f5f7fb; color:#1f2937; line-height:1.6; }}
  .wrapper {{ max-width:1100px; margin:0 auto; padding:28px 22px 80px; }}
  .banner {{ background:linear-gradient(135deg,#0f4c81 0%,#1e7fbf 100%); color:#fff;
            padding:34px 24px; border-radius:14px;
            box-shadow:0 6px 20px rgba(15,76,129,.18); margin-bottom:30px; }}
  .banner h1 {{ margin:0 0 6px; font-size:1.85rem; }}
  .banner p {{ margin:0; opacity:.95; }}
  h2 {{ color:#0f4c81; border-bottom:3px solid #1e7fbf; padding-bottom:6px; margin-top:42px; }}
  h3 {{ color:#0f4c81; margin-top:28px; }}
  .lede {{ font-size:1.02rem; }}
  .quote {{ background:#fff; border-left:5px solid #0f4c81; border-radius:10px;
           padding:16px 22px; margin:18px 0; box-shadow:0 2px 10px rgba(0,0,0,.06); }}
  .quote p {{ margin:0 0 8px; }}
  .quote p:last-child {{ margin:0; }}
  .quote cite {{ font-size:.85rem; color:#6b7280; font-style:normal; }}
  .note {{ background:#fffbeb; border:1px solid #fde68a; border-left:5px solid #f59e0b;
          border-radius:10px; padding:16px 20px; margin:20px 0; }}
  .note strong {{ color:#92400e; }}
  .gaps {{ background:#fef2f2; border:1px solid #fecaca; border-left:5px solid #dc2626;
          border-radius:10px; padding:4px 22px 16px; margin:20px 0; }}
  .gaps strong {{ color:#991b1b; }}
  .scroll {{ overflow-x:auto; border-radius:10px; box-shadow:0 2px 10px rgba(0,0,0,.06);
            margin:16px 0; background:#fff; }}
  table {{ border-collapse:collapse; width:100%; min-width:620px; }}
  th, td {{ text-align:left; padding:10px 14px; border-bottom:1px solid #e2e8f0;
           font-size:.92rem; vertical-align:top; }}
  th {{ background:#eef4fa; color:#0f4c81; }}
  tr:last-child td {{ border-bottom:none; }}
  td:first-child {{ width:44%; }}
  .g {{ display:inline-block; font-size:.72rem; font-weight:700; letter-spacing:.04em;
       padding:2px 9px; border-radius:10px; white-space:nowrap; }}
  .g.deep {{ background:#d1fae5; color:#065f46; }}
  .g.brief {{ background:#fef3c7; color:#92400e; }}
  .g.missing {{ background:#fee2e2; color:#991b1b; }}
  .none {{ color:#991b1b; font-size:.88rem; }}
  .tally {{ display:flex; gap:10px; flex-wrap:wrap; margin:14px 0 0; padding:0; list-style:none; }}
  .tally li {{ background:#fff; border:1px solid #e2e8f0; border-radius:10px;
              padding:10px 16px; font-size:.9rem; }}
  .tally b {{ display:block; font-size:1.3rem; color:#0f4c81; }}
  .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
           gap:16px; margin:20px 0; }}
  .card {{ background:#fff; border-radius:12px; padding:20px; text-decoration:none;
          color:inherit; border-top:4px solid #1e7fbf;
          box-shadow:0 2px 10px rgba(0,0,0,.06); transition:transform .15s ease; }}
  .card:hover {{ transform:translateY(-3px); }}
  .card h3 {{ margin:0 0 8px; font-size:1.08rem; }}
  .card p {{ margin:0; font-size:.9rem; color:#4b5563; }}
  a {{ color:#0f4c81; }}
  footer {{ text-align:center; margin-top:46px; font-size:.85rem; color:#6b7280; }}
  @media (max-width:760px) {{ .banner h1 {{ font-size:1.4rem; }} td:first-child {{ width:auto; }} }}
</style>
<style>
.nrstatlab-bar{{background:#0f4c81;color:#fff;font-family:"Segoe UI","Helvetica Neue",Arial,sans-serif;font-size:.9rem;line-height:1.5;padding:10px 22px;margin:0}}
.nrstatlab-bar .nrstatlab-inner{{max-width:1100px;margin:0 auto;display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.nrstatlab-bar a.nrstatlab-brand{{color:#fff;font-weight:700;letter-spacing:.09em;text-decoration:none;border-bottom:2px solid rgba(255,255,255,.45);padding-bottom:1px}}
.nrstatlab-bar a.nrstatlab-brand:hover{{border-bottom-color:#fff}}
.nrstatlab-bar .nrstatlab-sep{{opacity:.55}}
.nrstatlab-bar .nrstatlab-here{{opacity:.95}}
.nrstatlab-bar a.nrstatlab-topics{{color:#fff;text-decoration:none;font-weight:600;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.32);border-radius:6px;padding:2px 10px;white-space:nowrap}}
.nrstatlab-bar a.nrstatlab-topics:hover{{background:rgba(255,255,255,.3)}}
</style>
</head>
<body>
<div class="nrstatlab-bar"><div class="nrstatlab-inner"><a class="nrstatlab-brand" href="{root}">NRSTATLAB</a><span class="nrstatlab-sep">&rsaquo;</span><a href="{up}" style="color:#fff">Examinations</a><span class="nrstatlab-sep">&rsaquo;</span><span class="nrstatlab-here">{crumb}</span><a class="nrstatlab-topics" href="{root}topics.html">Topics A&ndash;Z</a></div></div>

<div class="wrapper">

  <div class="banner">
    <h1>{h1}</h1>
    <p>{sub}</p>
  </div>
"""

TAIL = """
  <p><a href="{back}">&larr; {backlabel}</a></p>

  <footer>
    <p>{footer} &middot; <a href="{root}">NRSTATLAB</a></p>
  </footer>
</div>
</body>
</html>
"""


def page(path, *, title, desc, crumb, h1, sub, body, back, backlabel, footer,
         root="../../", up="../"):
    out = HEAD.format(title=title, desc=desc, crumb=crumb, h1=h1, sub=sub,
                      root=root, up=up)
    out += body
    out += TAIL.format(back=back, backlabel=backlabel, footer=footer, root=root)
    import pathlib
    pathlib.Path(path).write_text(out, encoding="utf-8")

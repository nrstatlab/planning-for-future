#!/usr/bin/env bash
# Rebuild everything generated, in the one order that converges.
#
#     bash tools/build_all.sh
#
# The order matters in both directions (docs/ARCHITECTURE.md §6): the
# generators rewrite whole pages, so the shared chrome goes on after them;
# the topic index rewrites topics.html whole, so the chrome goes on after it
# too; and the search index and sitemap read the finished pages, so they come
# after the chrome. Running this twice must leave the tree byte-identical
# (compare `git add -A && git write-tree` before and after) -- if it does not,
# the order has been broken.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 tools/data-science/build_site.py >/dev/null
( cd tools/exams
  python3 iss_map.py          >/dev/null
  python3 appsc_map.py        >/dev/null
  python3 gen_csir.py         >/dev/null
  python3 asrb_map.py --apply >/dev/null
  python3 ugc_map.py  --apply >/dev/null
  python3 appsc_paper.py --apply >/dev/null )
python3 tools/course_catalogue.py   >/dev/null
python3 tools/build_course_hubs.py  --apply
python3 tools/build_exam_courses.py --apply | tail -1
python3 tools/build_progress_index.py --apply | tail -1
python3 tools/build_dark_theme.py   --apply | tail -1
python3 tools/build_topic_index.py  --apply | tail -1
python3 tools/add_site_nav.py       --apply | head -1
python3 tools/build_search_index.py --apply | tail -1
python3 tools/build_sitemap.py      --apply | tail -1
python3 tools/check_canonical.py    --apply | head -1
python3 tools/check_home_stats.py   --fix   | tail -1
python3 tools/check_catalogue.py
python3 tools/check_published.py

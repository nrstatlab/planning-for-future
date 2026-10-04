"""Opens 08_responsive.html in Chromium at three widths, and reads the layout at each.

Run by tools/data-science/capture_lab_outputs.py, through tools/data-science/web_lab.py.
"""
from web_lab import open_page

LAYOUT = """() => {
  const page = getComputedStyle(document.querySelector('.page'));
  const tops = [...document.querySelectorAll('.card')].map(c => c.offsetTop);
  const aside = document.querySelector('aside').getBoundingClientRect();
  const main = document.querySelector('main').getBoundingClientRect();
  return { columns: page.gridTemplateColumns,
           perRow: tops.filter(t => t === tops[0]).length, cards: tops.length,
           aside: aside.top >= main.bottom ? 'below the content' : 'beside the content' };
}"""

for width in (390, 800, 1200):
    with open_page("08_responsive.html", width=width, height=900) as p:
        L = p.evaluate(LAYOUT)
        print(f"  page grid columns: {L['columns']}")
        print(f"  cards: {L['perRow']} in the first row, of {L['cards']}; the sidebar is {L['aside']}")
        p.screenshot(f"{width} px wide", full_page=True)
        if width == 390:
            assert L["aside"] == "below the content" and L["perRow"] == 1
        if width == 1200:
            assert L["aside"] == "beside the content" and L["perRow"] > 1

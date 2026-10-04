"""Drives 09_hover.html in Chromium: hovers over each effect, and reads what changed.

Run by tools/data-science/capture_lab_outputs.py, through tools/data-science/web_lab.py. Each
reading is the computed style after the transition has finished.
"""
from web_lab import open_page


def style(p, selector, prop):
    return p.evaluate(f"getComputedStyle(document.querySelector('{selector}')).{prop}")


with open_page("09_hover.html", height=760) as p:
    before = style(p, ".btn", "transform")
    p.hover(".btn")
    p.wait_for_timeout(500)
    print(f"button:  transform {before} -> {style(p, '.btn', 'transform')}  (lifted 2 px)")
    p.screenshot("hovering over the first button")

    img = ".thumb img"
    before = style(p, img, "filter"), style(p, img, "transform")
    p.hover(".thumb")
    p.wait_for_timeout(600)
    after = style(p, img, "filter"), style(p, img, "transform")
    print(f"image:   filter {before[0]} -> {after[0]}, transform {before[1]} -> {after[1]}")
    p.screenshot("hovering over the first image")

    cap = ".card .caption"
    before = style(p, cap, "transform")
    p.hover(".card")
    p.wait_for_timeout(500)
    print(f"caption: transform {before} -> {style(p, cap, 'transform')}  (slid up into view)")
    p.screenshot("hovering over the first card")

    p.hover(".tip")
    p.wait_for_timeout(400)
    tip = p.evaluate("getComputedStyle(document.querySelector('.tip'), '::after').opacity")
    print(f"tooltip: opacity of its ::after is {tip}")
    assert tip == "1"
    p.screenshot("hovering over the tooltip")

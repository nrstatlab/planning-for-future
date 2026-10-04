"""Drives 16_jquery.html in Chromium: presses each button, and reads what jQuery did.

Run by tools/data-science/capture_lab_outputs.py, through tools/data-science/web_lab.py, which
serves jQuery 3.7.1 from npm's copy in place of code.jquery.com (unreachable from here); the
page's integrity attribute has the browser check that the copy is the same file.
"""
from web_lab import open_page


def settle(p):
    """Wait until jQuery has no animation running, nor the stylesheet a transition: a fixed
    wait reads some of them mid-way."""
    p.wait_for_timeout(50)
    p.wait_for_function("jQuery(':animated').length === 0 && document.getAnimations().length === 0")


def panel(p):
    return p.evaluate("""() => { const s = getComputedStyle(document.getElementById('panel'));
        return s.display === 'none' ? 'hidden' : 'shown, opacity ' + s.opacity; }""")


with open_page("16_jquery.html", height=760, clock=None) as p:     # animations need a clock that moves
    version = p.evaluate("window.jQuery ? jQuery.fn.jquery : null")
    print(f"jQuery loaded: {version}  (so the jQuery version of the page is the one running)")
    assert version == "3.7.1"
    for button in ("hide", "show", "fade", "fade", "slide", "slide", "toggle", "toggle"):
        p.click(f"#{button}")
        settle(p)
        print(f"  {button:<7} -> the panel is {panel(p)}")
    p.click("#animate")
    settle(p)
    box = p.evaluate("[document.getElementById('box').style.left, document.getElementById('box').className]")
    print(f"  animate -> the box is at left {box[0]}, class {box[1]!r}")
    p.screenshot("after animate()", full_page=True)
    p.click("#ok")
    settle(p)
    print(f"  ok      -> the message reads {p.text('#msg')!r}, class {p.get_attribute('#msg', 'class')!r}")
    rows = lambda: p.evaluate("document.querySelectorAll('#tbody tr').length")
    before = rows()
    p.click("#addrow")
    p.wait_for_timeout(300)
    added = rows()
    p.click("#tbody tr:last-child .delete-btn")
    settle(p)
    print(f"  rows: {before}, {added} after Add row, {rows()} after deleting the new one"
          " -- delegation works for a row added later")
    assert added == before + 1 and rows() == before
    p.screenshot("after the rows", full_page=True)

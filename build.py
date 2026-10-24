"""Builds index.html from template.html and the register values below.

Every number comes from docs/hypotheses/README.md in the NQX repo (stressed t-statistic where the
register records one; plain t for H1 and H11). Run: python build.py
"""
import json
from pathlib import Path

GATE = 2.5
# id, idea, t, note, dsr (None when not recorded)
POINTS = [
    ("H1", "Intraday momentum, US100", -4.3, "All four variants negative. Holdout not opened.", None),
    ("H3", "30-minute opening-range breakout", 1.04, "+0.084 R before the stress. PBO 0.77.", 0.06),
    ("H4", "Midday reversion to TWAP", -4.29, "All variants negative.", 0.00),
    ("H5", "Regime-based strategy selection", 1.15, "102 trades, below the 500 minimum.", 0.44),
    ("H6", "ML strategy selection", 0.16, "Worse than always running the best single rule.", 0.006),
    ("H7", "Cross-asset trend, daily", -0.11, "Gross edge about half eaten by swap.", None),
    ("H7b", "Cross-asset trend, fill time fixed", -0.81, "Gross +9.8%, mostly eaten by swap.", 0.20),
    ("H8", "Overnight drift in index CFDs", -4.1, "+0.13 R gross, -0.032 R after swap and spread.", None),
    ("H9", "US30 opening-range breakout", 0.43, "Does not replicate the H3 result.", None),
    ("H10", "Hourly Donchian, multi-asset", -3.9, "Gross +0.07 R eaten by spread and swap.", None),
    ("H11", "Hourly Donchian, 27 unseen FX pairs", -14.0, "-0.124 R over 32,594 trades. Plain t, off the chart.", None),
    ("H12", "Trend on 30+ years of daily data", 0.57, "Net t 2.72, but the edge decays from Sharpe 1.3 to 0.06.", None),
    ("H13", "Canonical 12-month trend", 2.10, "Needs 2.5. DSR 0.12.", 0.12),
    ("H14", "Trend across 20 markets", 2.86, "Crosses the gate. Fails Deflated Sharpe after 48 trials.", 0.29),
    ("H15", "G10 FX carry", 2.50, "Crosses the gate. Fails Deflated Sharpe.", 0.18),
    ("H16", "Trend plus carry, equal risk", 3.79, "Closest of all. One losing block. Forward test running.", 0.56),
    ("F1", "Gold expert advisor, out of sample", -2.47, "Hit its own loss stop in 2022.", None),
    ("F3", "Gold high at least $1 above the open", -1.85, "The fact was true on 96.87% of days. The trade lost.", 0.053),
    ("H19", "Gold Asian-session drift", 0.15, "Positive drift, fails the gate.", 0.11),
    ("H20", "Gold rebound after a London decline", -1.48, "No rebound found.", 0.0003),
    ("H21", "ML intraday reversal entry", -0.66, "Upper bound; 24,206 candidates.", None),
]

W, H = 1000, 400
X0, X1 = 56, 960
TMIN, TMAX = -5.6, 4.6
R = 15
BASE = 218


def x(t):
    t = max(t, -5.2)
    return X0 + (t - TMIN) / (TMAX - TMIN) * (X1 - X0)


placed = []
shapes = []
for i, (pid, idea, t, note, dsr) in enumerate(sorted(POINTS, key=lambda p: p[2])):
    cx = x(t)
    for k in range(0, 14):
        off = ((k + 1) // 2) * (2 * R + 3) * (1 if k % 2 else -1)
        cy = BASE + off
        if all((cx - px) ** 2 + (cy - py) ** 2 >= (2 * R + 2) ** 2 for px, py in placed):
            break
    placed.append((cx, cy))
    crossed = t >= GATE
    cls = "dot crossed" if crossed else "dot"
    shapes.append(
        f'<g class="{cls}" tabindex="0" role="button" data-id="{pid}" style="--i:{i}" '
        f'aria-label="{pid}, {idea}, t {t:g}">'
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R}"/><text x="{cx:.1f}" y="{cy + 3.5:.1f}">{pid}</text>'
        f'<title>{pid}: {idea} (t {t:g})</title></g>'
    )

ticks = "".join(
    f'<g><line class="tick" x1="{x(v):.1f}" x2="{x(v):.1f}" y1="60" y2="352"/>'
    f'<text class="axis" x="{x(v):.1f}" y="378" text-anchor="middle">{v:+d}</text></g>'.replace("+0", "0")
    for v in range(-5, 5)
)
gx = x(GATE)
chart = f"""<svg class="plot" viewBox="0 0 {W} {H}" role="group" aria-label="Strip plot of stressed t-statistics for {len(POINTS)} hypotheses">
<rect class="zone" x="{gx:.1f}" y="40" width="{X1 - gx + 20:.1f}" height="312"/>
{ticks}
<line class="gate" x1="{gx:.1f}" x2="{gx:.1f}" y1="40" y2="352"/>
<text class="gate-label" x="{gx + 10:.1f}" y="62">gate: stressed t &#8805; 2.5</text>
<text class="side-label" x="{X0}" y="34">&#8592; costs eat it</text>
<text class="axis-title" x="{(X0 + X1) / 2:.0f}" y="398" text-anchor="middle">stressed t-statistic (plain t for H1, H11)</text>
{''.join(shapes)}
</svg>"""

data = {pid: dict(idea=idea, t=t, note=note, dsr=dsr, crossed=t >= GATE) for pid, idea, t, note, dsr in POINTS}
crossed = [p[0] for p in POINTS if p[2] >= GATE]

here = Path(__file__).parent
html = (here / "template.html").read_text(encoding="utf-8")
html = (html.replace("{{CHART}}", chart)
            .replace("{{DATA}}", json.dumps(data, ensure_ascii=False))
            .replace("{{N}}", str(len(POINTS)))
            .replace("{{CROSSED}}", str(len(crossed))))
(here / "index.html").write_text(html, encoding="utf-8", newline="\n")
print(f"{len(POINTS)} points, crossed gate: {', '.join(crossed)}")

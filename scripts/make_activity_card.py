"""Generates assets/activity.svg: last-12-months contributions, styled to sit beside the streak-stats card."""
import json
import os
import sys
import urllib.request
from datetime import date

OUT = sys.argv[1]
USER = "BaldSalad"

W, H = 495, 195
BG, BLUE, DEEP, TEXT, MUTED, LINE = "#0D1117", "#58A6FF", "#1F6FEB", "#FEFEFE", "#9E9E9E", "#E4E2E2"
FONT = '"Segoe UI", Ubuntu, sans-serif'

# Weekly bar chart area (right of the divider).
CX0, CX1 = 186, 474
CY0, CY1 = 50, 148

QUERY = """query($login: String!) { user(login: $login) { contributionsCollection { contributionCalendar {
  totalContributions weeks { contributionDays { date contributionCount } } } } } }"""

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
    headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
)
cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]

weeks = [[(date.fromisoformat(d["date"]), d["contributionCount"]) for d in w["contributionDays"]] for w in cal["weeks"]]
days = [d for w in weeks for d in w]
totals = [sum(c for _, c in w) for w in weeks]
total = cal["totalContributions"]
active = sum(1 for _, c in days if c)
peak = max(totals) or 1
first, last = days[0][0], days[-1][0]

out = []
add = out.append
add(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" direction="ltr">
<style>
  text {{ font-family: {FONT}; }}
  @keyframes fadein {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
  @keyframes grow {{ from {{ transform: scaleY(0); }} to {{ transform: scaleY(1); }} }}
  .f {{ opacity: 0; animation: fadein .5s linear forwards; }}
  .b {{ transform-box: fill-box; transform-origin: bottom; transform: scaleY(0); animation: grow .5s ease-out forwards; }}
</style>
<clipPath id="outer"><rect width="{W}" height="{H}" rx="4.5"/></clipPath>
<g clip-path="url(#outer)">
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="4.5" fill="{BG}"/>
<line x1="165" y1="28" x2="165" y2="170" stroke="{LINE}" stroke-width="1"/>
''')

# Left column: mirrors the streak card's "Total Contributions" column.
add(f'''<text class="f" style="animation-delay:.6s" x="82.5" y="80" text-anchor="middle" fill="{BLUE}" font-weight="700" font-size="28px">{total:,}</text>
<text class="f" style="animation-delay:.7s" x="82.5" y="116" text-anchor="middle" fill="{TEXT}" font-size="14px">Contributions</text>
<text class="f" style="animation-delay:.8s" x="82.5" y="146" text-anchor="middle" fill="{MUTED}" font-size="12px">{first:%b %Y} - {last:%b %Y}</text>
''')

# Right column: header, weekly bars, month labels.
add(f'''<text class="f" style="animation-delay:.6s" x="{CX0}" y="34" fill="{TEXT}" font-size="14px">Weekly activity</text>
<text class="f" style="animation-delay:.6s" x="{CX1}" y="34" text-anchor="end" fill="{MUTED}" font-size="12px">{active} active days</text>
<line x1="{CX0}" y1="{CY1 + .5}" x2="{CX1}" y2="{CY1 + .5}" stroke="{LINE}" stroke-opacity=".25"/>
''')
step = (CX1 - CX0) / len(weeks)
bw = step * .7
for i, t in enumerate(totals):
    x = CX0 + i * step + (step - bw) / 2
    h = max(2, (CY1 - CY0) * t / peak) if t else 2
    colour, opacity = (BLUE, .35 + .65 * t / peak) if t else (DEEP, .35)
    add(f'<rect class="b" style="animation-delay:{.6 + i * .012:.3f}s" x="{x:.2f}" y="{CY1 - h:.2f}" width="{bw:.2f}" '
        f'height="{h:.2f}" rx="1" fill="{colour}" fill-opacity="{opacity:.2f}"/>\n')

seen = set()
for i, w in enumerate(weeks):
    d = w[0][0]
    if d.day <= 7 and d.month % 2 == 1 and d.month not in seen and 2 <= i <= len(weeks) - 3:
        seen.add(d.month)
        add(f'<text class="f" style="animation-delay:.9s" x="{CX0 + (i + .5) * step:.1f}" y="168" text-anchor="middle" '
            f'fill="{MUTED}" font-size="11px">{d:%b}</text>\n')

add('</g>\n</svg>\n')

open(OUT, "w", encoding="utf-8").write("".join(out))
print(f"{total} contributions, {active} active days, {len(weeks)} weeks -> {OUT}")

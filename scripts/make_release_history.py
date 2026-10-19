"""Generates assets/release-history.svg: career as a deployment pipeline."""
import sys

OUT = sys.argv[1]

W, H = 1000, 312
CARD_W, GAP, X0 = 180, 12, 26
CARD_Y, CARD_H = 96, 136
TRACK_Y = 266

AMBER, BLUE, PURPLE, GREEN = "#D29922", "#58A6FF", "#A371F7", "#3FB950"
TEXT, MUTED, DIM, LINE, CARD = "#E6EDF3", "#8B949E", "#6E7681", "#30363d", "#161b22"

ROLES = [
    ("v1.0", "Apprentice Electrician", "ENRG Electrical Services", "JUL 2018", "FEB 2020", "shipped", "1y 8m", AMBER, "2018"),
    ("v2.0", "Electrician", "Jascom Electrical", "OCT 2020", "SEP 2022", "shipped", "2y", AMBER, "2020"),
    ("v3.0", "Software Developer", "Harbour Rock Capital", "OCT 2022", "JUL 2025", "shipped", "2y 10m", BLUE, "2022"),
    ("v4.0", "Solutions Engineer", "Apex Infinity Solutions", "JUL 2025", "SEP 2026", "promoted", "1y 3m", BLUE, "2025"),
    ("v5.0", "Delivery Manager", "Apex Infinity Solutions", "OCT 2026", "NOW", "deploying", "", PURPLE, "2026"),
]
ERAS = [("ON THE TOOLS", 0, 1, AMBER), ("IN THE CODE", 2, 3, BLUE), ("LEADING DELIVERY", 4, 4, PURPLE)]

DRAW_START, DRAW_DUR = 0.9, 2.6


def card_x(i):
    return X0 + i * (CARD_W + GAP)


def centre(i):
    return card_x(i) + CARD_W / 2


def appear_at(i):
    return DRAW_START + DRAW_DUR * i / (len(ROLES) - 1)


track_x1, track_x2 = centre(0), centre(len(ROLES) - 1)
track_len = track_x2 - track_x1

out = []
add = out.append
add(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">
<style>
  .m {{ font-family: ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace; }}
  .s {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; }}
</style>
<defs>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#21262d"/></pattern>
  <clipPath id="panel"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  <clipPath id="typing"><rect x="84" y="18" height="26" width="0">
    <animate attributeName="width" from="0" to="260" dur=".8s" begin=".1s" fill="freeze" calcMode="discrete"
      values="{';'.join(str(round(n * 260 / 29)) for n in range(30))}" keyTimes="{';'.join(f'{n / 29:.3f}' for n in range(30))}"/>
  </rect></clipPath>
  <linearGradient id="track" x1="{track_x1}" x2="{track_x2}" gradientUnits="userSpaceOnUse">
    <stop stop-color="{AMBER}"/><stop offset=".3" stop-color="{AMBER}"/><stop offset=".45" stop-color="{BLUE}"/>
    <stop offset=".75" stop-color="{BLUE}"/><stop offset=".92" stop-color="{PURPLE}"/><stop offset="1" stop-color="{PURPLE}"/>
  </linearGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="cardglow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="8"/></filter>
</defs>
<g clip-path="url(#panel)">
<rect width="{W}" height="{H}" fill="#0d1117"/>
<rect width="{W}" height="{H}" fill="url(#dots)"/>
''')

# Terminal header: window dots, typed command, blinking cursor, section label.
add(f'''<circle cx="30" cy="31" r="5" fill="#f85149"/><circle cx="47" cy="31" r="5" fill="{AMBER}"/><circle cx="64" cy="31" r="5" fill="{GREEN}"/>
<text class="m" x="84" y="36" font-size="14" clip-path="url(#typing)"><tspan fill="{GREEN}">josh@apex</tspan><tspan fill="{MUTED}">:~$ </tspan><tspan fill="{TEXT}">git log --career</tspan></text>
<rect x="{84 + 29 * 8.43 + 3:.1f}" y="23" width="8" height="16" fill="{BLUE}" opacity="0">
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" begin=".9s" repeatCount="indefinite"/></rect>
<text class="m" x="{W - 28}" y="36" font-size="11.5" letter-spacing="3" fill="{DIM}" text-anchor="end">RELEASE HISTORY · 2018 → NOW</text>
''')

# Era bands above the cards.
for label, a, b, colour in ERAS:
    x1, x2 = card_x(a), card_x(b) + CARD_W
    begin = appear_at(a) - 0.3
    add(f'''<g opacity="0"><animate attributeName="opacity" to="1" dur=".5s" begin="{begin:.2f}s" fill="freeze"/>
  <path d="M{x1 + 1},84 V78 H{x2 - 1} V84" stroke="{colour}" stroke-opacity=".45" stroke-width="1.5"/>
  <text class="m" x="{x1}" y="68" font-size="11" letter-spacing="2.5" fill="{colour}" font-weight="600">{label}</text>
</g>
''')

# Pipeline track: grey base, gradient draw-in, then a looping deploy packet.
add(f'''<path d="M{track_x1},{TRACK_Y} H{track_x2}" stroke="#21262d" stroke-width="4" stroke-linecap="round"/>
<path d="M{track_x2},{TRACK_Y} H{W - 30}" stroke="{LINE}" stroke-width="2" stroke-dasharray="3 6"/>
<path d="M{track_x1},{TRACK_Y} H{track_x2}" stroke="url(#track)" stroke-width="4" stroke-linecap="round" stroke-dasharray="{track_len}" stroke-dashoffset="{track_len}">
  <animate attributeName="stroke-dashoffset" to="0" dur="{DRAW_DUR}s" begin="{DRAW_START}s" fill="freeze"/></path>
<rect x="-7" y="{TRACK_Y - 3}" width="14" height="6" rx="3" fill="{TEXT}" filter="url(#glow)" opacity="0">
  <animateMotion path="M{track_x1},0 H{track_x2}" dur="3.5s" begin="{DRAW_START + DRAW_DUR + .6:.1f}s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="3.5s" begin="{DRAW_START + DRAW_DUR + .6:.1f}s" repeatCount="indefinite"/></rect>
''')

for i, (ver, title, company, start, end, status, dur, colour, year) in enumerate(ROLES):
    x, cx, t = card_x(i), centre(i), appear_at(i)
    current = status == "deploying"
    add(f'<g opacity="0">\n  <animate attributeName="opacity" to="1" dur=".5s" begin="{t:.2f}s" fill="freeze"/>\n'
        f'  <animateTransform attributeName="transform" type="translate" from="0 10" to="0 0" dur=".5s" begin="{t:.2f}s" fill="freeze"/>\n')
    if current:
        add(f'  <rect x="{x}" y="{CARD_Y}" width="{CARD_W}" height="{CARD_H}" rx="10" fill="{PURPLE}" opacity=".18" filter="url(#cardglow)"/>\n')
    add(f'  <rect x="{x + .5}" y="{CARD_Y + .5}" width="{CARD_W - 1}" height="{CARD_H - 1}" rx="10" fill="{CARD}" '
        f'stroke="{PURPLE if current else LINE}" stroke-opacity="{.8 if current else 1}"/>\n')
    # version tag (+ HEAD marker on the live release)
    add(f'  <rect x="{x + 12}" y="{CARD_Y + 13}" width="40" height="20" rx="10" fill="{colour}" fill-opacity=".14" stroke="{colour}" stroke-opacity=".5"/>\n'
        f'  <text class="m" x="{x + 32}" y="{CARD_Y + 27}" font-size="11" font-weight="600" fill="{colour}" text-anchor="middle">{ver}</text>\n')
    if current:
        add(f'  <rect x="{x + 58}" y="{CARD_Y + 13}" width="42" height="20" rx="10" fill="{PURPLE}"/>\n'
            f'  <text class="m" x="{x + 79}" y="{CARD_Y + 27}" font-size="10.5" font-weight="700" fill="#0d1117" text-anchor="middle">HEAD</text>\n')
    # status badge, top right
    sx, sy = x + CARD_W - 24, CARD_Y + 23
    if current:
        add(f'  <circle cx="{sx}" cy="{sy}" r="5" fill="{PURPLE}"/>\n'
            f'  <circle cx="{sx}" cy="{sy}" r="5" stroke="{PURPLE}" stroke-width="2"><animate attributeName="r" values="5;13" dur="1.6s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values=".9;0" dur="1.6s" repeatCount="indefinite"/></circle>\n')
    else:
        add(f'  <circle cx="{sx}" cy="{sy}" r="9" fill="{GREEN}" fill-opacity=".14" stroke="{GREEN}" stroke-opacity=".6"/>\n'
            f'  <path d="M{sx - 4},{sy} l3,3 l5,-6" stroke="{GREEN}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\n')
    # role, company, dates, status line
    add(f'  <text class="s" x="{x + 14}" y="{CARD_Y + 58}" font-size="13.5" font-weight="700" fill="{TEXT}">{title}</text>\n'
        f'  <text class="s" x="{x + 14}" y="{CARD_Y + 77}" font-size="11.5" fill="{MUTED}">{company}</text>\n'
        f'  <path d="M{x + 14},{CARD_Y + 92} H{x + CARD_W - 14}" stroke="#21262d"/>\n'
        f'  <text class="m" x="{x + 14}" y="{CARD_Y + 110}" font-size="10.5" fill="{DIM}">{start} → {end}</text>\n')
    if current:
        add(f'  <text class="m" x="{x + 14}" y="{CARD_Y + 126}" font-size="10.5" fill="{PURPLE}">● deploying<tspan>'
            f'<animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/>...</tspan></text>\n')
    else:
        verb = "↑ promoted" if status == "promoted" else "✓ shipped"
        add(f'  <text class="m" x="{x + 14}" y="{CARD_Y + 126}" font-size="10.5" fill="{GREEN}">{verb}<tspan fill="{DIM}"> · {dur}</tspan></text>\n')
    # drop line to the track, node, year
    add(f'  <path d="M{cx},{CARD_Y + CARD_H + 4} V{TRACK_Y - 12}" stroke="{colour}" stroke-opacity=".5" stroke-dasharray="2 3"/>\n'
        f'  <circle cx="{cx}" cy="{TRACK_Y}" r="7" fill="#0d1117" stroke="{colour}" stroke-width="3"/>\n'
        f'  <text class="m" x="{cx}" y="{TRACK_Y + 30}" font-size="10.5" fill="{DIM}" text-anchor="middle">{year}</text>\n</g>\n')

# Pulse on the live node once the track arrives.
cx = centre(len(ROLES) - 1)
add(f'''<circle cx="{cx}" cy="{TRACK_Y}" r="7" stroke="{PURPLE}" stroke-width="2" opacity="0">
  <animate attributeName="r" values="7;20" dur="1.8s" begin="{DRAW_START + DRAW_DUR:.1f}s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values=".8;0" dur="1.8s" begin="{DRAW_START + DRAW_DUR:.1f}s" repeatCount="indefinite"/></circle>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="15.5" stroke="{LINE}"/>
</svg>
''')

open(OUT, "w").write("".join(out))

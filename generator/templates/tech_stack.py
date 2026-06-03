import html
import math


def render(cfg: dict, stats: dict) -> str:
    t = cfg["theme"]
    bg = t["background"]
    txt1 = t["text_primary"]
    txt2 = t["text_secondary"]
    acc = t["accretion_outer"]
    cyan = t["cyan"]
    violet = t["violet"]
    amber = t["amber"]

    exclude = set(cfg.get("languages", {}).get("exclude", []))
    max_display = cfg.get("languages", {}).get("max_display", 7)
    langs = [l for l in stats.get("languages", []) if l["name"] not in exclude][:max_display]

    arms = cfg.get("orbit_arms", [])
    sectors = [arm["name"] for arm in arms]
    arm_colors_map = {"cyan": cyan, "violet": violet, "amber": amber}
    sector_colors = [arm_colors_map.get(arm.get("color", "cyan"), cyan) for arm in arms]

    W, H = 850, 185
    bar_x = 32
    bar_label_w = 90
    bar_total_w = 345
    pct_x = bar_x + bar_label_w + bar_total_w + 8
    chart_cx, chart_cy, chart_r = 670, 108, 56

    row_h = (H - 50) / max(len(langs), 1)
    bar_colors = [cyan, violet, amber, cyan, violet, amber, cyan]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <style>
    @keyframes rspin3{{to{{transform:rotate(360deg)}}}}
    .radararm{{animation:rspin3 10s linear infinite;transform-origin:{chart_cx}px {chart_cy}px}}
  </style>
</defs>
<rect width="{W}" height="{H}" fill="{bg}" rx="6"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" fill="none" stroke="{acc}" stroke-width="0.5" rx="5" opacity="0.4"/>
<text x="32" y="24" font-family="monospace" font-size="9" fill="{txt2}" letter-spacing="3" opacity="0.6">LANGUAGE TELEMETRY</text>
<text x="545" y="24" font-family="monospace" font-size="9" fill="{txt2}" letter-spacing="3" opacity="0.6">FOCUS SECTORS</text>
<line x1="32" y1="31" x2="{W-32}" y2="31" stroke="{acc}" stroke-width="0.5" opacity="0.25"/>
<line x1="515" y1="31" x2="515" y2="{H-12}" stroke="{acc}" stroke-width="0.5" opacity="0.2"/>
'''

    for i, lang in enumerate(langs):
        y = 38 + i * row_h
        bar_fill = min(lang["percent"] / 55.0, 1.0) * bar_total_w
        color = lang.get("color") or bar_colors[i % len(bar_colors)]
        label_y = y + row_h * 0.65

        svg += f'<text x="{bar_x}" y="{label_y:.0f}" font-family="monospace" font-size="11" fill="{txt1}">{lang["name"]}</text>\n'
        svg += f'<rect x="{bar_x + bar_label_w}" y="{y + 4:.0f}" width="{bar_total_w}" height="8" rx="2" fill="{acc}" opacity="0.12"/>\n'
        svg += f'<rect x="{bar_x + bar_label_w}" y="{y + 4:.0f}" width="{bar_fill:.0f}" height="8" rx="2" fill="{color}" opacity="0.75"/>\n'
        svg += f'<text x="{pct_x}" y="{label_y:.0f}" font-family="monospace" font-size="10" fill="{txt2}">{lang["percent"]:.1f}%</text>\n'

    # Radar chart
    for ring_r in [chart_r * 0.33, chart_r * 0.66, chart_r]:
        svg += f'<circle cx="{chart_cx}" cy="{chart_cy}" r="{ring_r:.0f}" fill="none" stroke="{acc}" stroke-width="0.5" opacity="0.2"/>\n'

    n = len(sectors)
    for i, (sector, color) in enumerate(zip(sectors, sector_colors)):
        angle = (i / n) * 2 * math.pi - math.pi / 2
        sx = chart_cx + math.cos(angle) * chart_r
        sy = chart_cy + math.sin(angle) * chart_r
        svg += f'<line x1="{chart_cx}" y1="{chart_cy}" x2="{sx:.1f}" y2="{sy:.1f}" stroke="{acc}" stroke-width="0.5" opacity="0.18"/>\n'
        tx = chart_cx + math.cos(angle) * (chart_r + 16)
        ty = chart_cy + math.sin(angle) * (chart_r + 16)
        svg += f'<text x="{tx:.1f}" y="{ty + 4:.1f}" text-anchor="middle" font-family="monospace" font-size="9" fill="{color}" opacity="0.9">{html.escape(sector)}</text>\n'

    if n >= 3:
        pts = []
        for i in range(n):
            angle = (i / n) * 2 * math.pi - math.pi / 2
            r = chart_r * [0.85, 0.7, 0.9][i % 3]
            pts.append(f"{chart_cx + math.cos(angle)*r:.1f},{chart_cy + math.sin(angle)*r:.1f}")
        svg += f'<polygon points="{" ".join(pts)}" fill="{violet}" fill-opacity="0.1" stroke="{violet}" stroke-width="0.8" opacity="0.45"/>\n'

    svg += f'<line class="radararm" x1="{chart_cx}" y1="{chart_cy}" x2="{chart_cx}" y2="{chart_cy - chart_r}" stroke="{cyan}" stroke-width="1.5" opacity="0.75"/>\n'

    svg += '</svg>'
    return svg

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

    projects = cfg.get("projects", [])[:4]
    arms = cfg.get("orbit_arms", [])
    arm_colors_map = {"cyan": cyan, "violet": violet, "amber": amber}
    arm_colors = [arm_colors_map.get(arm.get("color", "cyan"), cyan) for arm in arms]

    W = 850
    n = max(len(projects), 1)
    padding = 28
    gap = 10
    card_w = (W - padding * 2 - gap * (n - 1)) / n
    H = 195

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <style>
    @keyframes pdot{{from{{r:4;opacity:0.65}}to{{r:5.5;opacity:1}}}}
    .pd{{animation:pdot 3s ease-in-out infinite alternate}}
  </style>
</defs>
<rect width="{W}" height="{H}" fill="{bg}" rx="6"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" fill="none" stroke="{acc}" stroke-width="0.5" rx="5" opacity="0.4"/>
<text x="32" y="24" font-family="monospace" font-size="9" fill="{txt2}" letter-spacing="3" opacity="0.6">FEATURED SYSTEMS</text>
<line x1="32" y1="31" x2="{W-32}" y2="31" stroke="{acc}" stroke-width="0.5" opacity="0.25"/>
'''

    dot_positions = []
    for i, proj in enumerate(projects):
        x = padding + i * (card_w + gap)
        y = 40
        arm_idx = proj.get("arm", i % max(len(arm_colors), 1))
        color = arm_colors[arm_idx] if arm_idx < len(arm_colors) else cyan
        repo = proj.get("repo", "")
        name = repo.split("/")[-1] if "/" in repo else repo
        desc = proj.get("description", "")

        dot_x = x + card_w / 2
        dot_y = y + 22
        dot_positions.append((dot_x, dot_y, color))

        arm_label = arms[arm_idx]["name"] if arm_idx < len(arms) else ""
        pill_w = len(arm_label) * 6.5 + 16
        pill_x = x + card_w / 2 - pill_w / 2

        # Desc line split
        desc_line1 = desc[:30] if len(desc) > 30 else desc
        desc_line2 = desc[30:60] if len(desc) > 30 else ""

        svg += f'''<rect x="{x:.1f}" y="{y:.0f}" width="{card_w:.1f}" height="140" rx="4" fill="#0d0d20" stroke="{color}" stroke-width="0.5" opacity="0.55"/>
<circle class="pd" cx="{dot_x:.1f}" cy="{dot_y:.1f}" r="4" fill="{color}" style="animation-delay:{i}s"/>
<text x="{dot_x:.1f}" y="{y+52:.0f}" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="{txt1}">{name}</text>
<text x="{dot_x:.1f}" y="{y+69:.0f}" text-anchor="middle" font-family="monospace" font-size="9" fill="{txt2}" opacity="0.6">{repo}</text>
<text x="{dot_x:.1f}" y="{y+90:.0f}" text-anchor="middle" font-family="monospace" font-size="10" fill="{txt2}">{desc_line1}</text>
'''
        if desc_line2:
            svg += f'<text x="{dot_x:.1f}" y="{y+104:.0f}" text-anchor="middle" font-family="monospace" font-size="10" fill="{txt2}">{desc_line2}</text>\n'

        svg += f'''<rect x="{pill_x:.1f}" y="{y+118:.0f}" width="{pill_w:.0f}" height="15" rx="7" fill="{color}" fill-opacity="0.1" stroke="{color}" stroke-width="0.5"/>
<text x="{dot_x:.1f}" y="{y+129:.0f}" text-anchor="middle" font-family="monospace" font-size="9" fill="{color}">{arm_label}</text>
'''

    # Constellation connector lines between dot centers
    for i in range(len(dot_positions) - 1):
        x1, y1, _ = dot_positions[i]
        x2, y2, _ = dot_positions[i + 1]
        svg += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{acc}" stroke-width="0.5" stroke-dasharray="3,3" opacity="0.3"/>\n'

    svg += '</svg>'
    return svg

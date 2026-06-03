import math
import random


def render(cfg: dict, stats: dict) -> str:
    t = cfg["theme"]
    p = cfg["profile"]
    arms = cfg.get("orbit_arms", [])

    bg = t["background"]
    txt1 = t["text_primary"]
    txt2 = t["text_secondary"]
    acc_in = t["accretion_inner"]
    acc_out = t["accretion_outer"]
    jet_col = t["jet"]
    arm_colors = {"cyan": t["cyan"], "violet": t["violet"], "amber": t["amber"]}

    W, H = 850, 310
    cx, cy = 425, 162

    rng = random.Random(42)
    stars = [
        (rng.randint(5, W-5), rng.randint(5, H-5), round(rng.uniform(0.4, 1.2), 1),
         round(rng.uniform(1.6, 3.8), 1), round(rng.uniform(0.0, 2.8), 1),
         round(rng.uniform(0.08, 0.25), 2), round(rng.uniform(0.6, 0.95), 2))
        for _ in range(140)
    ]

    # Spread orbit items evenly across full 360 degrees, grouped by arm
    # Arm 0: 0–110 deg (right), Arm 1: 120–230 deg (left-bottom), Arm 2: 250–360 deg (top)
    arm_ranges = [(0, 110), (120, 230), (250, 360)]
    orbit_r = 135      # horizontal radius
    orbit_ry = 40      # vertical radius (ellipse squish)

    orbit_items = []
    for arm_idx, arm in enumerate(arms):
        color = arm_colors.get(arm.get("color", "cyan"), "#ffffff")
        items = arm.get("items", [])
        n = len(items)
        start_deg, end_deg = arm_ranges[arm_idx % 3]
        for i, item in enumerate(items):
            frac = i / max(n, 1)
            deg = start_deg + frac * (end_deg - start_deg)
            rad = math.radians(deg)
            ox = cx + math.cos(rad) * orbit_r
            oy = cy + math.sin(rad) * orbit_ry
            # Decide label anchor based on position
            if ox > cx + 20:
                anchor, lx = "start", ox + 8
            elif ox < cx - 20:
                anchor, lx = "end", ox - 8
            else:
                anchor, lx = "middle", ox
            ly = oy - 10 if oy < cy else oy + 18
            orbit_items.append({
                "label": item, "x": ox, "y": oy,
                "lx": lx, "ly": ly, "anchor": anchor,
                "color": color
            })

    # Build per-star keyframes — no CSS vars
    star_anims = ""
    star_els = ""
    for idx, (sx, sy, sr, dur, delay, lo, hi) in enumerate(stars):
        anim_id = f"tw{idx}"
        star_anims += f"@keyframes {anim_id}{{from{{opacity:{lo}}}to{{opacity:{hi}}}}}"
        star_els += f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#ffffff" style="animation:{anim_id} {dur}s {delay}s infinite alternate ease-in-out"/>\n'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <radialGradient id="bh" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#000"/>
    <stop offset="40%" stop-color="#0d0020"/>
    <stop offset="70%" stop-color="{acc_out}" stop-opacity="0.3"/>
    <stop offset="100%" stop-color="{bg}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="bgr" cx="50%" cy="45%" r="65%">
    <stop offset="0%" stop-color="#0e0828"/>
    <stop offset="100%" stop-color="#060410"/>
  </radialGradient>
  <style>
    {star_anims}
    @keyframes rspin{{to{{transform:rotate(360deg)}}}}
    @keyframes rrev{{to{{transform:rotate(-360deg)}}}}
    @keyframes jpulse{{from{{opacity:0.25}}to{{opacity:0.85}}}}
    @keyframes pout{{0%{{r:46;opacity:0.3}}100%{{r:78;opacity:0}}}}
    .r1{{animation:rspin 24s linear infinite;transform-origin:{cx}px {cy}px}}
    .r2{{animation:rrev 40s linear infinite;transform-origin:{cx}px {cy}px}}
    .jet{{animation:jpulse 3s ease-in-out infinite alternate}}
    .pulse{{animation:pout 4.5s ease-out infinite;transform-origin:{cx}px {cy}px}}
  </style>
</defs>
<rect width="{W}" height="{H}" fill="url(#bgr)"/>
{star_els}
<circle cx="{cx}" cy="{cy}" r="120" fill="url(#bh)"/>
<ellipse class="r2" cx="{cx}" cy="{cy}" rx="105" ry="26" fill="none" stroke="{acc_out}" stroke-width="1" opacity="0.4"/>
<ellipse class="r1" cx="{cx}" cy="{cy}" rx="84" ry="21" fill="none" stroke="{acc_in}" stroke-width="2.5" opacity="0.8"/>
<ellipse cx="{cx}" cy="{cy}" rx="66" ry="16" fill="none" stroke="{acc_in}" stroke-width="0.8" opacity="0.3"/>
<circle class="pulse" cx="{cx}" cy="{cy}" r="46" fill="none" stroke="{acc_out}" stroke-width="1.5"/>
<line class="jet" x1="{cx}" y1="{cy-44}" x2="{cx}" y2="{cy-126}" stroke="{jet_col}" stroke-width="3.5" stroke-linecap="round"/>
<line class="jet" x1="{cx}" y1="{cy+44}" x2="{cx}" y2="{cy+126}" stroke="{jet_col}" stroke-width="3.5" stroke-linecap="round"/>
<line x1="{cx}" y1="{cy-44}" x2="{cx}" y2="{cy-118}" stroke="{acc_in}" stroke-width="1" opacity="0.3" stroke-linecap="round"/>
<line x1="{cx}" y1="{cy+44}" x2="{cx}" y2="{cy+118}" stroke="{acc_in}" stroke-width="1" opacity="0.3" stroke-linecap="round"/>
<circle cx="{cx}" cy="{cy}" r="43" fill="#000"/>
<circle cx="{cx}" cy="{cy}" r="38" fill="#020008"/>
<circle cx="{cx}" cy="{cy}" r="44" fill="none" stroke="{acc_in}" stroke-width="1.4" opacity="0.95"/>
'''

    for item in orbit_items:
        svg += f'<circle cx="{item["x"]:.1f}" cy="{item["y"]:.1f}" r="3.5" fill="{item["color"]}" opacity="0.9"/>\n'
        svg += f'<text x="{item["lx"]:.1f}" y="{item["ly"]:.1f}" text-anchor="{item["anchor"]}" font-family="monospace" font-size="10" fill="{item["color"]}">{item["label"]}</text>\n'

    name = p.get("name", cfg.get("username", ""))
    title = p.get("title", "")
    bio = p.get("bio", "")

    svg += f'''<text x="{cx}" y="32" text-anchor="middle" font-family="monospace" font-size="19" font-weight="bold" fill="{txt1}" letter-spacing="3">{name}</text>
<text x="{cx}" y="54" text-anchor="middle" font-family="monospace" font-size="11" fill="{txt2}" letter-spacing="2">{title}</text>
<text x="{cx}" y="{H-13}" text-anchor="middle" font-family="monospace" font-size="10" fill="{txt2}" opacity="0.6" font-style="italic">{bio}</text>
</svg>'''

    return svg

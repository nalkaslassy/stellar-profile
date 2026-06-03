def render(cfg: dict, stats: dict) -> str:
    t = cfg["theme"]
    bg = t["background"]
    txt2 = t["text_secondary"]
    acc = t["accretion_outer"]
    cyan = t["cyan"]

    metrics_cfg = cfg.get("stats", {}).get("metrics", ["commits", "stars", "prs", "issues", "repos"])

    labels = {
        "commits":  ("COMMITS",      _fmt(stats.get("commits", 0))),
        "stars":    ("STARS",        _fmt(stats.get("stars", 0))),
        "prs":      ("PULL REQUESTS",_fmt(stats.get("prs", 0))),
        "issues":   ("ISSUES",       _fmt(stats.get("issues", 0))),
        "repos":    ("REPOS",        _fmt(stats.get("repos", 0))),
    }

    metrics = [(k, *labels[k]) for k in metrics_cfg if k in labels]

    W, H = 850, 120
    n = len(metrics)
    col_w = W / n

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="{bg}" rx="6"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" fill="none" stroke="{acc}" stroke-width="0.5" rx="5" opacity="0.4"/>
<text x="32" y="24" font-family="monospace" font-size="9" fill="{txt2}" letter-spacing="3" opacity="0.6">MISSION TELEMETRY</text>
<line x1="32" y1="31" x2="{W-32}" y2="31" stroke="{acc}" stroke-width="0.5" opacity="0.25"/>
'''

    for i, (key, label, value) in enumerate(metrics):
        x = col_w * i + col_w / 2
        if i > 0:
            lx = col_w * i
            svg += f'<line x1="{lx:.0f}" y1="38" x2="{lx:.0f}" y2="{H-12}" stroke="{acc}" stroke-width="0.5" opacity="0.2"/>\n'
        svg += f'<text x="{x:.1f}" y="80" text-anchor="middle" font-family="monospace" font-size="32" font-weight="bold" fill="{cyan}">{value}</text>\n'
        svg += f'<text x="{x:.1f}" y="101" text-anchor="middle" font-family="monospace" font-size="9" fill="{txt2}" letter-spacing="2" opacity="0.8">{label}</text>\n'

    svg += '</svg>'
    return svg


def _fmt(n: int) -> str:
    if n >= 1000:
        return f"{n/1000:.1f}k"
    return str(n)

"""Convert generated SVGs to PNGs for GitHub README display.

Tries cairosvg first (works in CI on Linux), then falls back to Node.js + sharp
for local development on Windows/Mac where the Cairo system library may be missing.
"""
import json
import os
import subprocess
import sys

SVG_DIR = "assets/generated"

CONVERSIONS = [
    ("blackhole-header.svg", "blackhole-header.png"),
    ("stats-card.svg", "stats-card.png"),
    ("tech-stack.svg", "tech-stack.png"),
    ("projects-constellation.svg", "projects-constellation.png"),
]


def _convert_cairosvg(pairs):
    import cairosvg
    for svg_name, png_name in pairs:
        svg_path = os.path.join(SVG_DIR, svg_name)
        png_path = os.path.join(SVG_DIR, png_name)
        if not os.path.exists(svg_path):
            print(f"Skipping {svg_name} (not found)")
            continue
        cairosvg.svg2png(url=svg_path, write_to=png_path, scale=2.0)
        size_kb = os.path.getsize(png_path) // 1024
        print(f"Converted {svg_name} -> {png_name} ({size_kb} KB)")


def _convert_node_sharp(pairs):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    node_script = """
const sharp = require('sharp');
const path = require('path');
const fs = require('fs');
const pairs = """ + json.dumps([[os.path.join(SVG_DIR, s), os.path.join(SVG_DIR, p)] for s, p in pairs]) + """;
async function run() {
  for (const [svg, png] of pairs) {
    if (!fs.existsSync(svg)) { console.log('Skipping ' + svg); continue; }
    await sharp(svg, { density: 144 }).png().toFile(png);
    const kb = Math.round(fs.statSync(png).size / 1024);
    console.log('Converted ' + path.basename(svg) + ' -> ' + path.basename(png) + ' (' + kb + ' KB)');
  }
  console.log('Done.');
}
run().catch(e => { console.error(e.message); process.exit(1); });
"""
    tmp = os.path.join(project_dir, "_convert_tmp.js")
    try:
        with open(tmp, "w") as f:
            f.write(node_script)
        result = subprocess.run(["node", tmp], capture_output=True, text=True, cwd=project_dir)
        print(result.stdout, end="")
        if result.returncode != 0:
            raise RuntimeError(result.stderr)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main():
    try:
        import cairosvg
        cairosvg.surface  # trigger DLL load
        print("Using cairosvg backend")
        _convert_cairosvg(CONVERSIONS)
    except (ImportError, OSError):
        print("cairosvg unavailable, falling back to Node.js + sharp")
        try:
            _convert_node_sharp(CONVERSIONS)
        except FileNotFoundError:
            print("ERROR: neither cairosvg nor Node.js is available.")
            print("Install cairosvg (Linux/Mac) or Node.js + sharp (Windows).")
            sys.exit(1)


if __name__ == "__main__":
    main()

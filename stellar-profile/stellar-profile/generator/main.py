import argparse
import os
import sys

from generator.config import load_config, DEMO_CONFIG, DEMO_STATS
from generator.github_api import fetch_stats
from generator.templates import blackhole_header, stats_card, tech_stack, projects_constellation

OUTPUT_DIR = "assets/generated"


def main():
    parser = argparse.ArgumentParser(description="Generate stellar GitHub profile SVGs")
    parser.add_argument("--demo", action="store_true", help="Use demo data, no API calls")
    parser.add_argument("--config", default="config.yml", help="Path to config file")
    args = parser.parse_args()

    if args.demo:
        cfg = DEMO_CONFIG
        stats = DEMO_STATS
        print("[stellar-profile] Running in demo mode with sample data.")
    else:
        try:
            cfg = load_config(args.config)
        except FileNotFoundError as e:
            print(f"[stellar-profile] Error: {e}")
            sys.exit(1)

        username = cfg.get("username")
        if not username:
            print("[stellar-profile] Error: 'username' is required in config.yml")
            sys.exit(1)

        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            print("[stellar-profile] Warning: No GITHUB_TOKEN found. Commit counts will be limited.")

        print(f"[stellar-profile] Fetching stats for @{username}...")
        stats = fetch_stats(username, token)
        print(f"[stellar-profile] Got stats: commits={stats.get('commits')}, stars={stats.get('stars')}, repos={stats.get('repos')}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    renders = [
        ("blackhole-header.svg", blackhole_header.render),
        ("stats-card.svg", stats_card.render),
        ("tech-stack.svg", tech_stack.render),
        ("projects-constellation.svg", projects_constellation.render),
    ]

    for filename, render_fn in renders:
        path = os.path.join(OUTPUT_DIR, filename)
        svg = render_fn(cfg, stats)
        with open(path, "w") as f:
            f.write(svg)
        print(f"[stellar-profile] Generated {path}")

    print("[stellar-profile] Done. Open assets/generated/ in a browser to preview.")


if __name__ == "__main__":
    main()

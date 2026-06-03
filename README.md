# stellar-profile

Your GitHub profile, reimagined as a black hole. Auto-generated animated SVG cards with a deep space aesthetic — stats, tech stack, language telemetry, and featured projects.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-brightgreen.svg)](https://python.org)

## Preview

![Blackhole Header](./assets/generated/blackhole-header.png)

![Stats](./assets/generated/stats-card.png)

![Tech Stack](./assets/generated/tech-stack.png)

![Projects](./assets/generated/projects-constellation.png)

## Features

- **Black hole header** — animated accretion disk, relativistic jets, and orbiting tech labels
- **Mission telemetry** — real-time commits, stars, PRs, issues, and repo count
- **Language telemetry** — language usage bars with a rotating radar chart of focus sectors
- **Featured systems** — project constellation cards with orbital animations
- **Fully configurable** — colors, tech stack, projects, and metrics all via `config.yml`
- **Auto-updates** — GitHub Actions regenerates SVGs every 12 hours

## Quick Start

1. **Use this template** (click "Use this template" above) and name the new repo your GitHub username.

2. Copy the example config:
   ```bash
   cp config.example.yml config.yml
   ```

3. Edit `config.yml` with your details — name, title, tech stack, projects, etc.

4. Replace your `README.md` with `README.profile.md` and update the social links.

5. In `.github/workflows/generate-profile.yml`, change:
   ```yaml
   run: python -m generator.main --demo
   ```
   to:
   ```yaml
   run: python -m generator.main
   ```

6. Push — the Action generates and commits your SVGs automatically. You can also trigger it manually from the Actions tab.

## Local Development

```bash
git clone https://github.com/YOUR_USERNAME/stellar-profile.git
cd stellar-profile
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp config.example.yml config.yml

# Demo mode (no API calls)
python -m generator.main --demo

# With your real data
GITHUB_TOKEN=ghp_your_token python -m generator.main
```

SVGs are written to `assets/generated/`. Open them directly in a browser to preview.

To generate a token: [github.com/settings/tokens](https://github.com/settings/tokens) → Generate new (classic) → select `read:user` scope.

## Configuration

All config lives in `config.yml`. See `config.example.yml` for a fully commented template.

| Section | Description |
|---|---|
| `username` | Your GitHub username (required) |
| `profile` | Name, title, bio, location, company |
| `social` | Email, LinkedIn, website |
| `orbit_arms` | 3 tech groups that orbit the black hole — name, color, and items |
| `projects` | Featured repos with description and which arm they belong to |
| `stats.metrics` | Which metrics to show: `commits`, `stars`, `prs`, `issues`, `repos` |
| `languages` | Languages to exclude and max count to display |
| `theme` | Full color overrides for the deep space palette |

## Architecture

```
generator/
├── main.py                          # Entry point
├── config.py                        # Config loading and defaults
├── github_api.py                    # GitHub GraphQL + REST client
└── templates/
    ├── blackhole_header.py          # Animated black hole banner (850×300)
    ├── stats_card.py                # Mission telemetry card (850×140)
    ├── tech_stack.py                # Language bars + radar chart (850×200)
    └── projects_constellation.py   # Project cards (850×220)
```

## Contributing

Bug reports, feature requests, and PRs are welcome. Open an issue first for anything beyond small fixes.

## License

MIT

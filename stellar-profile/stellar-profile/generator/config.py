import yaml
import os
from dataclasses import dataclass, field
from typing import List, Optional

DEMO_CONFIG = {
    "username": "demo-user",
    "profile": {
        "name": "Demo User",
        "title": "AI Engineer",
        "bio": "Building things that matter.",
        "location": "San Francisco, CA",
        "company": "@demo-corp",
    },
    "social": {
        "email": "demo@example.com",
        "linkedin": "demo-user",
        "website": "https://demo.dev",
    },
    "orbit_arms": [
        {"name": "Languages", "color": "cyan", "items": ["Python", "TypeScript", "Rust", "SQL"]},
        {"name": "Cloud & Infra", "color": "violet", "items": ["AWS", "Docker", "Terraform", "Linux"]},
        {"name": "Frameworks", "color": "amber", "items": ["FastAPI", "React", "PySpark", "PostgreSQL"]},
    ],
    "projects": [
        {"repo": "demo-user/project-alpha", "description": "An AI-powered tool for data pipelines.", "arm": 0},
        {"repo": "demo-user/project-beta", "description": "Cloud-native microservices platform.", "arm": 1},
        {"repo": "demo-user/project-gamma", "description": "Real-time analytics dashboard.", "arm": 2},
    ],
    "stats": {"metrics": ["commits", "stars", "prs", "issues", "repos"]},
    "languages": {"exclude": ["HTML", "CSS", "Makefile"], "max_display": 7},
    "theme": {
        "background": "#0a0a12",
        "singularity": "#000000",
        "accretion_inner": "#ff6ef7",
        "accretion_outer": "#7c3aed",
        "jet": "#c084fc",
        "text_primary": "#e2d9f3",
        "text_secondary": "#9f7edd",
        "cyan": "#22d3ee",
        "violet": "#a78bfa",
        "amber": "#fbbf24",
    },
}

DEMO_STATS = {
    "commits": 1247,
    "stars": 342,
    "prs": 89,
    "issues": 14,
    "repos": 28,
    "languages": [
        {"name": "Python", "percent": 45.2, "color": "#3572A5"},
        {"name": "TypeScript", "percent": 28.1, "color": "#2b7489"},
        {"name": "Rust", "percent": 12.4, "color": "#dea584"},
        {"name": "SQL", "percent": 7.8, "color": "#e38c00"},
        {"name": "Shell", "percent": 4.1, "color": "#89e051"},
        {"name": "Go", "percent": 2.4, "color": "#00ADD8"},
    ],
    "focus_sectors": ["AI & Data", "Cloud", "Web"],
}


def load_config(path="config.yml"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config not found at {path}. Copy config.example.yml to config.yml and fill it in.")
    with open(path) as f:
        cfg = yaml.safe_load(f)
    _apply_defaults(cfg)
    return cfg


def _apply_defaults(cfg):
    cfg.setdefault("theme", {})
    for k, v in DEMO_CONFIG["theme"].items():
        cfg["theme"].setdefault(k, v)
    cfg.setdefault("stats", {}).setdefault("metrics", ["commits", "stars", "prs", "issues", "repos"])
    cfg.setdefault("languages", {}).setdefault("exclude", [])
    cfg["languages"].setdefault("max_display", 7)

import os
import requests
from typing import Optional


def fetch_stats(username: str, token: Optional[str] = None) -> dict:
    token = token or os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"bearer {token}"} if token else {}

    stats = {"commits": 0, "stars": 0, "prs": 0, "issues": 0, "repos": 0, "languages": [], "focus_sectors": []}

    if token:
        stats.update(_graphql_fetch(username, headers))
    else:
        stats.update(_rest_fetch(username))

    stats["languages"] = _fetch_languages(username, headers)
    return stats


def _graphql_fetch(username: str, headers: dict) -> dict:
    query = """
    query($login: String!) {
      user(login: $login) {
        repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
          nodes { stargazerCount primaryLanguage { name color } }
        }
        contributionsCollection {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
        }
        repositoriesContributedTo(first: 1) { totalCount }
        pullRequests(states: MERGED) { totalCount }
        issues { totalCount }
      }
    }
    """
    try:
        r = requests.post(
            "https://api.github.com/graphql",
            json={"query": query, "variables": {"login": username}},
            headers=headers,
            timeout=10,
        )
        data = r.json().get("data", {}).get("user", {})
        repos = data.get("repositories", {}).get("nodes", [])
        cc = data.get("contributionsCollection", {})
        return {
            "commits": cc.get("totalCommitContributions", 0),
            "stars": sum(r.get("stargazerCount", 0) for r in repos),
            "prs": data.get("pullRequests", {}).get("totalCount", 0),
            "issues": data.get("issues", {}).get("totalCount", 0),
            "repos": len(repos),
        }
    except Exception:
        return _rest_fetch(username)


def _rest_fetch(username: str) -> dict:
    try:
        r = requests.get(f"https://api.github.com/users/{username}", timeout=10)
        u = r.json()
        return {
            "commits": 0,
            "stars": 0,
            "prs": 0,
            "issues": 0,
            "repos": u.get("public_repos", 0),
        }
    except Exception:
        return {}


def _fetch_languages(username: str, headers: dict) -> list:
    try:
        r = requests.get(
            f"https://api.github.com/users/{username}/repos?per_page=100&sort=pushed",
            headers=headers,
            timeout=10,
        )
        repos = r.json()
        lang_bytes = {}
        for repo in repos[:30]:
            if repo.get("fork"):
                continue
            lr = requests.get(repo["languages_url"], headers=headers, timeout=5)
            for lang, count in lr.json().items():
                lang_bytes[lang] = lang_bytes.get(lang, 0) + count

        total = sum(lang_bytes.values()) or 1
        sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)

        lang_colors = {
            "Python": "#3572A5", "TypeScript": "#2b7489", "JavaScript": "#f1e05a",
            "Rust": "#dea584", "Go": "#00ADD8", "Java": "#b07219", "C++": "#f34b7d",
            "C": "#555555", "SQL": "#e38c00", "Shell": "#89e051", "Ruby": "#701516",
            "Swift": "#ffac45", "Kotlin": "#A97BFF", "Svelte": "#ff3e00",
        }

        return [
            {
                "name": name,
                "percent": round(count / total * 100, 1),
                "color": lang_colors.get(name, "#888888"),
            }
            for name, count in sorted_langs[:10]
        ]
    except Exception:
        return []

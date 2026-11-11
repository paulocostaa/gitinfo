import json
from urllib import parse, request
from urllib.error import URLError

from .constants import _COMMITS_URL, _REPOS_URL


def fetch_repos(username: str) -> dict:
    if not username:
        raise ValueError("missing username")

    if not isinstance(username, str):
        return ValueError(f"username: expected 'str', got '{type(username).__name__}'")

    url: str = _REPOS_URL.format(
        username=parse.quote(username, safe="")
    )
    try:
        with request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8", errors="replace"))
    except URLError as e:
        raise RuntimeError(f"failed to fetch repositories: {e.reason}") from e


def fetch_commits(username: str, repo: str) -> list:
    if not username:
        raise ValueError("missing username")
    if not repo:
        raise ValueError("missing repository")

    if not isinstance(username, str):
        raise TypeError(f"username: expected 'str', got '{type(username).__name__}'")
    if not isinstance(repo, str):
        raise TypeError(f"repo: expected 'str', got '{type(repo).__name__}'")

    url: str = _COMMITS_URL.format(
        username=parse.quote(username, safe=""), repo=parse.quote(repo, safe="")
    )

    try:
        with request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8", errors="replace"))
    except URLError as e:
        raise RuntimeError(f"failed to fetch commits: {e.reason}") from e


# took from https://github.com/evilstdio/gitmail
def extract_emails(commits: list) -> dict:
    results: dict = {}

    for item in commits:
        author = item.get("commit", {}).get("author") or {}
        name = author.get("name", "Unknown")
        email = author.get("email", "")

        if email and "noreply.github.com" not in email:
            if email not in results:
                results[email] = {"name": name, "count": 1}
            else:
                results[email]["count"] += 1

    return results

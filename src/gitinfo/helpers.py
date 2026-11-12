from __future__ import annotations

import json
from typing import Any
from urllib import parse, request
from urllib.error import URLError

from .constants import _COMMITS_URL, _REPOS_URL


def fetch_repos(username: str) -> list[dict[str, Any]]:
    """
    Fetch a user's publicly available repositories from GitHub's REST API.

    Args:
        username: GitHub username; percent-quoted before the request.

    Returns:
        List of repository objects, first page only (~30 items).

    Raises:
        ValueError: Empty username.
        TypeError: Username not a str.
        RuntimeError: The request failed at the network level.
    """

    if not username:
        raise ValueError("missing username")

    if not isinstance(username, str):
        raise TypeError(f"username: expected 'str', got '{type(username).__name__}'")

    url: str = _REPOS_URL.format(username=parse.quote(username, safe=""))
    try:
        with request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8", errors="replace"))
    except URLError as e:
        raise RuntimeError(f"failed to fetch repositories: {e.reason}") from e


def fetch_commits(username: str, repo: str) -> list[dict[str, Any]]:
    """
    Fetch a repository's commit list from GitHub's REST API.

    Returns commits from the default branch.

    Args:
        username: Repository owner's GitHub username.
        repo: Repository name; percent-quoted before the request.

    Returns:
        List of commit objects, first page only (~30 items).

    Raises:
        ValueError: Empty username or repo.
        TypeError: Username or repo not a str.
        RuntimeError: The request failed at the network level.
    """

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
def extract_emails(commits: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """
    Aggregate author contact info from a list of commit objects.

    Emails come straight from each commit's ``commit.author.email`` field
    (nothing is scanned out of free text); commits authored with GitHub's
    noreply address are skipped, so privacy-enabled authors won't appear.

    Args:
        commits: Commit objects as returned by ``fetch_commits``.

    Returns:
        Mapping email -> {"name": author name, "count": occurrences}.

    Raises:
        TypeError: Commits not a list.
    """
    if not isinstance(commits, list):
        raise TypeError(f"commits: expected 'list', got: {type(commits).__name__}")

    _results: dict = {}

    for item in commits:
        author = item.get("commit", {}).get("author") or {}
        name = author.get("name", "Unknown")
        email = author.get("email", "")

        if email and "noreply.github.com" not in email:
            if email not in _results:
                _results[email] = {"name": name, "count": 1}
            else:
                _results[email]["count"] += 1

    return _results

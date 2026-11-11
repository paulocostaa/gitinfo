from gitinfo import fetch_commits


def main(username: str, repo: str) -> None:
    raw_commits = fetch_commits(username, repo)
    for c in raw_commits:
        print(c.get("author", {}).get("name", "") or {})

if __name__ == "__main__":
    main("paulocostaa", "gitinfo")

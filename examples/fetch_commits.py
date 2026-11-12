from gitinfo import fetch_commits


def main(username: str, repository: str):
    try:
        for commit in fetch_commits(username, repository):
            print(commit["sha"], commit["commit"]["message"].splitlines()[0])
    except (RuntimeError, ValueError, TypeError) as e:
        print(e)


if __name__ == "__main__":
    main("paulocostaa", "gitinfo")

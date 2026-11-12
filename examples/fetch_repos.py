from gitinfo import fetch_repos


def main(username: str):
    try:
        for repo in fetch_repos(username):
            print(repo["name"], repo["html_url"])
    except (RuntimeError, ValueError, TypeError) as e:
        print(e)


if __name__ == "__main__":
    main("paulocostaa")

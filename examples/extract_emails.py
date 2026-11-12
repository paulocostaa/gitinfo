from gitinfo import extract_emails, fetch_commits


def main(username: str, repository: str):
    try:
        emails = extract_emails(fetch_commits(username, repository))
        for email, info in emails.items():
            print(email, info["name"], info["count"])
    except (RuntimeError, ValueError, TypeError) as e:
        print(e)


if __name__ == "__main__":
    main("paulocostaa", "gitinfo")

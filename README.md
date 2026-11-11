# gitinfo

Fetch a GitHub user's public repos and commits, and collect author emails from
them. Python ≥ 3.8, standard library only.

## Install

```sh
pip install .
```

## Usage

```python
from gitinfo import fetch_repos, fetch_commits, extract_emails

for repo in fetch_repos("paulocostaa"):
    name = repo.get("name")
    emails = extract_emails(fetch_commits("paulocostaa", name))
    print(name, emails)
```

`extract_emails` returns `{email: {"name": ..., "count": ...}}` and skips
`noreply.github.com` addresses. Emails come from the API's author fields —
nothing is scanned out of commit messages.

Email-collecting logic borrowed from [evilstdio/gitmail](https://github.com/evilstdio/gitmail).

## Disclaimer

This tool is provided "as is", with no warranty of any kind. I, **paulocostaa**,
am not liable for any damage caused by the use of this tool. Use it
responsibly and at your own risk.

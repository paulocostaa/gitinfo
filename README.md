# gitinfo

Fetch a GitHub user's public repos and commits, and collect author emails from
them. Python ≥ 3.8, standard library only.

## Install

```sh
pip install .
```

## Usage

Runnable examples live in [`examples/`](examples):

- [`examples/fetch_repos.py`](examples/fetch_repos.py) — list a user's
  public repositories.
- [`examples/fetch_commits.py`](examples/fetch_commits.py) — list commits
  from a repository's default branch.
- [`examples/extract_emails.py`](examples/extract_emails.py) — aggregate
  commit author emails.

Run one directly:

```sh
python examples/extract_emails.py
```

Each imports its functions from `gitinfo` (`fetch_repos`, `fetch_commits`,
`extract_emails`) and works as a starting point for your own script.

`extract_emails` returns `{email: {"name": ..., "count": ...}}` and skips
`noreply.github.com` addresses. Emails come from the API's author fields —
nothing is scanned out of commit messages.

Email-collecting logic borrowed from [evilstdio/gitmail](https://github.com/evilstdio/gitmail).

## Disclaimer

This tool is provided "as is", with no warranty of any kind. I, **paulocostaa**,
am not liable for any damage caused by the use of this tool. Use it
responsibly and at your own risk.

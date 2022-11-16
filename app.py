import os
from pathlib import Path

from github import Github
from github.Repository import Repository

g = Github(os.environ["GITHUB_TOKEN"])
repo = os.environ.get("GITHUB_REPOSITORY", "lizadaly/forks")

out = Path('index.html').open('w')

def get_all_forks(repo: Repository, forks: list[Repository]) -> list[Repository]:
    if repo.parent is None:
        print(f"<p>{repo.owner.name or repo.owner.login} started the journey on {repo.created_at}.</p>", file=out)

    for fork in repo.get_forks():
        print(f"""
        <p>
        {fork.owner.name or fork.owner.login} joined the party on {fork.created_at}.
        </p>""", file=out)
        forks.append(fork)
        get_all_forks(fork, forks)
    return forks

def main():

    forks = get_all_forks(g.get_repo(repo), [])





if __name__ == "__main__":
    main()

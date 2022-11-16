import os
from pathlib import Path

from github import Github
from github.Repository import Repository
from jinja2 import FileSystemLoader, Environment

g = Github(os.environ["GITHUB_TOKEN"])
repo_name = os.environ.get("GITHUB_REPOSITORY", "lizadaly/forks")






def get_all_forks(repo: Repository, forks: list[Repository]) -> list[Repository]:

    for fork in repo.get_forks():
        forks.append(fork)
        get_all_forks(fork, forks)
    return forks

def main():
    repo = g.get_repo(repo_name)
    root = repo if repo.parent is None else repo.parent  # FIXME find real parent
    forks = get_all_forks(repo, [])

    loader = FileSystemLoader(".")
    env = Environment(loader=loader)
    template = env.get_template("index.jinja")
    Path('index.html').write_text(template.render({
        "root": root,
        "forks": forks
    }))



if __name__ == "__main__":
    main()

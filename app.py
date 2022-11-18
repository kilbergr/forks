import os
from pathlib import Path
import json
import random

from github import Github
from github.Repository import Repository
from jinja2 import FileSystemLoader, Environment

g = Github(os.environ["GITHUB_TOKEN"])

def generate_random_modifiers(username: str) -> dict[str, str]:
    random.seed(username)

    return {
        "weather": random.choice(
            json.load(Path("data/weather_conditions.json").open())["conditions"]
        ),
        "materials": random.choice(
            json.load(Path("data/natural-materials.json").open())["natural materials"]
        ),
        "flowers": random.choice(
            json.load(Path("data/flowers.json").open())["flowers"]
        ),
        "stones": random.choice(
            json.load(Path("data/decorative-stones.json").open())["decorative stones"]
        ),
        "metals": random.choice(
            json.load(Path("data/layperson-metals.json").open())["layperson metals"]
        ),
    }


def get_all_forks(repo: Repository, forks: list[Repository]) -> list[Repository]:

    for fork in repo.get_forks():

        fork.owner.forks_data = generate_random_modifiers(fork.owner.login)
        forks.append(fork)
        get_all_forks(fork, forks)
    return forks


def main(repo_name=str):
    repo = g.get_repo(repo_name)
    repo.owner.forks_data = generate_random_modifiers(repo.owner.login)

    source = repo.source or repo
    source.owner.forks_data = generate_random_modifiers(source.owner.login)

    parent = repo.parent or repo
    parent.owner.forks_data = generate_random_modifiers(parent.owner.login)

    # Get all descendent forks from this repo
    forks = get_all_forks(repo, [])

    loader = FileSystemLoader(".")
    env = Environment(
        loader=loader, extensions=["jinja2_humanize_extension.HumanizeExtension"]
    )
    template = env.get_template("index.jinja")
    Path("index.html").write_text(
        template.render({"repo": repo, "source": source, "parent": parent, "forks": forks})
    )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', default="lizadaly/forks",  help="An optional repo to use instead of the root repository")
    args = parser.parse_args()
    main(repo_name=args.repo)

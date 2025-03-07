from helper import GithubHelper, PaperMCHelper

if __name__ == "__main__":
    tags = GithubHelper.get_repo_tags()
    supportet_versions = []
    velocity_versions = PaperMCHelper.get_project_versions("velocity")

    for i, tag in enumerate(tags):
        supportet_versions.append(tag[1:])

    for version in velocity_versions:
        if version not in supportet_versions:
            title = f"New Velocity version {version}!"
            open_issues = GithubHelper.get_open_issues()
            create_issue = True

            for issue in open_issues:
                if title in issue["title"]:
                    print(f"Version {version} is already reported!")
                    create_issue = False
                    break

            if create_issue:
                body = f"Version {version} is not supported by this repository!"
                GithubHelper.create_issue(title, body, ["Endkind"], ["update"])

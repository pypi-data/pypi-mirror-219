"""gitpr cli"""
import logging
import argparse
import subprocess
import boto3
import botocore
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_current_repository():
    """get current repository"""
    try:
        # repo_output = subprocess.run(
        #     ["git", "rev-parse", "--show-toplevel"], check=False
        # )
        # repo_output = str(repo_output)
        # repo_name = repo_output
        # repo_name = repo_name.rsplit("/", 1)[-1]

        branch_output = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        )
        branch_name = branch_output.decode().strip()
        return branch_name

    except subprocess.CalledProcessError:
        logging.error(
            "could not get repo name, please check if you are inside a git repository"
        )


def create_pull_request(repo, branch_name, args):
    """create pull request"""
    cc_client = boto3.client("codecommit")
    print(branch_name)
    try:
        cc_client.create_pull_request(
            title=args.title,
            description=args.description,
            targets=[
                {
                    "repositoryName": repo,
                    "sourceReference": branch_name,  # args.source_branch,
                    "destinationReference": args.target_branch,
                }
            ],
        )
        logging.info("PR Created")
    except botocore.exceptions.ClientError as error:
        raise error


def main():
    """main"""
    parser = argparse.ArgumentParser(description="codecommit command line parameter")

    # parser.add_argument("-r", "--repository", help="repository name")
    parser.add_argument("-sb", "--source_branch", help="enter source branch")
    parser.add_argument(
        "-tb", "--target_branch", help="enter target branch", default="main"
    )
    parser.add_argument(
        "-t", "--title", help="title of the pull request", required=True
    )
    parser.add_argument(
        "-desc", "--description", help="Pull Request Description Message", required=True
    )

    args = parser.parse_args()

    branch_name = get_current_repository()
    if branch_name:
        repository_name = (os.path.basename(os.getcwd())).strip("'")

        create_pull_request(repository_name, branch_name, args)
    # else:
    #     logger.error("")


if __name__ == "__main__":
    main()

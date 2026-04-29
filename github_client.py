import requests
from config import Config

class GitHubClient:
    def __init__(self):
        self.token = Config.GITHUB_TOKEN
        self.headers = {"Authorization": f"token {self.token}"} if self.token else {}

    def get_pr_diff(self, repo_owner: str, repo_name: str, pr_number: int) -> str:
        url = f"https://patch-diff.githubusercontent.com/raw/{repo_owner}/{repo_name}/pull/{pr_number}.diff"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.text

    def post_comment(self, repo_owner: str, repo_name: str, pr_number: int, body: str) -> bool:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments"
        resp = requests.post(url, headers=self.headers, json={"body": body})
        return resp.status_code == 201

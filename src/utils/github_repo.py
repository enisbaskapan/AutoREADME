import requests
import base64
from typing import Optional


class GitHubRepo:
    """Helper class for interacting with GitHub API"""

    def __init__(self, owner: str, repo: str, token: Optional[str] = None):
        self.owner = owner
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            self.headers["Authorization"] = f"token {token}"

    def get_tree(self, recursive: bool = True) -> dict:
        """Get repository tree structure"""
        try:
            repo_info = requests.get(self.base_url, headers=self.headers).json()
            default_branch = repo_info.get("default_branch", "main")

            url = f"{self.base_url}/git/trees/{default_branch}"
            if recursive:
                url += "?recursive=1"

            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_file_content(self, path: str) -> str:
        """Get content of a specific file"""
        try:
            url = f"{self.base_url}/contents/{path}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            if data.get("encoding") == "base64":
                content = base64.b64decode(data["content"]).decode("utf-8")
                return content
            return data.get("content", "")
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def get_repo_info(self) -> dict:
        """Get repository metadata"""
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


def parse_github_url(url: str) -> tuple:
    """Parse GitHub URL to extract owner and repo name"""
    url = url.strip().rstrip("/")

    if url.endswith(".git"):
        url = url[:-4]

    url = url.replace("https://", "").replace("http://", "")

    if url.startswith("github.com/"):
        url = url[11:]

    parts = url.split("/")
    if len(parts) >= 2:
        return parts[0], parts[1]

    raise ValueError(f"Invalid GitHub URL: {url}")

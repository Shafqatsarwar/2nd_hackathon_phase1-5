"""
GitHub MCP Tools for the Todo Application
Provides integration with GitHub services through MCP
"""
from typing import Dict, Optional
import requests
import os
from dataclasses import dataclass


@dataclass
class GitHubConfig:
    """Configuration for GitHub API access"""
    token: str
    owner: str
    repo: str


class GitHubMCPTools:
    """MCP Tools for GitHub integration"""

    def __init__(self, get_session_func=None):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_owner = os.getenv("GITHUB_OWNER", "")
        self.github_repo = os.getenv("GITHUB_REPO", "")

        # Base URL for GitHub API
        self.base_url = "https://api.github.com"

        # Headers for API requests
        self.headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Evolution-of-Todo-App"
        } if self.github_token else {}

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make a request to the GitHub API"""
        if not self.github_token:
            return {"error": "GITHUB_TOKEN environment variable not set"}

        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=self.headers, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=self.headers)
            elif method.upper() == "PATCH":
                response = requests.patch(url, headers=self.headers, json=data)
            else:
                return {"error": f"Unsupported HTTP method: {method}"}

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"GitHub API request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    def create_issue(self, title: str, body: str = "", labels: Optional[list] = None) -> Dict:
        """
        Create a GitHub issue in the configured repository
        """
        if not self.github_owner or not self.github_repo:
            return {"error": "GITHUB_OWNER and GITHUB_REPO environment variables must be set"}

        data = {
            "title": title,
            "body": body,
            "labels": labels or []
        }

        endpoint = f"/repos/{self.github_owner}/{self.github_repo}/issues"
        return self._make_request("POST", endpoint, data)

    def list_issues(self, state: str = "open", labels: Optional[str] = None) -> Dict:
        """
        List GitHub issues from the configured repository
        """
        if not self.github_owner or not self.github_repo:
            return {"error": "GITHUB_OWNER and GITHUB_REPO environment variables must be set"}

        params = {"state": state}
        if labels:
            params["labels"] = labels

        # Build query string manually
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        endpoint = f"/repos/{self.github_owner}/{self.github_repo}/issues"
        if query_string:
            endpoint += f"?{query_string}"

        return self._make_request("GET", endpoint)

    def create_pull_request(self, title: str, body: str, head: str, base: str = "main") -> Dict:
        """
        Create a GitHub pull request in the configured repository
        """
        if not self.github_owner or not self.github_repo:
            return {"error": "GITHUB_OWNER and GITHUB_REPO environment variables must be set"}

        data = {
            "title": title,
            "body": body,
            "head": head,
            "base": base
        }

        endpoint = f"/repos/{self.github_owner}/{self.github_repo}/pulls"
        return self._make_request("POST", endpoint, data)

    def get_repo_info(self) -> Dict:
        """
        Get information about the configured repository
        """
        if not self.github_owner or not self.github_repo:
            return {"error": "GITHUB_OWNER and GITHUB_REPO environment variables must be set"}

        endpoint = f"/repos/{self.github_owner}/{self.github_repo}"
        return self._make_request("GET", endpoint)

    def list_repo_contents(self, path: str = "/") -> Dict:
        """
        List contents of the repository at the specified path
        """
        if not self.github_owner or not self.github_repo:
            return {"error": "GITHUB_OWNER and GITHUB_REPO environment variables must be set"}

        endpoint = f"/repos/{self.github_owner}/{self.github_repo}/contents{path}"
        return self._make_request("GET", endpoint)

    def create_gist(self, description: str, files: Dict[str, Dict[str, str]], public: bool = True) -> Dict:
        """
        Create a GitHub gist
        """
        data = {
            "description": description,
            "public": public,
            "files": files
        }

        endpoint = "/gists"
        return self._make_request("POST", endpoint, data)

    def get_user_info(self) -> Dict:
        """
        Get information about the authenticated GitHub user
        """
        endpoint = "/user"
        return self._make_request("GET", endpoint)


# Define the GitHub tools for MCP
GITHUB_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_github_issue",
            "description": "Create a GitHub issue in the project repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the issue"},
                    "body": {"type": "string", "description": "Body/description of the issue (optional)"},
                    "labels": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Labels to apply to the issue (optional)"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_github_issues",
            "description": "List GitHub issues from the project repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "enum": ["open", "closed", "all"],
                        "default": "open",
                        "description": "State of issues to list"
                    },
                    "labels": {"type": "string", "description": "Comma-separated list of labels to filter by (optional)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_github_pull_request",
            "description": "Create a GitHub pull request in the project repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the pull request"},
                    "body": {"type": "string", "description": "Body/description of the pull request (optional)"},
                    "head": {"type": "string", "description": "Source branch name"},
                    "base": {"type": "string", "default": "main", "description": "Target branch name (default: main)"}
                },
                "required": ["title", "head"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_github_repo_info",
            "description": "Get information about the GitHub repository",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_github_repo_contents",
            "description": "List contents of the GitHub repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "default": "/", "description": "Path in the repository to list (default: /)"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_github_gist",
            "description": "Create a GitHub gist with specified content",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "Description of the gist"},
                    "files": {
                        "type": "object",
                        "description": "Dictionary of file names to file content objects",
                        "additionalProperties": {
                            "type": "object",
                            "properties": {
                                "content": {"type": "string", "description": "Content of the file"}
                            },
                            "required": ["content"]
                        }
                    },
                    "public": {"type": "boolean", "default": True, "description": "Whether the gist should be public (default: true)"}
                },
                "required": ["description", "files"]
            }
        }
    }
]
"""Class that can fetch content of a file and push new commit with content"""
import base64
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


class GitHubHandler:
    def __init__(self, input_filename: str, repository: str, branch: str):
        self.input_filename = input_filename
        self.repository = repository
        self.branch = branch
        self.url = f"https://api.github.com/repos/{repository}/contents/{input_filename}"
        self.header, self.content, self.sha = None, None, None

    def fetch_content(self) -> str:
        """Get content of input filename

        Returns
        -------
        content: str
            The content of the page that is requested
        """
        token = os.getenv("GITHUB_ACCESS_TOKEN")
        data = requests.get(f"{self.url}?ref={self.branch}", headers={"Authorization": f"token {token}"}).json()
        self.sha = data["sha"]

        return base64.b64decode(data["content"]).decode("utf-8")

    def push(self, content: str):
        """
        Commits and pushes header + content to GitHub

        Parameters
        ----------
        content: str
            The content of the page that will be pushed to self.input_filename
        """
        # necessary to create valid message
        content = base64.encodebytes(content.encode("utf-8")).decode("utf-8")

        # create message
        message = json.dumps(
            {
                "message": "Update bookmarks",
                "branch": self.branch,
                "content": content,
                "sha": self.sha,
            }
        )

        # push content to GitHub
        print("Pushing content to GitHub..")
        response = requests.put(
            self.url,
            data=message,
            headers={
                "Content-Type": "application/json",
                "Authorization": "token " + os.getenv("GITHUB_ACCESS_TOKEN"),
            },
        )

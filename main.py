"""
Add pocket bookmark to a specified file on GitHub
"""
import logging
import click
from typing import Optional
from urllib.parse import urlparse
from datetime import datetime
from github_handler import GitHubHandler
from pocket_handler import PocketHandler


@click.command()
@click.option(
    "-i",
    "--input-filename",
    type=click.STRING,
    required=True,
    help="The name of the file that you want to update, e.g. 'bookmarks.html'",
)
@click.option(
    "-r",
    "--repository",
    type=click.STRING,
    required=True,
    help="The repository where the file is located, {username}/{repository_name}",
)
@click.option(
    "-b",
    "--branch",
    type=click.STRING,
    required=False,
    default="master",
    help="The branch where the file should be updated. Defaults to master",
)
def main(input_filename: str, repository: str, branch: Optional[str] = "master"):
    """
    Main function to run. Adds new bookmarks from Pocket to bookmarks page

    Parameters
    ----------
    input_filename: str
        The name of the file that you want to update, e.g. 'bookmarks.html'
    repository: str
        The repository where the file is located, {username}/{repository_name}
    branch: str = "master"
        The branch where the file should be updated. Defaults to master
    """
    # get urls and titles from pocket
    urls, titles = PocketHandler().get_urls_titles()
    # get page content from GitHub
    handler = GitHubHandler(input_filename, repository, branch)
    original_content = handler.fetch_content()
    content = original_content
    # add url and title to content page
    for url, title in zip(urls, titles):
        print(url, title)
        content = add_bookmark(content, url, title)
    # push content
    if original_content != content:
        handler.push(content)


def add_bookmark(all_content: str, bookmark_url: str, title: str) -> str:
    """
    Adds link with bookmark url and title to content

    Parameters
    ----------
    all_content: str
        The entire content, header should end with </h1>
    bookmark_url: str
        The url that will be added as a link (a href={bookmark_url})
    title: str
        The title that will be displayed as a link
    
    Returns
    -------
    The content with the new bookmark added after the header
    """
    # separate header from content
    header, content = all_content.split("<ul>")
    # if link already added, return original content
    if bookmark_url in content:
        print("Bookmark added already")
        return all_content
    # add bookmark
    content = (
        f'\n<li><a href="{bookmark_url}" target="_blank">{title}</a><br>{urlparse(bookmark_url).netloc} - {datetime.now().strftime("%Y-%m-%d")}</li>'
        + content
    )
    return header + "<ul>" + content


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    main()  # pylint: disable=no-value-for-parameter

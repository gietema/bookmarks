"""
Add bookmark to gietema.github.io/bookmarks
"""
import logging
import click
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
def main(input_filename: str, repository: str, branch: str = "master"):
    urls, titles = PocketHandler().get_urls_titles()
    for url, title in zip(urls, titles):
        print(url, title)
        handler = GitHubHandler(input_filename, repository, branch)
        content = handler.fetch_content()
        content_with_bookmark = add_bookmark(content, url, title)
        if content == content_with_bookmark:
            print("Bookmark already added")
            continue
        handler.push(content_with_bookmark)


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
        return all_content
    # add bookmark
    content = f'\n<li><a href="{bookmark_url}" target="_blank">{title}</a><br>{urlparse(bookmark_url).netloc} - {datetime.now().strftime("%Y-%m-%d")}</li>' + content
    return header + "<ul>" + content


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    main()  # pylint: disable=no-value-for-parameter

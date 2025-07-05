import io
import os
import zipfile
from typing import Dict

import dotenv
import requests

from repo2md.utils import LOGGER

dotenv.load_dotenv(dotenv_path=dotenv.find_dotenv())

API_URL = "https://api.github.com/repos"


def get_repo_info(
    repo: str,
    git_owner: str = os.environ.get("GIT_OWNER"),
    git_token: str = os.getenv("GIT_TOKEN"),
) -> Dict[str, str]:
    """Fetches the default branch and language of a GitHub repository.

    Args:
        repo: The name of the repository.
        git_owner: The owner of the repository. Defaults to the environment variable GIT_OWNER.
        git_token: GitHub token for authentication. Defaults to the environment variable

    Returns:
        Dict[str, str]:
        A dictionary containing the default branch and language of the repository.
    """
    LOGGER.info("Fetching default branch for %s/%s...", git_owner, repo)
    url = f"{API_URL}/{git_owner}/{repo}"
    response = requests.get(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {git_token}",
        },
    )
    assert response.ok, response.text
    data = response.json()
    return {"branch": data.get("default_branch"), "language": data.get("language")}


def make_request(
    url: str, git_token: str = os.getenv("GIT_TOKEN")
) -> requests.Response:
    """Makes a GET request to the specified URL with the configured headers.

    Args:
        url: The URL to make the request to.
        git_token: GitHub token for authentication. Defaults to the environment variable.

    Returns:
        requests.Response: The response object from the GET request.
    """
    for attempt in range(5):
        LOGGER.debug("Attempt %d to fetch %s", attempt + 1, url)
        try:
            response = requests.get(
                url,
                headers={
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"Bearer {git_token}",
                },
            )
            assert response.ok, response.text
        except requests.exceptions.RequestException as error:
            LOGGER.error(error)
            LOGGER.warning("Request failed on attempt %d, retrying...", attempt + 1)
            continue
        return response
    raise RuntimeError(f"Request failed on {url}")


def download_and_extract(
    repo: str,
    dest_dir: str,
    branch: str = None,
    git_owner: str = os.environ.get("GIT_OWNER"),
    git_token: str = os.getenv("GIT_TOKEN"),
) -> Dict[str, str]:
    """Downloads a GitHub repository as a zip file and extracts it to the specified directory.

    Args:
        repo: Repository name.
        dest_dir: Destination directory where the repository will be extracted.
        branch: Branch name to download. If not specified, the default branch will be used.
        git_owner: Owner of the repository. Defaults to the environment variable GIT_OWNER.
        git_token: GitHub token for authentication. Defaults to the environment variable.

    Returns:
        str:
        True path to the extracted repository directory.
    """
    repo_info = get_repo_info(repo=repo, git_token=git_token)
    url = f"{API_URL}/{git_owner}/{repo}/zipball/{branch or repo_info['branch']}"
    LOGGER.info("Downloading '%s/%s' to '%s'", git_owner, repo, dest_dir)
    LOGGER.debug("Download successful, unzipping...")
    response = make_request(url=url, git_token=git_token)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(dest_dir)
        subdir = zip_ref.namelist()[0].split("/")[0]
    LOGGER.debug(f"Repository unzipped to: {dest_dir}")
    true_path = os.path.join(dest_dir, repo)
    os.rename(os.path.join(dest_dir, subdir), os.path.join(dest_dir, repo))
    return {"path": true_path, "language": repo_info["language"]}

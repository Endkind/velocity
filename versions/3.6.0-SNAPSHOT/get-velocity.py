#!/usr/bin/env python3

import argparse
import os
from typing import Final

import requests
from result import Err, Ok, Result, is_err

# region Configuration
PROJECT: Final[str] = "velocity"
DISPLAY_NAME: Final[str] = "Velocity"
BASE_URL: Final[str] = f"https://fill.papermc.io/v3/projects/{PROJECT}"
# endregion


def main():
    parser = argparse.ArgumentParser(
        description=f"{DISPLAY_NAME} Download Script - Version and Build Parameters"
    )

    parser.add_argument(
        "--version",
        type=str,
        default=os.environ.get("VERSION", "latest"),
        help=f'{DISPLAY_NAME} Version (Default: environment variable VERSION or "latest")',
    )

    parser.add_argument(
        "--build",
        type=str,
        default=os.environ.get("BUILD", "latest"),
        help=f'{DISPLAY_NAME} Build Number (Default: environment variable BUILD or "latest")',
    )

    parser.add_argument(
        "--output",
        type=str,
        default="server.jar",
        help="Output file path (Default: server.jar)",
    )

    args = parser.parse_args()

    if args.version == "latest":
        version_result = get_latest_version()
        if is_err(version_result):
            print(f"Error: {version_result.unwrap_err()}")
            exit(1)
        version = version_result.unwrap()
    else:
        version = args.version

    build = args.build

    print(f"Version: {version}")
    print(f"Build: {build}")

    download_result = download_server_jar(version, build, args.output)
    if is_err(download_result):
        print(f"Error: {download_result.unwrap_err()}")
        exit(1)


def download_server_jar(
    version: str, build: str, output: str = "server.jar"
) -> Result[None, str]:
    download_meta_url = f"{BASE_URL}/versions/{version}/builds/{build}"  #

    try:
        response = requests.get(download_meta_url)
        response.raise_for_status()
        data = response.json()
        download_url = data["downloads"]["server:default"]["url"]

        output_dir = os.path.dirname(output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        response = requests.get(download_url)
        response.raise_for_status()

        with open(output, "wb") as f:
            f.write(response.content)

        print(f"Downloaded: {os.path.basename(output)}")
        return Ok(None)
    except Exception as e:
        return Err(f"Error downloading: {e}")


def get_latest_version() -> Result[str, str]:
    versions = get_all_versions()

    if versions.is_err():
        return Err(versions.unwrap_err())

    versions = versions.unwrap()

    index = 0

    while not has_builds(versions[index]).unwrap_or(False):
        index += 1
        if index >= len(versions):
            return Err("No versions with builds found")

    if len(versions) == 0:
        return Err("No versions found")

    return Ok(versions[index])


def get_all_versions() -> Result[list[str], str]:
    try:
        response = requests.get(BASE_URL)
    except requests.RequestException as error:
        return Err(
            f"Failed to fetch versions for project {PROJECT}. Request error: {error}"
        )

    if response.status_code != 200:
        return Err(
            f"Failed to fetch versions for project {PROJECT}. Status code: {response.status_code}"
        )

    try:
        payload = response.json()
    except ValueError as error:
        return Err(
            f"Failed to fetch versions for project {PROJECT}. Invalid JSON response: {error}"
        )

    versions_by_release = payload.get("versions")
    if not isinstance(versions_by_release, dict):
        return Err(
            f"Failed to fetch versions for project {PROJECT}. Invalid response shape: missing or invalid 'versions' object"
        )

    all_versions = []

    for release, versions in versions_by_release.items():
        if not isinstance(versions, list) or not all(
            isinstance(version, str) for version in versions
        ):
            return Err(
                f"Failed to fetch versions for project {PROJECT}. Invalid versions list for release '{release}'"
            )

        all_versions.extend(versions)

    return Ok(all_versions)


def has_builds(version: str) -> Result[bool, str]:
    print(version)
    try:
        response = requests.get(f"{BASE_URL}/versions/{version}")
        response.raise_for_status()
        data = response.json()
        builds = data.get("builds", [])
        return Ok(len(builds) > 0)
    except Exception as e:
        return Err(f"Error checking builds for version {version}: {e}")


if __name__ == "__main__":
    main()

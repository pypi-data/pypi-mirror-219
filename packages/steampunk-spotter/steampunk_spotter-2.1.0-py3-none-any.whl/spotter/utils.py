"""Provide utility functions that can be used as helpers throughout the code."""

import argparse
import sys
from urllib.parse import urlparse

import pkg_resources


def get_current_cli_version() -> str:
    """
    Retrieve current version of Steampunk Spotter CLI (steampunk-spotter Python package).

    :return: Version string
    """
    try:
        return pkg_resources.get_distribution("steampunk-spotter").version
    except pkg_resources.DistributionNotFound as e:
        print(f"Error when retrieving current steampunk-spotter version: {e}", file=sys.stderr)
        sys.exit(2)


def validate_url(url: str) -> str:
    """
    Validate URL.

    :param url: URL to validate
    :return: The same URL as input
    """
    parsed_url = urlparse(url)
    supported_url_schemes = ("http", "https")
    if parsed_url.scheme not in supported_url_schemes:
        raise argparse.ArgumentTypeError(
            f"URL '{url}' has an invalid URL scheme '{parsed_url.scheme}', "
            f"supported are: {', '.join(supported_url_schemes)}."
        )

    if len(url) > 2048:
        raise argparse.ArgumentTypeError(f"URL '{url}' exceeds maximum length of 2048 characters.")

    if not parsed_url.netloc:
        raise argparse.ArgumentTypeError(f"No URL domain specified in '{url}'.")

    return url

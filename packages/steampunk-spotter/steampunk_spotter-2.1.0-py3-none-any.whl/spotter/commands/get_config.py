"""Provide get-config CLI command."""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

from spotter.api import ApiClient
from spotter.storage import Storage


def add_parser(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    """
    Add a new parser for get-config command to subparsers.

    :param subparsers: Subparsers action
    """
    parser = subparsers.add_parser(
        "get-config", help="Get configuration from organization",
        description="Print organization-level file with configuration (e.g., for enforcing and skipping checks)"
    )
    parser.add_argument(
        "--organization-id", type=str,
        help="UUID of an existing Steampunk Spotter organization to get configuration from "
             "(default organization will be used if not specified)"
    )
    parser.set_defaults(func=_parser_callback)


def _parser_callback(args: argparse.Namespace) -> None:
    """
    Execute callback for get-config command.

    :param args: Argparse arguments
    """
    api_endpoint = args.endpoint or os.environ.get("SPOTTER_ENDPOINT", None)
    storage_path = args.storage_path or Storage.DEFAULT_PATH
    api_token = args.api_token or os.environ.get("SPOTTER_API_TOKEN")
    username = args.username or os.environ.get("SPOTTER_USERNAME")
    password = args.password or os.environ.get("SPOTTER_PASSWORD")
    debug = args.debug

    get_config(api_endpoint, storage_path, api_token, username, password, args.organization_id, debug=debug)


def _debug_print_project_and_org(api_client: ApiClient, organization_id: Optional[str]) -> None:
    if organization_id is not None:
        api_client.debug_print("Getting configuration for organization id {}", organization_id)
        api_client.debug_organization(organization_id)
    else:
        api_client.debug_print("Getting configuration for default organization")
        api_client.debug_my_default_organization()


# pylint: disable=too-many-arguments,too-many-locals,too-many-branches
def get_config(api_endpoint: Optional[str], storage_path: Path, api_token: Optional[str], username: Optional[str],
               password: Optional[str], organization_id: Optional[str], debug: bool = False) -> None:
    """
    Get configuration file for organization.

    By default, this will print configuration from the default organization.

    :param api_endpoint: Steampunk Spotter API endpoint
    :param storage_path: Path to storage
    :param api_token: Steampunk Spotter API token
    :param username: Steampunk Spotter username
    :param password: Steampunk Spotter password
    :param organization_id: UUID of an existing Steampunk Spotter organization to get configuration from
    :param debug: Enable debug mode
    """
    storage = Storage(storage_path)

    # TODO: extract this to a separate configuration component along with other configuration file options
    if api_endpoint is None:
        if storage.exists("spotter.json"):
            storage_configuration_json = storage.read_json("spotter.json")
            endpoint = storage_configuration_json.get("endpoint", ApiClient.DEFAULT_ENDPOINT)
        else:
            endpoint = ApiClient.DEFAULT_ENDPOINT
    else:
        endpoint = api_endpoint

    api_client = ApiClient(endpoint, storage, api_token, username, password, debug=debug)
    api_client.debug_print_me()
    _debug_print_project_and_org(api_client, organization_id)
    if organization_id:
        response = api_client.get(f"/v3/configuration/?organization={organization_id}")
    else:
        response = api_client.get("/v3/configuration/")
    if not response.ok:
        print(api_client.format_api_error(response), file=sys.stderr)
        sys.exit(2)

    try:
        configuration_json = response.json()
        print(json.dumps(configuration_json, indent=2))
    except json.JSONDecodeError as e:
        print(f"Error: scan result cannot be converted to JSON: {str(e)}", file=sys.stderr)
        sys.exit(2)

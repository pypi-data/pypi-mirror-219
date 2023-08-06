"""Provide set-config CLI command."""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

from pydantic.json import pydantic_encoder

from spotter.api import ApiClient
from spotter.environment import Environment
from spotter.storage import Storage


def add_parser(subparsers: "argparse._SubParsersAction[argparse.ArgumentParser]") -> None:
    """
    Add a new parser for set-config command to subparsers.

    :param subparsers: Subparsers action
    """
    parser = subparsers.add_parser(
        "set-config", help="Set configuration file for organization",
        description="Set organization-level file with configuration (e.g., for enforcing and skipping checks)"
    )
    parser.add_argument(
        "--organization-id", type=str,
        help="UUID of an existing Steampunk Spotter organization to set configuration for "
             "(default organization will be used if not specified)"
    )
    parser.add_argument(
        "config_path", type=lambda p: Path(p).absolute(),
        help="Path to the configuration file (JSON/YAML)"
    )
    parser.set_defaults(func=_parser_callback)


def _parser_callback(args: argparse.Namespace) -> None:
    """
    Execute callback for set-config command.

    :param args: Argparse arguments
    """
    api_endpoint = args.endpoint or os.environ.get("SPOTTER_ENDPOINT", None)
    storage_path = args.storage_path or Storage.DEFAULT_PATH
    api_token = args.api_token or os.environ.get("SPOTTER_API_TOKEN")
    username = args.username or os.environ.get("SPOTTER_USERNAME")
    password = args.password or os.environ.get("SPOTTER_PASSWORD")
    debug = args.debug

    config_path: Path = args.config_path
    if not config_path.exists():
        print(f"Error: Path at {config_path} does not exist.", file=sys.stderr)
        sys.exit(2)
    if not config_path.is_file():
        print(f"Error: Path at {config_path} is not a valid file.", file=sys.stderr)
        sys.exit(2)

    set_config(
        api_endpoint, storage_path, api_token, username, password, args.organization_id, config_path,
        debug=debug
    )


def _debug_print_project_and_org(api_client: ApiClient, organization_id: Optional[str]) -> None:
    if organization_id is not None:
        api_client.debug_print("Setting configuration for organization id {}", organization_id)
        api_client.debug_organization(organization_id)
    else:
        api_client.debug_print("Setting configuration for default organization")
        api_client.debug_my_default_organization()


# pylint: disable=too-many-arguments,too-many-locals,too-many-branches
def set_config(api_endpoint: Optional[str], storage_path: Path, api_token: Optional[str], username: Optional[str],
               password: Optional[str], organization_id: Optional[str],
               config_path: Path, debug: bool = False) -> None:
    """
    Set configuration file for organization.

    By default, this will set configuration for the default organization.

    :param api_endpoint: Steampunk Spotter API endpoint
    :param storage_path: Path to storage
    :param api_token: Steampunk Spotter API token
    :param username: Steampunk Spotter username
    :param password: Steampunk Spotter password
    :param organization_id: UUID of an existing Steampunk Spotter organization to set configuration for
    :param config_path: Path to the configuration file (JSON/YAML)
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

    spotter_noqa = []
    environment = Environment.from_config_file(config_path)
    if environment.cli_scan_args:
        skip_checks = environment.cli_scan_args.get("skip_checks", [])
        for skip_check in skip_checks:
            skip_check_dict = pydantic_encoder(skip_check)
            skip_check_dict["type"] = "skip"
            spotter_noqa.append(skip_check_dict)

        enforce_checks = environment.cli_scan_args.get("enforce_checks", [])
        for enforce_check in enforce_checks:
            enforce_check_dict = pydantic_encoder(enforce_check)
            enforce_check_dict["type"] = "enforce"
            spotter_noqa.append(enforce_check_dict)

    api_client = ApiClient(endpoint, storage, api_token, username, password, debug=debug)
    api_client.debug_print_me()
    _debug_print_project_and_org(api_client, organization_id)
    if organization_id:
        response = api_client.patch(
            f"/v3/configuration/?organization={organization_id}", payload={"spotter_noqa": spotter_noqa}
        )
    else:
        response = api_client.patch("/v3/configuration/", payload={"spotter_noqa": spotter_noqa})
    if not response.ok:
        print(api_client.format_api_error(response), file=sys.stderr)
        sys.exit(2)

    print("Configuration successfully set.")

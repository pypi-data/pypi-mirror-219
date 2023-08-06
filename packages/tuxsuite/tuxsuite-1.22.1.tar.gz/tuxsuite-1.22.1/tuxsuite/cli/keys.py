# -*- coding: utf-8 -*-

import sys
import json

from tuxsuite.cli.requests import (
    delete,
    get,
    post,
    put,
)
from tuxsuite.cli.utils import error

# keys available kinds with their arguments
KIND = {
    "pat": ["domain", "username", "token"],
    "variables": ["keyname", "type", "value"],
}


def display_keys(keys):
    for kind in KIND:
        kind_keys = keys.get(kind)
        if kind_keys:
            print(f"{kind} keys:\n")
            print("{:<10} {:<25} {:<25} {:<10}\n".format(*(["S.no"] + KIND[kind])))
            for count, item in enumerate(kind_keys, start=1):
                values = [item[val] for val in KIND[kind]]
                print("{:<10} {:<25} {:<25} {:<10}".format(*([str(count)] + values)))
            print()


def check_required_cmdargs(kind, cmdargs, required_args=None):
    if required_args is None:
        required_args = KIND[kind]
    for item in required_args:
        if getattr(cmdargs, item) is None:
            error(f"--{item} is required for kind '{kind}'")


def handle_add(cmdargs, _, config):
    data = {"key": {}}
    kind = cmdargs.kind[0]
    url = f"/v1/groups/{config.group}/projects/{config.project}/keys"
    check_required_cmdargs(kind, cmdargs)
    data["kind"] = kind
    for item in KIND[kind]:
        data["key"][item] = getattr(cmdargs, item)

    ret = post(config, url, data=data)
    msg = (
        f"{cmdargs.domain}:{cmdargs.username}"
        if kind == "pat"
        else f"{cmdargs.keyname}:{cmdargs.type}"
    )

    if ret.status_code != 201:
        error(f"Failed to add '{kind}' key '{msg}'")
    else:
        print(f"'{kind}' key '{msg}' added")
        sys.exit(0)


def handle_get(cmdargs, _, config):
    url = f"/v1/groups/{config.group}/projects/{config.project}/keys"
    ret = get(config, url)

    if ret.status_code != 200:
        error("Failed to get the keys")
    else:
        keys = ret.json()
        if cmdargs.json:
            print(json.dumps(ret.json(), indent=True))
        else:
            print(f"ssh public key:\n\n{keys['ssh']['pub']}\n")
            display_keys(keys)
        sys.exit(0)


def handle_delete(cmdargs, _, config):
    data = {"key": {}}
    msg = ""
    kind = cmdargs.kind[0]
    url = f"/v1/groups/{config.group}/projects/{config.project}/keys"
    if kind == "pat":
        required_args = ["domain", "username"]
        msg = f"{cmdargs.domain}:{cmdargs.username}"
    elif kind == "variables":
        required_args = ["keyname"]
        msg = f"{cmdargs.keyname}"
    check_required_cmdargs(kind, cmdargs, required_args)
    data["kind"] = kind
    for item in required_args:
        data["key"][item] = getattr(cmdargs, item)

    ret = delete(config, url, data=data)
    if ret.status_code != 200:
        error(f"Failed to delete '{kind}' key '{msg}'")
    else:
        print(f"'{kind}' key '{msg}' deleted")
        sys.exit(0)


def handle_update(cmdargs, _, config):
    data = {"key": {}}
    kind = cmdargs.kind[0]
    url = f"/v1/groups/{config.group}/projects/{config.project}/keys"
    check_required_cmdargs(kind, cmdargs)
    data["kind"] = kind
    for item in KIND[kind]:
        data["key"][item] = getattr(cmdargs, item)

    msg = (
        f"{cmdargs.domain}:{cmdargs.username}"
        if kind == "pat"
        else f"{cmdargs.keyname}:{cmdargs.type}"
    )
    ret = put(config, url, data=data)

    if ret.status_code != 201:
        error(f"Failed to update '{kind}' key '{msg}'")
    else:
        print(f"'{kind}' key '{msg}' updated")
        sys.exit(0)


handlers = {
    "add": handle_add,
    "get": handle_get,
    "delete": handle_delete,
    "update": handle_update,
}


def keys_cmd_common_options(sp):
    sp.add_argument(
        "kind",
        choices=list(KIND),
        help="Kind of the key {pat}",
        nargs=1,
    )
    # keys kind arguments groups
    # kind: "pat" arguments
    pat_group = sp.add_argument_group("pat kind options")
    pat_group.add_argument(
        "--domain",
        help="Domain for the given key",
        default=None,
        type=str,
    )
    pat_group.add_argument(
        "--username",
        help="Username for the given key",
        default=None,
        type=str,
    )

    # kind: "variables" arguments
    variables_group = sp.add_argument_group("variables kind options")
    variables_group.add_argument(
        "--keyname", help="Keyname for the given key", default=None, type=str
    )

    return (pat_group, variables_group)


def keys_cmd_token_option(sp):
    sp.add_argument(
        "--token",
        help="Value of the Personal Access Token (PAT)",
        default=None,
        type=str,
    )


def keys_cmd_value_option(sp):
    sp.add_argument(
        "--value",
        help="Value of the variables key",
        default=None,
        type=str,
    )


def keys_cmd_type_options(sp):
    sp.add_argument(
        "--type",
        help="Type for the given key",
        choices=["file", "variable"],
        default=None,
        type=str,
    )


def setup_parser(parser):
    # "keys add"
    t = parser.add_parser("add")
    pat, variables = keys_cmd_common_options(t)
    keys_cmd_token_option(pat)
    keys_cmd_value_option(variables)
    keys_cmd_type_options(variables)

    # "keys get"
    t = parser.add_parser("get")
    t.add_argument(
        "--json",
        help="output json to stdout",
        default=False,
        action="store_true",
    )

    # "keys delete"
    t = parser.add_parser("delete")
    keys_cmd_common_options(t)

    # "keys update"
    t = parser.add_parser("update")
    pat, variables = keys_cmd_common_options(t)
    keys_cmd_token_option(pat)
    keys_cmd_value_option(variables)
    keys_cmd_type_options(variables)

    return sorted(parser._name_parser_map.keys())

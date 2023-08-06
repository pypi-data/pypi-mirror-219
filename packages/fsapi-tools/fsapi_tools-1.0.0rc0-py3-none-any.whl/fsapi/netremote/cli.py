# MIT License

# Copyright (c) 2023 MatrixEditor

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import argparse
import os
import re

from json import dump
from time import time

from fsapi.netremote.radiohttp import (
    FSDevice,
    CREATE_SESSION,
    GET,
    SET,
    LIST_GET_NEXT,
    netremote_request,
    is_list_class,
)
from fsapi.netremote.nodes import (
    BaseCreateSession,
    BaseSysInfoVersion,
    BaseSysInfoRadioId,
)
from fsapi.isu import isu_find_update, isu_get_update, isu_new_url
from fsapi.netremote import get_all_node_types, NodeList

RE_IPV4 = r"^\d{1,3}(.\d{1,3}){3}$"


def get_node_name(name):
    if name.startswith("netRemote."):
        return name

    return f"netRemote.{name}"


def delegate_explore(args: dict, radio: FSDevice):
    verbose = args["verbose"]
    exclude = args["exclude"].split(",")

    if verbose:
        print("\n[+] Starting to explore target host...")

    sid = netremote_request(CREATE_SESSION, BaseCreateSession, radio).content.value

    results = {}
    node_types = get_all_node_types()
    for name in node_types:
        node_type = node_types[name]
        if is_list_class(node_type):
            result = netremote_request(
                "LIST_GET_NEXT",
                node_type,
                radio,
                parameters={"maxItems": 100, "sid": sid},
            )
        else:
            result = netremote_request("GET", node_type, radio, parameters={"sid": sid})

        if result.status not in exclude and args["json"]:
            results[node_type.get_name()] = {
                "status": result.status,
                "result": result.to_json(),
            }
        if verbose:
            print("  - %s --> %s" % (node_type.get_name(), result.status))

    if args["json"]:
        name = "fsapi_exploration-%s.json" % time()
        with open(name, "w") as _res:
            dump(results, _res)
        if verbose:
            print("\n[+] Saved exlporation result to:", name)


def delegate_isu(args: dict, radio: FSDevice):
    verbose = args["verbose"]

    if args["find"]:
        # REVISIT: add not null checks
        mac = netremote_request("GET", BaseSysInfoRadioId, radio).content.value
        version = netremote_request("GET", BaseSysInfoVersion, radio).content.value

        values = version.split("_V")
        result = isu_find_update(mac, values[0], values[1], verbose)
        if not result or not result["update_present"]:
            print("\n[+] Generating current URL...")
            # This generation algorithm should return the right download URL
            url = isu_new_url(version)
            print("     - url:", url)
        else:
            print("[+] Found at least one Update:")
            for update in result["updates"]:
                print("    -", update)
                url = update.download_url

        path = args["collect"]
        if path:
            if path == "_":
                path = version
            if verbose:
                print(f"\n[+] Downloading update file to: {path}.isu.bin")
            isu_get_update(args["collect"] + "isu.bin", url, verbose=verbose)
            if verbose:
                print("[+] Download complete")
    elif args["file"]:
        path = args["target"]
        if verbose:
            print("\n[+] Downloading updates located in file:", path)

        try:
            os.mkdir("isu-download")
        except Exception:
            pass

        with open(path, "r", encoding="utf-8") as ufp:
            for fw_name in ufp.readlines():
                fw_name = fw_name.strip()
                if not fw_name:
                    continue

                url = isu_new_url(fw_name)
                if not url:
                    if verbose:
                        print("[-] Could not create download URL")
                    continue

                if verbose:
                    print(f" > Donwload of: isu-download/{fw_name}.isu.bin")
                    print(f'     ::url "{url}"')
                isu_get_update(f"isu-download/{fw_name}.isu.bin", url, verbose=verbose)
                if verbose:
                    print()
        if verbose:
            print("[+] Download complete")


def delegate_get(args: dict, radio: FSDevice):
    node_types = get_all_node_types()
    node = get_node_name(args["node"])

    if node not in node_types:
        print("[-] Undefined node:", node)
        exit(1)

    result = netremote_request(GET, node_types[node], radio)
    if result:
        print_result(node, result)
        if result.status == "FS_OK":
            print("     - value: %s" % (result.content.value))
            print("     - readonly: %s" % result.content.is_readonly())
            print("     - notifying: %s" % result.content.is_notifying())


def print_result(node, result):
    print("[+] fsapiResponse of %s:" % node)
    print("     - status: %s" % (result.status))


def delegate_set(args: dict, radio: FSDevice):
    node_types = get_all_node_types()
    node = get_node_name(args["node"])

    if node not in node_types:
        print("[-] Unknown node class")
    elif node_types[node].is_readonly():
        print("[-] Node is set to be read only. A SET-request is not possible.")
    else:
        params = {}
        for key in args["args"]:
            name, value = key.split(":")
            params[name] = value.strip('"')

        result = netremote_request(SET, node_types[node], radio, parameters=params)
        if result:
            print_result(node, result)
        else:
            print("[-] Failed to read response or to fetch url.")


def delegate_list(args: dict, radio: FSDevice):
    node_types = get_all_node_types()
    node = get_node_name(args["node"])

    if node not in node_types:
        print("[-] Unknown node class")
    else:
        params = {}
        for key in args["args"]:
            name, value = key.split(":")
            params[name] = value.strip('"')

        result = netremote_request(
            LIST_GET_NEXT, node_types[node], radio, parameters=params
        )
        if result:
            print_result(node, result)
        if result.status == "FS_OK":
            result_list: NodeList = result.content
            print("     - list: size=%d" % (result_list.size()))
            for item in result_list.get_items():
                print(f"         | {item.attr}")
        else:
            print("[-] Failed to read response or to fetch url.")


def main(cmd=None):
    parser = argparse.ArgumentParser(
        description="""
        A python implementation of the FSAPI with all possible nodes.

        You can execute the fsapi.isu or fsapi.ecmascript module
        by typing the same command but with their module name."""
    )
    subparsers = parser.add_subparsers(help="sub-commands:")

    explore_parser = subparsers.add_parser("explore", help="Node Exploration")
    explore_parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Saves information in JSON-format",
    )
    explore_parser.add_argument(
        "-E",
        "--exclude",
        type=str,
        default="",
        required=False,
        help="Exclude the following arguments from being analysed (if more that one, separate them with a comma)",
    )
    explore_parser.set_defaults(func=delegate_explore)

    isu_parser = subparsers.add_parser("isu", help="ISU Firmware Context")
    isu_parser.add_argument(
        "--find",
        action="store_true",
        required=False,
        default=False,
        help="Find an update for the specified host. If none was found a download URL for the current version will be generated.",
    )
    isu_parser.add_argument(
        "--collect",
        type=str,
        default=None,
        metavar="PATH",
        help="Collect the firmware to the specified path. (only together with --find)",
    )
    isu_parser.add_argument(
        "-F",
        "--file",
        action="store_true",
        default=False,
        help="Collect the firmware from the specified path.",
    )
    isu_parser.set_defaults(func=delegate_isu)

    get_parser = subparsers.add_parser("get", help="Request a simple property")
    get_parser.add_argument(
        "-n",
        "--node",
        required=True,
        help="The netremote package name. (format: sys.info.friendlyName)",
    )
    get_parser.set_defaults(func=delegate_get)

    set_parser = subparsers.add_parser(
        "set", help="Apply a value to a stored property."
    )
    set_parser.add_argument(
        "-n",
        "--node",
        required=True,
        help="The netremote package name. (format: sys.info.friendlyName)",
    )
    set_parser.add_argument(
        "--args",
        nargs="*",
        help="The arguments passed to the request. (format: --args arg:value [arg:value [...]]))",
    )
    set_parser.set_defaults(func=delegate_set)

    list_parser = subparsers.add_parser("list", help="Query property lists")
    list_parser.add_argument(
        "-n",
        "--node",
        required=True,
        help="The netremote package name. (format: sys.info.friendlyName)",
    )
    list_parser.add_argument(
        "--args",
        nargs="*",
        help="The arguments passed to the request. (format: --args arg:value [arg:value [...]]))",
    )

    list_parser.set_defaults(func=delegate_list)

    gb_group = parser.add_argument_group("Global options")
    gb_group.add_argument("target", type=str, help="The host address in IPv4 format.")
    gb_group.add_argument(
        "-W",
        "--pin",
        type=str,
        required=False,
        help="A PIN used by the device (default 1234).",
        default="1234",
    )
    gb_group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Prints useful information during the specified process.",
    )

    nspace = parser.parse_args(cmd).__dict__
    target = nspace["target"]
    verbose = nspace["verbose"]

    if not target or not re.match(RE_IPV4, target):
        if "file" not in nspace and not nspace["file"]:
            print("[-] Error: Invalid IPv4 or target host == null!")
            exit(1)

    radio = FSDevice(target, nspace["pin"])
    if verbose:
        print("[+] Setting up netremote with:", radio)
    nspace["func"](nspace, radio)

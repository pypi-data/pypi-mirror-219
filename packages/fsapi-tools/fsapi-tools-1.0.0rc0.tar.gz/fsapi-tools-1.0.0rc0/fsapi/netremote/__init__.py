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
from __future__ import annotations

__doc__ = """
The next module of this small API implementation focuses on the "FsNetRemoteLib". All
nodes presented here were converted from the Java source code of the app *"Medion Lifestream 2"*.

The script used for converting the code can be found `here`_. The source code was converted
to reduce the manual effort, as the final "nodes.py" file contained more than 4000 lines of code.

When querying a resource or attempting to set a value to a specific node, there is always a
status message that accompanies the response. The possible values for this status are:

+-------------------------+-------+-----------------------------------------------------------+
| Status                  | Body  | Description                                               |
+=========================+=======+===========================================================+
| `FS_OK`                 | True  | If everything goes right the status is set to `FS_OK`     |
+-------------------------+-------+-----------------------------------------------------------+
| `FS_PACKET_BAD`         | False | This status code will be returned if a value should be    |
|                         |       | applied to a read-only node.                              |
+-------------------------+-------+-----------------------------------------------------------+
| `FS_NODE_BLOCKED`       | False | Sometimes this status is given, maybe because the node    |
|                         |       | was deactivated on the device.                            |
+-------------------------+-------+-----------------------------------------------------------+
|`FS_NODE_DOES_NOT_EXIST` | False | As the name already states, the requested node is not     |
|                         |       | implemented on that device.                               |
+-------------------------+-------+-----------------------------------------------------------+
|`FS_TIMEOUT`             | False | The device takes too long to respond                      |
+-------------------------+-------+-----------------------------------------------------------+
| `FS_FAIL`               | False | If the parameters given in the url are mot matching the   |
|                         |       | node criteria, the request will fail.                     |
+-------------------------+-------+-----------------------------------------------------------+
"""

from fsapi.netremote.basenode import (
    NodeArg,
    NodeC,
    NodeE8,
    NodeInfo,
    NodeInteger,
    NodeList,
    NodeListItem,
    NodePrototype,
    NodeS16,
    NodeS32,
    NodeS8,
    NodeU,
    NodeU16,
    NodeU32,
    NodeU8,
    ARG_TYPE_C,
    ARG_TYPE_E8,
    ARG_TYPE_S16,
    ARG_TYPE_S32,
    ARG_TYPE_S8,
    ARG_TYPE_U,
    ARG_TYPE_U16,
    ARG_TYPE_U32,
    ARG_TYPE_U8,
)
from fsapi.netremote.radiohttp import (
    ApiResponse,
    FSDevice,
    NodeError,
    netremote_request,
    Get,
    Set,
    ListGet,
    ListGetNext,
    CreateSession,
    DeleteSession,
    is_list_class,
    GET_MULTIPLE,
    GET,
    SET,
    SET_MULTIPLE,
    LIST_GET,
    LIST_GET_NEXT,
    DELETE_SESSION,
    CREATE_SESSION,
    RADIO_HTTP_DEFAULT_PIN,
    FS_OK,
    FS_PACKET_BAD,
    FS_NODE_BLOCKED,
    FS_NODE_DOES_NOT_EXIST,
    FS_TIMEOUT,
    FS_FAIL,
)
from fsapi.netremote import nodes


def get_all_node_names() -> list[str]:
    """Returns all loaded node names."""
    names = []
    for key in nodes.__dict__:
        if "Base" in key:
            names.append(nodes.__dict__[key].get_name())
    return names


def get_all_node_types() -> dict[str, type]:
    """Returns all node names together with their class type.

    :return: all nodes mapped to their type
    :rtype: dict[str, type]
    """
    types = {}
    for key in nodes.__dict__:
        if "Base" in key:
            class_type = nodes.__dict__[key]
            types[class_type.get_name()] = class_type
    return types

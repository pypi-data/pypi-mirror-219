# SPDX-FileCopyrightText: 2023 Alex Lemna <git@alexanderlemna.com>
#
# SPDX-License-Identifier: MIT

import functools
import operator
from collections import UserDict, defaultdict
from typing import Any

_infinite_dict = lambda: defaultdict(_infinite_dict)


class AuldDict(UserDict):
    def __init__(self, dict=None, /, node_base_dict={}, **kwargs):
        self.__node_base_dict = AuldDict(node_base_dict)
        return super().__init__(dict, **kwargs)

    # def __getitem__(self, key: str) -> Any:
    #     if " " in key:
    #         key_chain = key.split(" ")
    #         # See explanation at: https://www.pythonmorsels.com/reduce/
    #         return functools.reduce(
    #             lambda access, value: access[value], key_chain, self.data
    #         )
    #     else:
    #         return super().__getitem__(key)

    # def __setitem__(self, key: str, item: Any) -> None:
    #     if item:
    #         pass
    #     else:
    #         item = self.__node_base_dict

    #     if " " in key:
    #         key_chain = key.split(" ")

    #         # # See explanation at: https://stackoverflow.com/a/12414913
    #         # d = lambda: defaultdict(_infinite_dict)
    #         # self.data = functools.reduce(operator.getitem, key_chain[:-1], d())
    #         # self.data[key_chain[-1]] = item
    #     else:
    #         return super().__setitem__(key, item)

    # def __delitem__(self, key: str) -> None:
    #     return super().__delitem__(key)

    # def __contains__(self, key: object) -> bool:
    #     return super().__contains__(key)

    def __missing__(self, key):
        d = AuldDict()
        self[key] = d
        return d


if __name__ == "__main__":
    # def cmd_foo():
    #     ...

    # key = "a b c d e f"
    # value = cmd_foo

    d = AuldDict(node_base_dict={"__foo__": 1, "__baz__": 2})
    d["foo"]["bar"]["baz"] = 1
    print(d)

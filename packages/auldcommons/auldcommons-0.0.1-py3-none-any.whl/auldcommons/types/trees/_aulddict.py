# SPDX-FileCopyrightText: 2023 Alex Lemna <git@alexanderlemna.com>
#
# SPDX-License-Identifier: MIT

import functools
import operator
import pprint
from collections import ChainMap, UserDict, defaultdict
from typing import Any


def set_arbitrary_nest(keys, value):
    """Creates a nested dict of arbitrary length.
    (source: https://stackoverflow.com/q/50932755)
    >>> keys = 1, 2, 3
    >>> value = 5
    result --> {1: {2: {3: 5}}}
    """

    it = iter(keys)
    last = next(it)
    res = {last: {}}
    lvl = res
    while True:
        try:
            k = next(it)
            lvl = lvl[last]
            lvl[k] = {}
            last = k
        except StopIteration:
            lvl[k] = value
            return res


def merge_dicts(dict1: dict, dict2: dict):
    """Merges two dictionaries while attempting to preserve any
    nested dictionaries."""
    for key, value in dict2.items():
        # if key doesn't exist, add it
        if key not in dict1.keys():
            dict1[key] = value

        # if key exists and both the old and new values are dicts,
        # enter recursively
        elif (
            key in dict1.keys()
            and isinstance(dict1[key], dict)
            and isinstance(dict2[key], dict)
        ):
            merge_dicts(dict1[key], dict2[key])

        # otherwise, overwrite the value in dict1
        elif key in dict1.keys():
            dict1[key] = dict2[key]

    return dict1


class AuldDict(UserDict):
    ...

    def __setitem__(self, key: Any, item: Any) -> None:
        def set_arbitrary_nest(keys, value):
            """Creates a nested dict of arbitrary length.
            (source: https://stackoverflow.com/q/50932755)
            >>> keys = 1, 2, 3
            >>> value = 5
            result --> {1: {2: {3: 5}}}
            """

            iterator = iter(keys)
            last = next(iterator)
            """latest key we've iterated on"""

            result = {last: {}}
            lvl = result
            while True:
                try:
                    k = next(iterator)
                    lvl = lvl[last]
                    lvl[k] = {}
                    last = k
                except StopIteration:
                    lvl[k] = value
                    return result

        return super().__setitem__(key, item)

    def pprint(self):
        """Pretty-print contents."""
        return pprint.pprint(self.data)


if __name__ == "__main__":
    print(set_arbitrary_nest(["foo", "baz", "bar", "bic", "yo"], 5))
    print()
    dict1 = {
        "foo": {
            "bar1": {},
            "bar2": {
                "baz2": {},
            },
        },
        "do": {"fo": {"__help__": "A message."}, "re": "A message"},
    }
    dict2 = {"foo": {"bar1": {"baz": {"qux": {}}}}, "do": {"re": {"me": {}}}}
    print(dict1 | dict2)
    print()
    pprint.pprint(merge_dicts(dict1, dict2))

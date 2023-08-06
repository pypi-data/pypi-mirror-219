# SPDX-FileCopyrightText: 2023 Alex Lemna <git@alexanderlemna.com>
#
# SPDX-License-Identifier: MIT

import re
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("auldcommons")
    __version_info__ = tuple(
        int(i) for i in __version__.split(".") if re.match("[0-9]+", i)
    )  # a tuple containing the numerical parts of the version
except PackageNotFoundError:
    # package is not installed
    pass

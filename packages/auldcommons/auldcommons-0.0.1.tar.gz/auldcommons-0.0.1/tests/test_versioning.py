# SPDX-FileCopyrightText: 2023 Alex Lemna <git@alexanderlemna.com>
#
# SPDX-License-Identifier: MIT

import auldcommons


def test_version():
    assert auldcommons.__version__


def test_versioninfo():
    assert auldcommons.__version_info__


if __name__ == "__main__":
    print(auldcommons.__version__)

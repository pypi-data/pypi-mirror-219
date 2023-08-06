<!--
SPDX-FileCopyrightText: 2023 Alex Lemna <git@alexanderlemna.com>

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Versioning

Since this project is a library of common modules, it'll be using an abbreviated Semantic Versioning format where each version follows the `MAJOR.PATCH` format. 

- Changes to the `MAJOR` version signal either breaking changes to the public API, dropping support for a release of Python (for example, dropping support for Python 3.9, etc.), or other significant changes.
- Changes to the `PATCH` version signal changes that are guarenteed to be API-identical to all other versions with the same major version.

Since this is a library designed primarily for one person's personal use, `MAJOR` version bumps may occur frequently.

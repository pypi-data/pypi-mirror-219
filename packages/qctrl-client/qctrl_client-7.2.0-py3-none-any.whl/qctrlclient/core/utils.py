# Copyright 2023 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

import sys
from importlib.metadata import (
    PackageNotFoundError,
    version,
)
from typing import Optional

import click


def get_installed_version(package: str) -> Optional[str]:
    """Get the installed version of the package. If
    the version cannot be found (e.g. package not installed)
    then None is returned.
    """
    try:
        pkg_version = version(package)

    except PackageNotFoundError:
        pkg_version = None

    return pkg_version


def show_error_message(error_message: str):
    """Displays the error message and stops execution."""
    click.echo(error_message, err=True)
    sys.exit(1)

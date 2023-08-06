# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import subprocess
import os

from . import cli
from .. import init_radstar, list_apps, shsplit

# -------------------------------------------------------------------------------------------------------------------- #

@cli.group('deps')
def deps_cli():
    ''' Dependency management. '''

# -------------------------------------------------------------------------------------------------------------------- #

@deps_cli.command()
def update():
    ''' Update and install Python dependencies. '''

    init_radstar(no_init=True)

    in_files = []
    for x in list_apps():
        x = os.path.join(x.dir, 'requirements.in')
        if os.path.exists(x):
            in_files.append(x)

    subprocess.check_call(
        shsplit('pip-compile --resolver=backtracking --allow-unsafe --generate-hashes --upgrade -o requirements.txt'
                ' --no-header') + in_files, cwd='/rs/project')

    subprocess.check_call(shsplit('python -m pip install -r requirements.txt --require-virtualenv'), cwd='/rs/project')

# -------------------------------------------------------------------------------------------------------------------- #

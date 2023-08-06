# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from rsrpc import json

from . import db, plugins, settings
from .application import get_app, list_apps
from .plugins import plugin
from .utils import attrs, camel_to_snake, getenv, panic, readfile, shsplit

# -------------------------------------------------------------------------------------------------------------------- #

def init_radstar(**kw):
    from . import application

    if application.radstar_app is not None:
        print('WARNING: radstar_init already called')
        return application.radstar_app

    # init core application
    application.init_app('core.core', **kw)

    # init main application
    application.radstar_app = application.init_app('main', **kw)

    return application.radstar_app

# -------------------------------------------------------------------------------------------------------------------- #

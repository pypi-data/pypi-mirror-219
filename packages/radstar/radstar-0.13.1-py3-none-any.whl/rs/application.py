# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from collections import OrderedDict
import importlib
import os

import yaml

# -------------------------------------------------------------------------------------------------------------------- #

radstar_app = None
radstar_apps = OrderedDict()

# -------------------------------------------------------------------------------------------------------------------- #

class Application:
    ''' ... '''

    def __init__(self, name: str):

        app_mod = importlib.import_module(name)

        self.name = name
        self.dir = str(app_mod.__path__[0])

        # load app manifest
        manifest = os.path.join(self.dir, 'app.yml')
        if os.path.isfile(manifest):
            with open(manifest) as f:
                self._manifest = yaml.safe_load(f)
        else:
            self._manifest = {}

        # XXX: remove before v1.0.0
        self.legacy_name = self._manifest.get('name') or name.split('.', 1)[-1]

    # ---------------------------------------------------------------------------------------------------------------- #

    def init_app(self, *, import_modules=[]):
        ''' continue initializing app, after dependencies has been initialized. '''
        # pylint: disable=dangerous-default-value

        # import auto import modules
        for mod in self.get_attr('auto_load', []):

            # named module, just import it
            if not mod.endswith('/'):
                self.import_module(mod)
                continue

            # directory import - import all modules in the directory
            mod, mod_dir = mod[:-1].replace('/', '.'), os.path.join(self.dir, mod[:-1])
            for fn in sorted(os.listdir(mod_dir)):

                if fn.startswith('_'):
                    continue

                if fn.endswith('.py'):
                    self.import_module(f'{mod}.{fn[:-3]}')

                elif (os.path.isdir(os.path.join(mod_dir, fn)) and
                        os.path.isfile(os.path.join(mod_dir, fn, '__init__.py'))):
                    self.import_module(f'{mod}.{fn}')

        # import context specific modules
        for mod in import_modules:
            self.import_module(mod)

    # ---------------------------------------------------------------------------------------------------------------- #

    def get_attr(self, key, default=None):
        ''' get attribute from app.yml manifest. key can include dots to reference sub-dicts. '''

        m = self._manifest
        parts = key.split('.')

        for part in parts[:-1]:
            m = m.get(part)
            if not isinstance(m, dict):
                return default

        return m.get(parts[-1], default)

    # ---------------------------------------------------------------------------------------------------------------- #

    def init_tables(self):

        db_mod = self.import_module('db')
        callback = getattr(db_mod, 'init_tables', None) if db_mod is not None else None

        from . import db
        with db.transaction():
            db.init_tables(self.name, callback)

    # ---------------------------------------------------------------------------------------------------------------- #

    def import_module(self, module):
        module = f'{self.name}.{module}'
        try:
            return importlib.import_module(module)
        except ModuleNotFoundError as e:
            if e.name == module:
                return None
            raise

    # ---------------------------------------------------------------------------------------------------------------- #

    def __repr__(self):
        return f'Application({self.name})'

# -------------------------------------------------------------------------------------------------------------------- #

def init_app(app_name: str, *, no_init: bool=False, **kw):

    # already initialized?
    if app_name in radstar_apps:
        return radstar_apps[app_name]

    # instantiate application
    app = Application(app_name)

    # init dependencies
    for d in app.get_attr('dependencies', []):
        init_app(d, no_init=no_init, **kw)

    # finialize application initialization
    if no_init is False:
        app.init_app(**kw)

    radstar_apps[app_name] = app
    return app

# -------------------------------------------------------------------------------------------------------------------- #

def get_app(app_name=None):
    return radstar_app if app_name is None else radstar_apps.get(app_name)

# -------------------------------------------------------------------------------------------------------------------- #

def list_apps():
    return radstar_apps.values()

# -------------------------------------------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

from subprocess import check_call

import click
import jinja2

from . import cli, shexec
from .. import init_radstar, getenv, list_apps, shsplit

# -------------------------------------------------------------------------------------------------------------------- #

SUPERVISOR_CONF_PATH = '/tmp/supervisord.conf'
DEFAULT_SYSTEM_USER = 'rs'

SUDO_PRESERVE_ENV = ','.join([
    'PATH',
    'PYTHONPATH',
])

# -------------------------------------------------------------------------------------------------------------------- #

@cli.command('run')
@click.argument('enabled', nargs=-1)
def run(*, enabled: tuple[str]):
    ''' Run services. '''

    dev_mode = getenv('RS_DEVMODE') == '1'

    if dev_mode or getenv('RS_INIT_DB') == '1':
        check_call(shsplit('rs db init'))

    init_radstar(no_init=True)
    j2 = jinja2.Environment(loader=jinja2.FileSystemLoader('templates/run'), autoescape=False)

    # built-in services
    services = {}
    if dev_mode:
        services['jetapp'] = {'name': 'jetapp', 'cmd': 'yarn start', 'dir':'/rs/radstar/jetapp'}

    # first iteration: get services
    for x in list_apps():
        for svc in x.get_attr('services', []):
            services[svc['name']] = svc

    # second iteration: get services again - this time expanding parameters too
    for x in list_apps():
        if (mod := x.import_module('run')) is None:
            continue
        parameters = mod.get_parameters(j2=j2, dev_mode=dev_mode, services=services)
        for svc_name in (x['name'] for x in x.get_attr('services', [])):
            services[svc_name]['cmd'] = services[svc_name]['cmd'].format(**parameters)

    # limit services based on command line
    if enabled:
        services = {k: v for k, v in services.items() if k in enabled}

    # finalize services by running build_program on each entry
    services = {k: build_program(**v) for k, v in services.items()}

    # generate supervisord config
    with open(SUPERVISOR_CONF_PATH, 'w') as f:
        conf = j2.get_template('supervisord.conf.j2').render(
            dev_mode=dev_mode,
            services=services,
        )
        print(conf, file=f)

    # exec supervisord
    if dev_mode:
        shexec('sudo -E --preserve-env={pe} supervisord -c {conf}', conf=SUPERVISOR_CONF_PATH, pe=SUDO_PRESERVE_ENV)
    else:
        shexec('supervisord -c {conf}', conf=SUPERVISOR_CONF_PATH)

# -------------------------------------------------------------------------------------------------------------------- #

def build_program(name: str, cmd: str, *, dir: str | None = None, user: str | None = DEFAULT_SYSTEM_USER, **kw):

    if x := getenv(f'RS_{name.upper()}_ARGS', ''):
        cmd += ' ' + x

    program = {
        'command': cmd,
        'stdout_logfile': 'NONE',
        'stdout_events_enabled': 'true',
        'stderr_logfile': 'NONE',
        'stderr_events_enabled': 'true',
        **kw
    }

    if dir is not None:
        program['directory'] = dir

    if user is not None:
        program.update({
            'user': user,
            'environment': f'HOME="/home/{user}",USER="{user}"'
        })

    return program

# -------------------------------------------------------------------------------------------------------------------- #

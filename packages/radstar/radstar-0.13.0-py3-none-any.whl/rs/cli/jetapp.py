# -------------------------------------------------------------------------------------------------------------------- #

# Copyright © 2021-2023 Peter Mathiasson
# SPDX-License-Identifier: ISC

# -------------------------------------------------------------------------------------------------------------------- #

import os
import subprocess
import shutil

import click
import yaml

from . import cli
from .. import init_radstar, json, list_apps, shsplit

# -------------------------------------------------------------------------------------------------------------------- #

@cli.group('jetapp')
def jetapp_cli():
    ''' Jetapp. '''

# -------------------------------------------------------------------------------------------------------------------- #

@jetapp_cli.command()
@click.argument('dst', nargs=1)
def build(*, dst: str):
    ''' Build Jetapp. '''

    subprocess.check_call(shsplit('yarn build'), cwd='jetapp')

    app = init_radstar(no_init=True)

    web_files = {}

    for wd in get_web_dirs():
        for root, dirs, files in os.walk(wd):
            for x in dirs:
                if x[0] == '.':
                    dirs.remove(x)
            for x in files:
                if x[0] != '.':
                    web_files[os.path.join(root[len(wd)+1:], x)] = os.path.join(root, x)

    for x in ['jetapp.css', 'jetapp.js']:
        web_files[os.path.join('app', x)] = os.path.join('/tmp/jetapp_output', x)

    if not os.path.isdir(dst):
        os.mkdir(dst)

    for fn, fp in web_files.items():
        dst_dir = os.path.join(dst, os.path.dirname(fn))
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir)
        shutil.copy(fp, os.path.join(dst, fn))

    # replace title in index.html
    index_file = os.path.join(dst, 'index.html')
    with open(index_file) as f:
        index_html = f.read().replace('<title></title>', f'<title>{app.get_attr("jetapp.title", app.name)}</title>')
    with open(index_file, 'w') as f:
        f.write(index_html)

# -------------------------------------------------------------------------------------------------------------------- #

@jetapp_cli.command()
def settings():
    ''' Get Jetapp Settings. '''

    init_radstar(no_init=True)

    with open('/rs/project/project.yml') as f:
        project_data = yaml.safe_load(f)

    jetapp_settings = {}
    for x in list_apps():
        jetapp_settings.update(x.get_attr('jetapp', {}))

    print(json.dumps({
        'name': project_data['name'],
        'settings': jetapp_settings,
        'webroots': list(reversed(get_web_dirs())),
    }, indent=4))

# -------------------------------------------------------------------------------------------------------------------- #

def get_web_dirs() -> list:
    web_dirs = ['/rs/radstar/jetapp/webroot']
    for x in list_apps():
        d = os.path.join(x.dir, 'webroot')
        if os.path.exists(d):
            web_dirs.append(d)
    return web_dirs

# -------------------------------------------------------------------------------------------------------------------- #

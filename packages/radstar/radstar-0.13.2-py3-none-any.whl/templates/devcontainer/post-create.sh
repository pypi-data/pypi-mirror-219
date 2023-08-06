#!/bin/bash -e

# use legacy-resolver to work around https://github.com/pypa/pip/issues/9644
python -m pip install -r /rs/project/requirements.txt --require-virtualenv --use-deprecated=legacy-resolver

python -m pip install pip-tools pylint

rs setup

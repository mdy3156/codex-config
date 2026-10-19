#!/bin/sh
set -eu
exec "${PYTHON:-python3}" "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/manage.py" update "$@"

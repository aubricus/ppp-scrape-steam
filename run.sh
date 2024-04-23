#!/usr/bin/env bash

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Run
#
# Example:
#   bash run.sh
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Bash flags
#  -e, exit on error
#  -u, unset variable is an error
#  -o pipefail, fail pipe chain if error
#  See: https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html
set -eu -o pipefail

python steam-lxml/__init__.py

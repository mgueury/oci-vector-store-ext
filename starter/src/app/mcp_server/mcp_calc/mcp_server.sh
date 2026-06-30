#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

. ../../env.sh

export PYTHONPATH=$HOME/app/src
# Default port is 2025
python mcp_server.py 2>&1 | tee ../../mcp.log

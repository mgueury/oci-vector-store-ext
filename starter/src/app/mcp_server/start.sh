#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR
export PATH=~/.local/bin/:$PATH

. $HOME/app/ingest/env.sh

# Default port is 2025
export PYTHONPATH=$HOME/app/ingest/src
source myenv/bin/activate
python mcp_server_rag.py 2>&1 | tee mcp_server.log

#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR
export PATH=~/.local/bin/:$PATH

. $HOME/compute/tf_env.sh
export MCP_SERVER_URL="http://localhost:2025/mcp"

# Start LangGraph CompiledStateGraph on port 2024
source myenv/bin/activate

port_wait 8080 | tee rest.log
python rest.py 2>&1 | tee -a rest.log

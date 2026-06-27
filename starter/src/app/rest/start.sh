#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR
export PATH=~/.local/bin/:$PATH

. $HOME/compute/tf_env.sh
export MCP_SERVER_URL="http://localhost:2025/mcp"

# Start LangGraph CompiledStateGraph on port 2024
source myenv/bin/activate

port_wait 8080 | tee rest.log

export AGENT_PROMPT="You are a support agent.

INSTRUCTIONS:
- When you receive a question, search the answer by calling the tools search and the tool find_service_request
- Combine the response of the 2 tools to create a final answer to the user or several possible answers found in the different documents.
- Answer only based on the result of the tools used. Do not add any other response or content that is not in the result of the tools.
- Do not call the same tools twice with the same parameters.

REFERENCES:
- When you answer always give the list of document on which you based your response. Give this in a table format. 2 columns.
- Show only the references that were used to answer the question.
- One line for each reference found in 
    - For the tool search. Give the document path and content.
    - For the tool find_service_request. Give the link to the SR and the question.   
Ex:
| Link | Text |
| ---- | ---- |                                                                
| [SR 1](https://url/sr/1) | SR question |                                                                
| [Document Name](https://document_url/) | Document content |                                                                
"

python rest.py 2>&1 | tee -a rest.log

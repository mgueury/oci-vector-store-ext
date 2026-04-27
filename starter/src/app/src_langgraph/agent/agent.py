from langchain_openai import ChatOpenAI
from langchain_oci import ChatOCIGenAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.interceptors import MCPToolCallRequest
import asyncio
import os
import time
import pprint
import httpx
import oci_openai 

COMPARTMENT_OCID = os.getenv("TF_VAR_compartment_ocid")
REGION = os.getenv("TF_VAR_region")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")

# auth = oci_openai.OciInstancePrincipalAuth()
# llm = ChatOpenAI(
#     model="xai.grok-4-fast-reasoning",
#     api_key="OCI",
#     base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1",
#     http_client=httpx.Client(
#         auth=auth,
#         headers={"CompartmentId": COMPARTMENT_OCID}
#     ),
# )

llm = ChatOCIGenAI(
    auth_type="API_KEY" if "LIVELABS" in os.environ else "INSTANCE_PRINCIPAL",
    model_id="openai.gpt-oss-120b",
    # model_id="meta.llama-4-scout-17b-16e-instruct",
    # model_id="cohere.command-a-03-2025",
    service_endpoint="https://inference.generativeai."+REGION+".oci.oraclecloud.com",
    # model_id="xai.grok-4-fast-reasoning",
    # service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id=COMPARTMENT_OCID,
    is_stream=True,
    model_kwargs={"temperature": 0}
)

# See https://docs.langchain.com/oss/python/langchain/mcp#accessing-runtime-context
async def inject_user_context(
    request: MCPToolCallRequest,
    handler,
):
    """Inject user credentials into MCP tool calls."""
    print( "--- request ----" )
    pprint.pprint( request )
    runtime = request.runtime
    user_id = runtime.config["configurable"]["user_id"]
    auth_user = runtime.config["configurable"]["langgraph_auth_user"]
    auth_header = auth_user.dict().get("auth_header")
    print( f"<inject_user_context> user_id={user_id}", flush=True )
    # print( f"<inject_user_context> auth_header={auth_header}", flush=True )
    # modified_request = request.override( headers = { "Authorization": f"User {user_id}" } )
    modified_request = request.override( headers = { "Authorization": auth_header } )
    return await handler(modified_request)

async def init( agent_name, prompt, tools_list, callback_handler=None ) -> StateGraph:

    # Waiting is important, since after reboot the MCP server could start afterwards.
    delay = 10
    for attempt in range(1, 30):
        try:
            print(f"Connecting to MCP {attempt}...")
            client = MultiServerMCPClient(
                {
                    "McpServerRag": {
                        "transport": "streamable_http",
                        "url": MCP_SERVER_URL,                     
                    },
                },
                tool_interceptors=[inject_user_context],
            )
            tools = await client.get_tools()
            print( "-- tools ------------------------------------------------------------")
            pprint.pprint( tools )
            # Filter tools.
            tools_filtered = []
            for tool in tools:
                if tools_list==None or tool.name in tools_list:
                    tools_filtered.append( tool )
            print( "-- tools_filtered ---------------------------------------------------")
            pprint.pprint( tools_filtered )
            break
        except Exception as e:
            print(f"Connection failed {attempt}: {e}")            
            print(f"Waiting for {delay} seconds before the next attempt...")
            time.sleep(delay)

    if client==None:
        print("ERROR: connection to MCP Failed")
        exit(1)

    agent = create_react_agent(
        model=llm,
        tools=tools_filtered,
        prompt=prompt,
        name=agent_name
    ) 

    return agent

prompt_rag = """You are a research agent.

            INSTRUCTIONS:
            - Assist ONLY with research-related tasks, DO NOT do any math.
            - Respond ONLY with the results of your work, do NOT include ANY other text.
            """

agent_rag = asyncio.run(init("agent_rag", prompt_rag, None))

prompt_sr = """You are a support agent.
            INSTRUCTIONS:
            - When you receive a question, search the answer by calling the tools search and the tool find_service_request
            - Combine the response of the 2 tools to create a final answer to the user or several possible answers found in the different documents.
            - Answer only based on the result of the tools used. Do not add any other response or content that is not in the result of the tools.
            
            REFERENCES:
            - When you answer always give the list of document on which you based your response. Give this in a table format. 2 columns.
            - One line for each reference found in 
               - For the tool search. Give the document path and content.
               - For the tool find_service_request. Give the link to the SR and the question.   
            Ex:
            | Link | Text |
            | ---- | ---- |                                                                
            | [SR 1](https://url/sr/1) | SR question |                                                                
            | [Document Name](https://document_url/) | Document content |                                                                
            """

agent_sr = asyncio.run(init("agent_sr", prompt_sr,
            ["search","find_service_request","get_service_request"]))

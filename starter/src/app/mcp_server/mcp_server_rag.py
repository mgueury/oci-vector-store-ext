from fastmcp import FastMCP  # Import FastMCP, the quickstart server base
from fastmcp.server.dependencies import get_http_request
import shared
import os
import rag_storage
import pprint
from typing import List, TypedDict
from pydantic import BaseModel

mcp = FastMCP("MCP RAG Server")  # Initialize an MCP server instance with a descriptive name
RAG_STORAGE = os.getenv("TF_VAR_rag_storage")

rag_storage.createPool()

class DocInfo(BaseModel):
    TITLE: str
    PATH: str

def get_auth_header():
    request = get_http_request()
    auth_header = request.headers.get("Authorization", "Unknown")
    return auth_header
    # "EMPLOYEE" if "EMPLOYEE" in auth_header else "CUSTOMER"

@mcp.tool()
def search(question: str) -> dict:
    """Search in document repository."""
    print(f"<search> question={question}", flush=True)    
    print(f"<search> RAG_STORAGE={RAG_STORAGE}", flush=True)    
    return shared.responses_search( question )

@mcp.tool()
def list_documents() ->  List[DocInfo]:
    """get the list of documents. Return for each document (PATH, TITLE)"""
    print("<list_documents>", flush=True)
    return rag_storage.getDocList()

@mcp.tool()
def get_document_summary(doc_path: str) -> dict:
    """get document summary by path"""
    print("<get_document_summary>", flush=True)
    return rag_storage.getDocByPath(doc_path)

@mcp.tool()
def get_document_by_path(doc_path: str) -> dict:
    """get document by path"""
    print("<get_document_by_path>", flush=True)
    return rag_storage.getDocByPath(doc_path)

@mcp.tool()
def find_service_request(question: str) -> List[dict]:
    """find similar service requests"""
    print("<find_service_request>", flush=True)
    return rag_storage.findServiceRequest(question, get_auth_header())

@mcp.tool()
def get_service_request(id: str) -> dict:
    """get the service request details"""
    print("<get_service_request>", flush=True)
    return rag_storage.getServiceRequest(id, get_auth_header())

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=2025)
    # print( search( "what is jazz" ) )
    # mcp.run(transport="stdio")  # Run the server, using standard input/output for communication

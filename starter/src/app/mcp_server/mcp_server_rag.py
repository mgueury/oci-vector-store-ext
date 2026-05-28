from __future__ import annotations

import os
from functools import wraps
from typing import Any, Callable, List, Optional, TypeVar, cast

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request
from pydantic import BaseModel, Field, ValidationError

import shared
import rag_storage

mcp = FastMCP("MCP RAG Server")
RAG_STORAGE = os.getenv("TF_VAR_rag_storage")

rag_storage.createPool()


class DocInfo(BaseModel):
    TITLE: str = Field(min_length=1)
    PATH: str = Field(min_length=1)


def _error(message: str, *, details: Optional[Any] = None) -> dict:
    payload = {"ok": False, "error": message}
    if details is not None:
        payload["details"] = details
    return payload


def _ok(data: Any) -> dict:
    return {"ok": True, "data": data}


def _normalize_text(value: Any, field_name: str) -> str:
    """
    Accepts strings, rejects None/empty/non-string values.
    Trims whitespace.
    """
    if value is None:
        raise ValueError(f"Missing required parameter: {field_name}")
    if not isinstance(value, str):
        raise TypeError(f"Invalid type for '{field_name}': expected str, got {type(value).__name__}")
    value = value.strip()
    if not value:
        raise ValueError(f"Parameter '{field_name}' cannot be empty")
    return value


def _safe_validate(model_cls: type[BaseModel], value: Any):
    return model_cls.model_validate(value)


def _get_auth_header() -> Optional[str]:
    """
    Return the Authorization header if available.
    Works even when the request context is missing.
    """
    try:
        request = get_http_request()
        if not request:
            return None
        auth_header = request.headers.get("Authorization")
        if isinstance(auth_header, str) and auth_header.strip():
            return auth_header.strip()
    except Exception:
        pass
    return None


T = TypeVar("T")

def tool_guard(fn: Callable[..., T]) -> Callable[..., dict]:
    """
    Convert unexpected exceptions into structured tool errors.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs) -> dict:
        try:
            result = fn(*args, **kwargs)
            shared.log('<tool_guard> OK')
            return _ok(result)
        except (ValueError, TypeError, ValidationError) as e:
            shared.log('<tool_guard> Invalid parameter '+str(e))
            return _error("Invalid parameter(s)", details=str(e))
        except Exception as e:
            shared.log('<tool_guard> Error '+str(e))
            return _error("Internal server error", details=str(e))
    return cast(Callable[..., dict], wrapper)


@mcp.tool()
@tool_guard
def search(question: Any) -> dict:
    """Search in document repository."""
    question = _normalize_text(question, "question")
    print(f"<search> question={question}", flush=True)
    print(f"<search> RAG_STORAGE={RAG_STORAGE}", flush=True)

    if not RAG_STORAGE:
        raise RuntimeError("RAG storage is not configured")

    result = shared.responses_search(question)
    return result


@mcp.tool()
@tool_guard
def list_documents() -> List[DocInfo]:
    """Get the list of documents. Return for each document (PATH, TITLE)."""
    print("<list_documents>", flush=True)

    docs = rag_storage.getDocList()
    if not isinstance(docs, list):
        raise TypeError("rag_storage.getDocList() must return a list")

    validated_docs = []
    for i, doc in enumerate(docs):
        try:
            validated_docs.append(_safe_validate(DocInfo, doc))
        except Exception as e:
            raise ValueError(f"Invalid document at index {i}: {e}") from e

    return validated_docs


@mcp.tool()
@tool_guard
def get_document_summary(doc_path: Any) -> dict:
    """Get document summary by path."""
    print("<get_document_summary>", flush=True)
    doc_path = _normalize_text(doc_path, "doc_path")
    return rag_storage.getDocByPath(doc_path)


@mcp.tool()
@tool_guard
def get_document_by_path(doc_path: Any) -> dict:
    """Get document by path."""
    print("<get_document_by_path>", flush=True)
    doc_path = _normalize_text(doc_path, "doc_path")
    return rag_storage.getDocByPath(doc_path)


@mcp.tool()
@tool_guard
def find_service_request(question: Any) -> List[dict]:
    """Find similar service requests."""
    print("<find_service_request>", flush=True)
    question = _normalize_text(question, "question")

    auth_header = _get_auth_header()
    if not auth_header:
        raise PermissionError("Missing Authorization header")

    results = rag_storage.findServiceRequest(question, auth_header)
    if not isinstance(results, list):
        raise TypeError("rag_storage.findServiceRequest() must return a list")

    return results


@mcp.tool()
@tool_guard
def get_service_request(request_id: Any) -> dict:
    """Get the service request details."""
    print("<get_service_request>", flush=True)
    request_id = _normalize_text(request_id, "request_id")

    auth_header = _get_auth_header()
    if not auth_header:
        raise PermissionError("Missing Authorization header")

    return rag_storage.getServiceRequest(request_id, auth_header)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=2025)
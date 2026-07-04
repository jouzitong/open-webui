from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    name: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    user_id: str | None = None
    session_id: str | None = None
    stream: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    model: str
    message: ChatMessage
    finish_reason: str | None = None
    usage: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatStreamEvent(BaseModel):
    event: Literal["start", "delta", "message", "error", "end"]
    delta: str | None = None
    message: ChatMessage | None = None
    error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class KnowledgeBaseItem(BaseModel):
    id: str
    name: str
    description: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class KnowledgeBaseCreateRequest(BaseModel):
    name: str
    description: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class KnowledgeBasePatchRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    metadata: dict[str, Any] | None = None


class KnowledgeDocumentItem(BaseModel):
    id: str
    knowledge_base_id: str
    title: str
    content: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class KnowledgeDocumentCreateRequest(BaseModel):
    title: str
    content: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class KnowledgeDocumentPatchRequest(BaseModel):
    title: str | None = None
    content: str | None = None
    metadata: dict[str, Any] | None = None


class KnowledgeQueryRequest(BaseModel):
    knowledge_base_id: str
    query: str
    top_k: int = 5
    filters: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class KnowledgeQueryResult(BaseModel):
    document_id: str
    knowledge_base_id: str
    score: float
    snippet: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class AIConfigItem(BaseModel):
    id: str
    name: str
    provider: str
    model: str
    enabled: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class AIConfigCreateRequest(BaseModel):
    name: str
    provider: str
    model: str
    enabled: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class AIConfigPatchRequest(BaseModel):
    name: str | None = None
    provider: str | None = None
    model: str | None = None
    enabled: bool | None = None
    metadata: dict[str, Any] | None = None


class AIConfigQuery(BaseModel):
    provider: str | None = None
    enabled: bool | None = None
    keyword: str | None = None

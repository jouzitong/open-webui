"""AI engine domain module."""

from open_webui.apps.ai_engine.api.contracts import (
    AIConfigCreateRequest,
    AIConfigItem,
    AIConfigPatchRequest,
    AIConfigQuery,
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ChatStreamEvent,
    KnowledgeBaseCreateRequest,
    KnowledgeBaseItem,
    KnowledgeBasePatchRequest,
    KnowledgeDocumentCreateRequest,
    KnowledgeDocumentItem,
    KnowledgeDocumentPatchRequest,
    KnowledgeQueryRequest,
    KnowledgeQueryResult,
)
from open_webui.apps.ai_engine.api.interfaces import (
    AIChatEngine,
    AIConfigEngine,
    AIKnowledgeEngine,
)

__all__ = [
    "AIChatEngine",
    "AIConfigCreateRequest",
    "AIConfigEngine",
    "AIConfigItem",
    "AIConfigPatchRequest",
    "AIConfigQuery",
    "AIKnowledgeEngine",
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "ChatStreamEvent",
    "KnowledgeBaseCreateRequest",
    "KnowledgeBaseItem",
    "KnowledgeBasePatchRequest",
    "KnowledgeDocumentCreateRequest",
    "KnowledgeDocumentItem",
    "KnowledgeDocumentPatchRequest",
    "KnowledgeQueryRequest",
    "KnowledgeQueryResult",
]

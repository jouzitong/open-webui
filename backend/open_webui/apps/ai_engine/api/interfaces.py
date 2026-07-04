from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from open_webui.apps.ai_engine.api.contracts import (
    AIConfigCreateRequest,
    AIConfigItem,
    AIConfigPatchRequest,
    AIConfigQuery,
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


class AIChatEngine(ABC):
    """Base chat capability exposed by the AI engine."""

    @abstractmethod
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Return a non-streaming chat completion."""

    @abstractmethod
    async def chat_stream(self, request: ChatRequest) -> AsyncIterator[ChatStreamEvent]:
        """Yield streaming chat events in order."""


class AIKnowledgeEngine(ABC):
    """Knowledge base CRUD and retrieval capability."""

    @abstractmethod
    async def create_knowledge_base(
        self, request: KnowledgeBaseCreateRequest
    ) -> KnowledgeBaseItem:
        """Create a knowledge base."""

    @abstractmethod
    async def get_knowledge_base(self, knowledge_base_id: str) -> KnowledgeBaseItem | None:
        """Fetch one knowledge base."""

    @abstractmethod
    async def list_knowledge_bases(self) -> list[KnowledgeBaseItem]:
        """List knowledge bases visible to the caller."""

    @abstractmethod
    async def update_knowledge_base(
        self, knowledge_base_id: str, request: KnowledgeBasePatchRequest
    ) -> KnowledgeBaseItem:
        """Update one knowledge base."""

    @abstractmethod
    async def delete_knowledge_base(self, knowledge_base_id: str) -> None:
        """Delete one knowledge base."""

    @abstractmethod
    async def create_document(
        self, knowledge_base_id: str, request: KnowledgeDocumentCreateRequest
    ) -> KnowledgeDocumentItem:
        """Create one knowledge document under the knowledge base."""

    @abstractmethod
    async def get_document(
        self, knowledge_base_id: str, document_id: str
    ) -> KnowledgeDocumentItem | None:
        """Fetch one knowledge document."""

    @abstractmethod
    async def list_documents(self, knowledge_base_id: str) -> list[KnowledgeDocumentItem]:
        """List documents under one knowledge base."""

    @abstractmethod
    async def update_document(
        self,
        knowledge_base_id: str,
        document_id: str,
        request: KnowledgeDocumentPatchRequest,
    ) -> KnowledgeDocumentItem:
        """Update one knowledge document."""

    @abstractmethod
    async def delete_document(self, knowledge_base_id: str, document_id: str) -> None:
        """Delete one knowledge document."""

    @abstractmethod
    async def search(self, request: KnowledgeQueryRequest) -> list[KnowledgeQueryResult]:
        """Run retrieval against a knowledge base."""


class AIConfigEngine(ABC):
    """Basic AI configuration management capability."""

    @abstractmethod
    async def create_config(self, request: AIConfigCreateRequest) -> AIConfigItem:
        """Create one AI config entry."""

    @abstractmethod
    async def get_config(self, config_id: str) -> AIConfigItem | None:
        """Fetch one AI config entry."""

    @abstractmethod
    async def list_configs(self, query: AIConfigQuery | None = None) -> list[AIConfigItem]:
        """List AI config entries."""

    @abstractmethod
    async def update_config(self, config_id: str, request: AIConfigPatchRequest) -> AIConfigItem:
        """Update one AI config entry."""

    @abstractmethod
    async def delete_config(self, config_id: str) -> None:
        """Delete one AI config entry."""

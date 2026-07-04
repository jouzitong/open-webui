from __future__ import annotations

from abc import ABC, abstractmethod

from open_webui.apps.db_engine.api.contracts import (
    DataAggregateRequest,
    DataAggregateResponse,
    DataCountRequest,
    DataCountResponse,
    DataDeleteRequest,
    DataDeleteResponse,
    DataDescribeRequest,
    DataGetRequest,
    DataGetResponse,
    DataInsertRequest,
    DataInsertResponse,
    DataListRequest,
    DataListResponse,
    DataPivotRequest,
    DataPivotResponse,
    DataTreeRequest,
    DataTreeResponse,
    DataUpdateRequest,
    DataUpdateResponse,
    TableDescribeResponse,
)


class DBQueryEngine(ABC):
    """Read-only query capability against an external data source."""

    @abstractmethod
    async def describe_table(self, request: DataDescribeRequest) -> TableDescribeResponse:
        """Describe one external table."""

    @abstractmethod
    async def get(self, request: DataGetRequest) -> DataGetResponse:
        """Fetch one record."""

    @abstractmethod
    async def list(self, request: DataListRequest) -> DataListResponse:
        """Fetch a paginated record list."""

    @abstractmethod
    async def count(self, request: DataCountRequest) -> DataCountResponse:
        """Count records matching filters."""

    @abstractmethod
    async def tree(self, request: DataTreeRequest) -> DataTreeResponse:
        """Build a hierarchical tree result."""

    @abstractmethod
    async def pivot(self, request: DataPivotRequest) -> DataPivotResponse:
        """Build a pivot result set."""

    @abstractmethod
    async def aggregate(self, request: DataAggregateRequest) -> DataAggregateResponse:
        """Run grouped aggregate queries."""


class DBMutationEngine(ABC):
    """Write capability against an external data source."""

    @abstractmethod
    async def insert(self, request: DataInsertRequest) -> DataInsertResponse:
        """Insert one record into an external table."""

    @abstractmethod
    async def update(self, request: DataUpdateRequest) -> DataUpdateResponse:
        """Update records in an external table."""

    @abstractmethod
    async def delete(self, request: DataDeleteRequest) -> DataDeleteResponse:
        """Delete records from an external table."""

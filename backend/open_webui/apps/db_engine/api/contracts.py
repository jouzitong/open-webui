from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class FilterCondition(BaseModel):
    field: str
    op: Literal[
        "eq",
        "ne",
        "gt",
        "gte",
        "lt",
        "lte",
        "in",
        "not_in",
        "between",
        "like",
        "ilike",
        "is_null",
        "is_not_null",
    ]
    value: Any = None


class FilterOperatorValue(BaseModel):
    op: Literal[
        "eq",
        "ne",
        "gt",
        "gte",
        "lt",
        "lte",
        "in",
        "not_in",
        "between",
        "like",
        "ilike",
        "is_null",
        "is_not_null",
    ]
    value: Any = None


class DataOrder(BaseModel):
    field: str
    direction: Literal["asc", "desc"] = "asc"


class RelationSpec(BaseModel):
    table: str | None = None
    model: str | None = None
    alias: str | None = None
    join_type: Literal["inner", "left", "right", "full"] | None = None
    on: str | None = None
    left_key: str | None = None
    right_key: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class QueryExt(BaseModel):
    fields: list[str] = Field(default_factory=list)
    relations: list[RelationSpec] = Field(default_factory=list)
    sorts: dict[str, Literal["asc", "desc"]] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class GroupByField(BaseModel):
    field: str
    alias: str | None = None


class AggregateField(BaseModel):
    field: str
    func: Literal["count", "sum", "avg", "min", "max", "count_distinct"]
    alias: str | None = None


class PivotValueField(BaseModel):
    field: str
    func: Literal["count", "sum", "avg", "min", "max", "count_distinct"]
    alias: str | None = None


class TreeNodeLink(BaseModel):
    id_field: str
    parent_field: str
    root_value: Any = None


class DataRecord(BaseModel):
    values: dict[str, Any] = Field(default_factory=dict)


class QueryRequestBase(BaseModel):
    title: str | None = None
    source_key: str
    model: str
    table: str | None = None
    filter_dict: dict[str, list[Any | dict[str, Any] | FilterOperatorValue]] = Field(default_factory=dict)
    filter_expr: str | None = None
    ext: QueryExt = Field(default_factory=QueryExt)


class MutationRequestBase(BaseModel):
    title: str | None = None
    source_key: str
    model: str
    table: str | None = None


class DataDescribeRequest(BaseModel):
    source_key: str
    table: str


class DataGetRequest(QueryRequestBase):
    filters: list[FilterCondition] = Field(default_factory=list)
    fields: list[str] = Field(default_factory=list)
    orders: list[DataOrder] = Field(default_factory=list)


class DataListRequest(QueryRequestBase):
    fields: list[str] = Field(default_factory=list)
    filters: list[FilterCondition] = Field(default_factory=list)
    orders: list[DataOrder] = Field(default_factory=list)
    limit: int | None = 100
    offset: int | None = 0


class DataQueryRequest(DataListRequest):
    """Backward-compatible alias of list query request."""


class DataCountRequest(QueryRequestBase):
    filters: list[FilterCondition] = Field(default_factory=list)
    distinct_field: str | None = None


class DataTreeRequest(QueryRequestBase):
    fields: list[str] = Field(default_factory=list)
    filters: list[FilterCondition] = Field(default_factory=list)
    orders: list[DataOrder] = Field(default_factory=list)
    link: TreeNodeLink
    max_depth: int | None = None


class DataPivotRequest(QueryRequestBase):
    filters: list[FilterCondition] = Field(default_factory=list)
    row_fields: list[str] = Field(default_factory=list)
    column_field: str
    value_fields: list[PivotValueField] = Field(default_factory=list)


class DataAggregateRequest(QueryRequestBase):
    filters: list[FilterCondition] = Field(default_factory=list)
    group_by: list[GroupByField] = Field(default_factory=list)
    aggregates: list[AggregateField] = Field(default_factory=list)
    orders: list[DataOrder] = Field(default_factory=list)
    limit: int | None = None
    offset: int | None = None


class DataInsertRequest(MutationRequestBase):
    values: dict[str, Any] = Field(default_factory=dict)


class DataUpdateRequest(MutationRequestBase):
    values: dict[str, Any] = Field(default_factory=dict)
    filters: list[FilterCondition] = Field(default_factory=list)
    filter_dict: dict[str, list[Any | dict[str, Any] | FilterOperatorValue]] = Field(default_factory=dict)
    filter_expr: str | None = None


class DataDeleteRequest(MutationRequestBase):
    filters: list[FilterCondition] = Field(default_factory=list)
    filter_dict: dict[str, list[Any | dict[str, Any] | FilterOperatorValue]] = Field(default_factory=dict)
    filter_expr: str | None = None


class TableColumnSchema(BaseModel):
    name: str
    data_type: str
    nullable: bool = True
    default_value: str | None = None
    ordinal_position: int | None = None
    comment: str | None = None


class TableDescribeResponse(BaseModel):
    source_key: str
    table: str
    columns: list[TableColumnSchema] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DataGetResponse(BaseModel):
    source_key: str
    table: str
    item: dict[str, Any] | None = None


class DataListResponse(BaseModel):
    source_key: str
    table: str
    items: list[dict[str, Any]] = Field(default_factory=list)
    total: int | None = None


class DataQueryResponse(DataListResponse):
    """Backward-compatible alias of list query response."""


class DataCountResponse(BaseModel):
    source_key: str
    table: str
    count: int = 0


class DataTreeNode(BaseModel):
    value: dict[str, Any] = Field(default_factory=dict)
    children: list["DataTreeNode"] = Field(default_factory=list)


class DataTreeResponse(BaseModel):
    source_key: str
    table: str
    items: list[DataTreeNode] = Field(default_factory=list)


class DataPivotCell(BaseModel):
    row_key: dict[str, Any] = Field(default_factory=dict)
    column_key: Any = None
    values: dict[str, Any] = Field(default_factory=dict)


class DataPivotResponse(BaseModel):
    source_key: str
    table: str
    items: list[DataPivotCell] = Field(default_factory=list)


class DataAggregateRow(BaseModel):
    group: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, Any] = Field(default_factory=dict)


class DataAggregateResponse(BaseModel):
    source_key: str
    table: str
    items: list[DataAggregateRow] = Field(default_factory=list)
    total: int | None = None


class DataInsertResponse(BaseModel):
    source_key: str
    table: str
    affected_rows: int = 0
    inserted_id: Any = None


class DataUpdateResponse(BaseModel):
    source_key: str
    table: str
    affected_rows: int = 0


class DataDeleteResponse(BaseModel):
    source_key: str
    table: str
    affected_rows: int = 0

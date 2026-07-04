from __future__ import annotations

import time
import uuid
from typing import Optional

from open_webui.internal.db import Base
from open_webui.internal.db import get_async_db_context
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Index, Integer, Text, UniqueConstraint
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class DbTableMeta(Base):
    """Metadata for one logical table under a data source."""

    __tablename__ = "db_table_meta"

    id = Column(Text, primary_key=True)
    data_source_id = Column(Text, ForeignKey("db_data_source.id", ondelete="CASCADE"), nullable=False)
    table_name = Column(Text, nullable=False)
    table_comment = Column(Text, nullable=True)
    table_type = Column(Text, nullable=True)
    layer_type = Column(Text, nullable=True)
    row_count = Column(BigInteger, nullable=True)
    column_count = Column(Integer, nullable=True)
    partition_key = Column(Text, nullable=True)
    freshness_seconds = Column(Integer, nullable=True)
    status = Column(Text, nullable=True)
    enabled = Column(Boolean, nullable=False, default=True)
    last_scan_at = Column(BigInteger, nullable=True)
    last_sync_at = Column(BigInteger, nullable=True)
    remark = Column(Text, nullable=True)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)

    __table_args__ = (
        UniqueConstraint("data_source_id", "table_name", name="uq_db_table_meta_source_table"),
        Index("ix_db_table_meta_data_source_id", "data_source_id"),
        Index("ix_db_table_meta_table_name", "table_name"),
        Index("ix_db_table_meta_enabled", "enabled"),
    )


class DbTableFieldMeta(Base):
    """Metadata for one logical column under a table."""

    __tablename__ = "db_table_field_meta"

    id = Column(Text, primary_key=True)
    table_meta_id = Column(Text, ForeignKey("db_table_meta.id", ondelete="CASCADE"), nullable=False)
    column_name = Column(Text, nullable=False)
    column_comment = Column(Text, nullable=True)
    data_type = Column(Text, nullable=False)
    column_length = Column(Integer, nullable=True)
    column_precision = Column(Integer, nullable=True)
    column_scale = Column(Integer, nullable=True)
    nullable = Column(Boolean, nullable=False, default=True)
    primary_key = Column(Boolean, nullable=False, default=False)
    partition_key = Column(Boolean, nullable=False, default=False)
    default_value = Column(Text, nullable=True)
    ordinal_position = Column(Integer, nullable=True)
    field_role = Column(Text, nullable=True)
    enabled = Column(Boolean, nullable=False, default=True)
    remark = Column(Text, nullable=True)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)

    __table_args__ = (
        UniqueConstraint("table_meta_id", "column_name", name="uq_db_table_field_meta_table_column"),
        Index("ix_db_table_field_meta_table_meta_id", "table_meta_id"),
        Index("ix_db_table_field_meta_column_name", "column_name"),
        Index("ix_db_table_field_meta_table_ordinal", "table_meta_id", "ordinal_position"),
    )


class DbTableIndexMeta(Base):
    """Metadata for one index column entry under a table."""

    __tablename__ = "db_table_index_meta"

    id = Column(Text, primary_key=True)
    table_meta_id = Column(Text, ForeignKey("db_table_meta.id", ondelete="CASCADE"), nullable=False)
    index_name = Column(Text, nullable=False)
    index_type = Column(Text, nullable=True)
    unique_flag = Column(Boolean, nullable=False, default=False)
    primary_flag = Column(Boolean, nullable=False, default=False)
    column_name = Column(Text, nullable=False)
    column_order = Column(Integer, nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    remark = Column(Text, nullable=True)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "table_meta_id",
            "index_name",
            "column_name",
            name="uq_db_table_index_meta_table_index_column",
        ),
        Index("ix_db_table_index_meta_table_meta_id", "table_meta_id"),
        Index("ix_db_table_index_meta_index_name", "index_name"),
        Index("ix_db_table_index_meta_table_index_order", "table_meta_id", "index_name", "column_order"),
    )


class DbTableMetaModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    data_source_id: str
    table_name: str
    table_comment: str | None = None
    table_type: str | None = None
    layer_type: str | None = None
    row_count: int | None = None
    column_count: int | None = None
    partition_key: str | None = None
    freshness_seconds: int | None = None
    status: str | None = None
    enabled: bool = True
    last_scan_at: int | None = None
    last_sync_at: int | None = None
    remark: str | None = None
    created_at: int
    updated_at: int


class DbTableMetaForm(BaseModel):
    data_source_id: str
    table_name: str
    table_comment: str | None = None
    table_type: str | None = None
    layer_type: str | None = None
    row_count: int | None = None
    column_count: int | None = None
    partition_key: str | None = None
    freshness_seconds: int | None = None
    status: str | None = None
    enabled: bool = True
    last_scan_at: int | None = None
    last_sync_at: int | None = None
    remark: str | None = None


class DbTableFieldMetaModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    table_meta_id: str
    column_name: str
    column_comment: str | None = None
    data_type: str
    column_length: int | None = None
    column_precision: int | None = None
    column_scale: int | None = None
    nullable: bool = True
    primary_key: bool = False
    partition_key: bool = False
    default_value: str | None = None
    ordinal_position: int | None = None
    field_role: str | None = None
    enabled: bool = True
    remark: str | None = None
    created_at: int
    updated_at: int


class DbTableFieldMetaForm(BaseModel):
    table_meta_id: str
    column_name: str
    column_comment: str | None = None
    data_type: str
    column_length: int | None = None
    column_precision: int | None = None
    column_scale: int | None = None
    nullable: bool = True
    primary_key: bool = False
    partition_key: bool = False
    default_value: str | None = None
    ordinal_position: int | None = None
    field_role: str | None = None
    enabled: bool = True
    remark: str | None = None


class DbTableIndexMetaModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    table_meta_id: str
    index_name: str
    index_type: str | None = None
    unique_flag: bool = False
    primary_flag: bool = False
    column_name: str
    column_order: int
    enabled: bool = True
    remark: str | None = None
    created_at: int
    updated_at: int


class DbTableIndexMetaForm(BaseModel):
    table_meta_id: str
    index_name: str
    index_type: str | None = None
    unique_flag: bool = False
    primary_flag: bool = False
    column_name: str
    column_order: int
    enabled: bool = True
    remark: str | None = None


class DbTableMetaDetailModel(BaseModel):
    table: DbTableMetaModel
    fields: list[DbTableFieldMetaModel] = Field(default_factory=list)
    indexes: list[DbTableIndexMetaModel] = Field(default_factory=list)


class DbTableMetaTable:
    async def insert_new_table_meta(
        self, form_data: DbTableMetaForm, db: Optional[AsyncSession] = None
    ) -> DbTableMetaModel:
        async with get_async_db_context(db) as db:
            now = int(time.time())
            table = DbTableMeta(id=str(uuid.uuid4()), created_at=now, updated_at=now, **form_data.model_dump())
            db.add(table)
            await db.commit()
            await db.refresh(table)
            return DbTableMetaModel.model_validate(table)

    async def get_table_meta_by_id(
        self, table_meta_id: str, db: Optional[AsyncSession] = None
    ) -> DbTableMetaModel | None:
        async with get_async_db_context(db) as db:
            table = await db.get(DbTableMeta, table_meta_id)
            return DbTableMetaModel.model_validate(table) if table else None

    async def get_table_metas_by_data_source_id(
        self, data_source_id: str, db: Optional[AsyncSession] = None
    ) -> list[DbTableMetaModel]:
        async with get_async_db_context(db) as db:
            result = await db.execute(
                select(DbTableMeta)
                .where(DbTableMeta.data_source_id == data_source_id)
                .order_by(DbTableMeta.table_name.asc())
            )
            items = result.scalars().all()
            return [DbTableMetaModel.model_validate(item) for item in items]

    async def delete_table_meta_by_id(self, table_meta_id: str, db: Optional[AsyncSession] = None) -> bool:
        async with get_async_db_context(db) as db:
            await db.execute(delete(DbTableMeta).filter_by(id=table_meta_id))
            await db.commit()
            return True


class DbTableFieldMetaTable:
    async def insert_new_field_meta(
        self, form_data: DbTableFieldMetaForm, db: Optional[AsyncSession] = None
    ) -> DbTableFieldMetaModel:
        async with get_async_db_context(db) as db:
            now = int(time.time())
            field = DbTableFieldMeta(id=str(uuid.uuid4()), created_at=now, updated_at=now, **form_data.model_dump())
            db.add(field)
            await db.commit()
            await db.refresh(field)
            return DbTableFieldMetaModel.model_validate(field)

    async def get_field_metas_by_table_meta_id(
        self, table_meta_id: str, db: Optional[AsyncSession] = None
    ) -> list[DbTableFieldMetaModel]:
        async with get_async_db_context(db) as db:
            result = await db.execute(
                select(DbTableFieldMeta)
                .where(DbTableFieldMeta.table_meta_id == table_meta_id)
                .order_by(DbTableFieldMeta.ordinal_position.asc(), DbTableFieldMeta.column_name.asc())
            )
            items = result.scalars().all()
            return [DbTableFieldMetaModel.model_validate(item) for item in items]

    async def delete_field_metas_by_table_meta_id(
        self, table_meta_id: str, db: Optional[AsyncSession] = None
    ) -> bool:
        async with get_async_db_context(db) as db:
            await db.execute(delete(DbTableFieldMeta).where(DbTableFieldMeta.table_meta_id == table_meta_id))
            await db.commit()
            return True


class DbTableIndexMetaTable:
    async def insert_new_index_meta(
        self, form_data: DbTableIndexMetaForm, db: Optional[AsyncSession] = None
    ) -> DbTableIndexMetaModel:
        async with get_async_db_context(db) as db:
            now = int(time.time())
            index = DbTableIndexMeta(id=str(uuid.uuid4()), created_at=now, updated_at=now, **form_data.model_dump())
            db.add(index)
            await db.commit()
            await db.refresh(index)
            return DbTableIndexMetaModel.model_validate(index)

    async def get_index_metas_by_table_meta_id(
        self, table_meta_id: str, db: Optional[AsyncSession] = None
    ) -> list[DbTableIndexMetaModel]:
        async with get_async_db_context(db) as db:
            result = await db.execute(
                select(DbTableIndexMeta)
                .where(DbTableIndexMeta.table_meta_id == table_meta_id)
                .order_by(DbTableIndexMeta.index_name.asc(), DbTableIndexMeta.column_order.asc())
            )
            items = result.scalars().all()
            return [DbTableIndexMetaModel.model_validate(item) for item in items]

    async def delete_index_metas_by_table_meta_id(
        self, table_meta_id: str, db: Optional[AsyncSession] = None
    ) -> bool:
        async with get_async_db_context(db) as db:
            await db.execute(delete(DbTableIndexMeta).where(DbTableIndexMeta.table_meta_id == table_meta_id))
            await db.commit()
            return True


class DbTableMetaBundleTable:
    async def get_table_meta_detail(
        self, table_meta_id: str, db: Optional[AsyncSession] = None
    ) -> DbTableMetaDetailModel | None:
        async with get_async_db_context(db) as db:
            table = await db.get(DbTableMeta, table_meta_id)
            if not table:
                return None

            fields_result = await db.execute(
                select(DbTableFieldMeta)
                .where(DbTableFieldMeta.table_meta_id == table_meta_id)
                .order_by(DbTableFieldMeta.ordinal_position.asc(), DbTableFieldMeta.column_name.asc())
            )
            indexes_result = await db.execute(
                select(DbTableIndexMeta)
                .where(DbTableIndexMeta.table_meta_id == table_meta_id)
                .order_by(DbTableIndexMeta.index_name.asc(), DbTableIndexMeta.column_order.asc())
            )

            return DbTableMetaDetailModel(
                table=DbTableMetaModel.model_validate(table),
                fields=[DbTableFieldMetaModel.model_validate(item) for item in fields_result.scalars().all()],
                indexes=[DbTableIndexMetaModel.model_validate(item) for item in indexes_result.scalars().all()],
            )


DbTableMetas = DbTableMetaTable()
DbTableFieldMetas = DbTableFieldMetaTable()
DbTableIndexMetas = DbTableIndexMetaTable()
DbTableMetaBundle = DbTableMetaBundleTable()

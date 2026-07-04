from __future__ import annotations

import time
import uuid
from typing import Optional

from open_webui.internal.db import Base, JSONField
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import BigInteger, Boolean, Column, Index, Text
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from open_webui.internal.db import get_async_db_context


class DbDataSource(Base):
    """Metadata for one logical data source."""

    __tablename__ = "db_data_source"

    id = Column(Text, primary_key=True)
    source_key = Column(Text, nullable=False, unique=True)
    source_name = Column(Text, nullable=False)
    source_type = Column(Text, nullable=False)
    owner_team = Column(Text, nullable=True)
    owner_user = Column(Text, nullable=True)
    enabled = Column(Boolean, nullable=False, default=True)
    sync_mode = Column(Text, nullable=True)
    config = Column(JSONField, nullable=True)
    summary = Column(Text, nullable=True)
    remark = Column(Text, nullable=True)
    last_sync_at = Column(BigInteger, nullable=True)
    last_access_at = Column(BigInteger, nullable=True)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)

    __table_args__ = (
        Index("ix_db_data_source_source_type", "source_type"),
        Index("ix_db_data_source_enabled", "enabled"),
    )


class DbDataSourceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    source_key: str
    source_name: str
    source_type: str
    owner_team: str | None = None
    owner_user: str | None = None
    enabled: bool = True
    sync_mode: str | None = None
    config: dict | None = None
    summary: str | None = None
    remark: str | None = None
    last_sync_at: int | None = None
    last_access_at: int | None = None
    created_at: int
    updated_at: int


class DbDataSourceForm(BaseModel):
    source_key: str
    source_name: str
    source_type: str
    owner_team: str | None = None
    owner_user: str | None = None
    enabled: bool = True
    sync_mode: str | None = None
    config: dict | None = None
    summary: str | None = None
    remark: str | None = None


class DbDataSourceUpdateForm(BaseModel):
    source_name: str | None = None
    source_type: str | None = None
    owner_team: str | None = None
    owner_user: str | None = None
    enabled: bool | None = None
    sync_mode: str | None = None
    config: dict | None = None
    summary: str | None = None
    remark: str | None = None
    last_sync_at: int | None = None
    last_access_at: int | None = None


class DbDataSourceListResponse(BaseModel):
    items: list[DbDataSourceModel] = Field(default_factory=list)
    total: int


class DbDataSourceTable:
    async def insert_new_data_source(
        self,
        form_data: DbDataSourceForm,
        db: Optional[AsyncSession] = None,
    ) -> DbDataSourceModel:
        async with get_async_db_context(db) as db:
            now = int(time.time())
            source = DbDataSource(
                id=str(uuid.uuid4()),
                source_key=form_data.source_key,
                source_name=form_data.source_name,
                source_type=form_data.source_type,
                owner_team=form_data.owner_team,
                owner_user=form_data.owner_user,
                enabled=form_data.enabled,
                sync_mode=form_data.sync_mode,
                config=form_data.config,
                summary=form_data.summary,
                remark=form_data.remark,
                created_at=now,
                updated_at=now,
            )
            db.add(source)
            await db.commit()
            await db.refresh(source)
            return DbDataSourceModel.model_validate(source)

    async def get_data_source_by_id(
        self, data_source_id: str, db: Optional[AsyncSession] = None
    ) -> DbDataSourceModel | None:
        async with get_async_db_context(db) as db:
            source = await db.get(DbDataSource, data_source_id)
            return DbDataSourceModel.model_validate(source) if source else None

    async def get_data_source_by_source_key(
        self, source_key: str, db: Optional[AsyncSession] = None
    ) -> DbDataSourceModel | None:
        async with get_async_db_context(db) as db:
            result = await db.execute(select(DbDataSource).filter_by(source_key=source_key))
            source = result.scalar_one_or_none()
            return DbDataSourceModel.model_validate(source) if source else None

    async def get_data_sources(self, db: Optional[AsyncSession] = None) -> list[DbDataSourceModel]:
        async with get_async_db_context(db) as db:
            result = await db.execute(select(DbDataSource).order_by(DbDataSource.created_at.desc()))
            items = result.scalars().all()
            return [DbDataSourceModel.model_validate(item) for item in items]

    async def update_data_source_by_id(
        self,
        data_source_id: str,
        form_data: DbDataSourceUpdateForm,
        db: Optional[AsyncSession] = None,
    ) -> DbDataSourceModel | None:
        async with get_async_db_context(db) as db:
            source = await db.get(DbDataSource, data_source_id)
            if not source:
                return None

            update_data = form_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(source, key, value)
            source.updated_at = int(time.time())

            await db.commit()
            await db.refresh(source)
            return DbDataSourceModel.model_validate(source)

    async def delete_data_source_by_id(
        self, data_source_id: str, db: Optional[AsyncSession] = None
    ) -> bool:
        async with get_async_db_context(db) as db:
            await db.execute(delete(DbDataSource).filter_by(id=data_source_id))
            await db.commit()
            return True

    async def touch_last_sync_at(
        self, data_source_id: str, last_sync_at: int | None = None, db: Optional[AsyncSession] = None
    ) -> bool:
        async with get_async_db_context(db) as db:
            timestamp = last_sync_at or int(time.time())
            await db.execute(
                update(DbDataSource)
                .where(DbDataSource.id == data_source_id)
                .values(last_sync_at=timestamp, updated_at=int(time.time()))
            )
            await db.commit()
            return True


DbDataSources = DbDataSourceTable()

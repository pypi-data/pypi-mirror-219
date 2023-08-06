from __future__ import annotations

import contextlib
import datetime
import json
import logging
import re
from contextvars import ContextVar
from typing import Type, Dict, List, Tuple

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from pydantic_db_backend.indexes import Index
from pydantic_db_backend.utils import uid, utcnow, str_to_datetime_if_parseable

log = logging.getLogger(__name__)

backend_context_var = ContextVar('backend_context_var')
backend_alias_context_var = ContextVar('backend_alias_context_var', default='default')


class BackendModel(BaseModel):
    uid: str | None = Field(default_factory=uid)
    revision: str | None = None
    version: int | None = 1
    created_time: datetime.datetime | None = Field(default_factory=utcnow)
    updated_time: datetime.datetime | None = Field(default_factory=utcnow)

    class Config:
        json_encoders = {
            datetime.datetime: lambda x: x.isoformat(),
        }
        json_decoders = {
            datetime.datetime: str_to_datetime_if_parseable,
        }


class Backend(object):
    @staticmethod
    @contextlib.contextmanager
    def provider(backend: Type[BackendBase]):
        token = backend_context_var.set(backend)
        yield backend
        backend_context_var.reset(token)

    @classmethod
    def backend(cls) -> BackendBase:
        return backend_context_var.get()

    @classmethod
    def post_instance(cls, instance: BackendModel) -> BackendModel:
        return cls.backend().post_instance(instance)

    @classmethod
    def get_instance(cls, model: Type[BackendModel], uid: str) -> BackendModel:
        return cls.backend().get_instance(model, uid)

    @classmethod
    def put_instance(cls, instance: BackendModel, ignore_revision_conflict: bool = False) -> BackendModel:
        return cls.backend().put_instance(instance, ignore_revision_conflict)

    @classmethod
    def get_uids(cls, model: Type[BackendModel], skip: int = 0, limit: int = 0, query_filter: dict | None = None,
                 sort: List | None = None) -> List[str]:
        return cls.backend().get_uids(model=model, skip=skip, limit=limit, query_filter=query_filter, sort=sort)

    @classmethod
    def get_instances(
        cls,
        model: Type[BackendModel],
        skip: int = 0,
        limit: int = 0,
        query_filter: dict | None = None,
        sort: List | None = None,
        max_results: bool | None = False
    ) -> Tuple[List[BackendModel], int]:
        return cls.backend().get_instances(model=model, skip=skip, limit=limit, query_filter=query_filter, sort=sort)

    @classmethod
    def delete_uid(cls, model: Type[BackendModel], uid: str) -> None:
        return cls.backend().delete_uid(model=model, uid=uid)

    @classmethod
    def delete_collection(cls, model: Type[BackendModel]) -> None:
        return cls.backend().delete_collection(model)


class BackendBase(object):
    _collections: Dict[Type[BaseModel], str] = {}
    _indexes: Dict[Type[BaseModel], list] = {}

    @classmethod
    def startup(cls, alias: str | None = "default"):
        load_dotenv(".env.local")

    @classmethod
    def get_instance(cls, model: Type[BackendModel], uid: str) -> BackendModel:
        raise NotImplementedError()

    @staticmethod
    @contextlib.contextmanager
    def alias_provider(alias: str):
        token = backend_alias_context_var.set(alias)
        yield
        backend_alias_context_var.reset(token)

    @staticmethod
    @contextlib.contextmanager
    def alias() -> str:
        yield backend_alias_context_var.get()

    @classmethod
    def collection_name(cls, model: Type[BaseModel]) -> str:
        if model not in cls._collections:
            name = re.sub('([A-Z]+)', r'_\1', model.__name__).lower().removeprefix("_").removesuffix("_model")
            cls._collections[model] = name
        return cls._collections[model]

    @classmethod
    def indexes(
        cls,
        model: Type[BaseModel],
        create_index_kwargs: dict | None,
        force_index_creation: bool = False
    ) -> List[Index]:
        if model not in cls._indexes or force_index_creation:
            indexes = cls.create_indexes(model, create_index_kwargs)
            cls._indexes[model] = indexes
        return cls._indexes[model]

    @classmethod
    def create_indexes(cls, model: Type[BaseModel], create_index_kwargs: dict | None) -> List[Index]:

        if not hasattr(model, "Config"):
            return True

        if not hasattr(model.Config, "backend_indexes"):
            return True

        indexes = model.Config.backend_indexes
        for index in indexes:
            cls.create_index(cls.collection_name(model), index, **create_index_kwargs)
        return indexes

    @classmethod
    def create_index(cls, collection_name: str, index: Index, **kwargs):
        log.debug(f"[{collection_name}] Creating {index.type} index {index.name}...")

    @classmethod
    def to_db(cls, instance: BackendModel, json_dict: bool | None = True) -> dict:
        instance.updated_time = utcnow()
        return json.loads(instance.json()) if json_dict else instance.dict()

    @classmethod
    def from_db(cls, model: Type[BackendModel], document: dict, json_dict: bool | None = True) -> BackendModel:
        return model.parse_raw(json.dumps(document)) if json_dict else model.parse_obj(document)

    @classmethod
    def put_instance(cls, instance: BackendModel, ignore_revision_conflict: bool = False) -> BackendModel:
        raise NotImplementedError

    @classmethod
    def post_instance(cls, instance: BackendModel) -> BackendModel:
        raise NotImplementedError

    @classmethod
    def get_uids(
        cls,
        model: Type[BackendModel],
        skip: int = 0,
        limit: int = 0,
        query_filter: dict | None = None,
        sort: List | None = None,
        max_results: bool | None = False
    ) -> Tuple[List[str], int]:
        raise NotImplementedError

    @classmethod
    def get_instances(
        cls,
        model: Type[BackendModel],
        skip: int = 0,
        limit: int = 0,
        query_filter: dict = None,
        sort: List = None,
        max_results: bool = False,
    ) -> Tuple[List[BackendModel], int]:
        ids, max_results = cls.get_uids(
            model=model,
            skip=skip,
            limit=limit,
            query_filter=query_filter,
            sort=sort,
            max_results=max_results
        )
        return [cls.get_instance(model, uid=x) for x in ids], max_results

    @classmethod
    def delete_uid(cls, model: Type[BackendModel], uid: str) -> None:
        raise NotImplementedError

    @classmethod
    def delete_collection(cls, model: Type[BackendModel]) -> None:
        # delete index info , for recreating it on next collection usage
        if model in cls._indexes:
            del cls._indexes[model]

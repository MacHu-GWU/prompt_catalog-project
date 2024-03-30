# -*- coding: utf-8 -*-

import typing as T
import json
import dataclasses

import pyairtable
import sayt.api as sayt

from .cache import cache

from .paths import (
    path_airtable_pac,
    path_airtable_data,
    dir_index,
    dir_cache,
)


def create_airtable_api() -> pyairtable.Api:
    return pyairtable.Api(path_airtable_pac.read_text().strip())


def get_base_id(
    api: pyairtable.Api,
    base_name: str = "Prompt Engineering",
) -> str:
    """
    Get base id by base name.
    """
    cache_key = f"{base_name} base id"
    base_id = cache.get(cache_key)
    if base_id is None:
        res = api.bases()
        for base in res:
            if base.name == base_name:
                base_id = base.id
                cache.set(cache_key, base_id)
                break
        if base_id is None:
            raise ValueError(f"Can not find base with name {base_name}")
    return base_id


def get_all_table_ids(
    base: pyairtable.Base,
) -> dict[str, str]:  # name -> id
    """
    Get all table ids in a base.
    """
    cache_key = "prompt engineer base tables"
    table_mapper: dict[str, str] = cache.get(cache_key)
    if table_mapper is None:
        table_mapper = {}
        for table in base.tables():
            table_mapper[table.name] = table.id
        cache.set(cache_key, table_mapper)
    return table_mapper


def get_data(
    save: bool = False,
):
    """ """
    api = create_airtable_api()
    base_name = "Prompt Engineering"
    base_id = get_base_id(api, base_name)
    table_mapper = get_all_table_ids(api.base(base_id))
    data = dict()
    for table_name, table_id in table_mapper.items():
        tb_data = dict()
        for record in api.table(base_id, table_id).all():
            tb_data[record["id"]] = record
        data[table_name] = tb_data
    if save:
        path_airtable_data.write_text(json.dumps(data, indent=4, ensure_ascii=False))
    return data

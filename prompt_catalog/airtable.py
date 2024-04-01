# -*- coding: utf-8 -*-

"""
todo: add docstring
"""

import typing as T
import json

import pyairtable

from .cache import cache

from .paths import (
    path_airtable_pac,
    path_airtable_data,
)


def create_airtable_api() -> pyairtable.Api:
    return pyairtable.Api(path_airtable_pac.read_text().strip())


DEFAULT_EXPIRE = 24 * 60 * 60  # 24 hours


def get_base_id(
    api: pyairtable.Api,
    base_name: str,
) -> str:
    """
    Get base id by base name.

    Ref:

    - https://airtable.com/developers/web/api/list-bases
    """
    res = api.bases()
    base_id = None
    for base in res:
        if base.name == base_name:
            base_id = base.id
            return base_id
    if base_id is None:
        raise ValueError(f"Can not find base with name {base_name}")


def get_base_id_with_cache(
    api: pyairtable.Api,
    base_name: str,
    use_cache: bool = True,
) -> str:
    if use_cache:
        cache_key = f"{base_name} base id"
        base_id = cache.get(cache_key)
        if base_id is None:
            base_id = get_base_id(api, base_name)
            cache.set(cache_key, base_id, expire=DEFAULT_EXPIRE)
        return base_id
    else:
        return get_base_id(api, base_name)


def get_all_table_ids(
    base: pyairtable.Base,
) -> dict[str, str]:  # {name: id}
    """
    Get all table ids in a base.

    Ref:

    - https://airtable.com/developers/web/api/get-base-schema
    """
    table_mapper: dict[str, str] = {}
    for table in base.tables():
        table_mapper[table.name] = table.id
    return table_mapper


def get_all_table_ids_with_cache(
    base: pyairtable.Base,
    use_cache: bool = True,
) -> dict[str, str]:  # {name: id}
    """
    Get all table ids in a base.

    Ref:

    - https://airtable.com/developers/web/api/get-base-schema
    """
    if use_cache:
        cache_key = f"{base.id} base tables"
        table_mapper = cache.get(cache_key)
        if table_mapper is None:
            table_mapper = get_all_table_ids(base)
            cache.set(cache_key, table_mapper, expire=DEFAULT_EXPIRE)
        return table_mapper
    else:
        return get_all_table_ids(base)


class T_RECORD(T.TypedDict):
    id: str
    createdTime: str
    fields: T.Mapping[str, T.Any]


T_RECORDS = T.Mapping[str, T_RECORD]
T_DATA = T.Mapping[str, T_RECORDS]


def get_data(
    api: pyairtable.Api,
    base: pyairtable.Base,
    table_mapper: dict[str, str],
) -> T_DATA:
    """
    Get all data (rows) in all tables in the given base.

    Ref:

    - https://airtable.com/developers/web/api/list-records
    - https://pyairtable.readthedocs.io/en/stable/api.html#pyairtable.Table.all
    """
    data = dict()
    for table_name, table_id in table_mapper.items():
        tb_data = dict()
        for record in api.table(base.id, table_id).all():
            tb_data[record["id"]] = record
        data[table_name] = tb_data
    return data


def get_data_with_cache(
    api: pyairtable.Api,
    base: pyairtable.Base,
    table_mapper: dict[str, str],
    use_cache: bool = True,
) -> T_DATA:
    if use_cache:
        cache_key = f"{base.id} data"
        data = cache.get(cache_key)
        if data is None:
            data = get_data(api, base, table_mapper)
            cache.set(cache_key, data, expire=DEFAULT_EXPIRE)
        return data
    else:
        return get_data(api, base, table_mapper)


def save_data(data: T_DATA):
    # ensure_ascii has to be False!
    path_airtable_data.write_text(json.dumps(data, indent=4, ensure_ascii=False))

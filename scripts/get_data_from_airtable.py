# -*- coding: utf-8 -*-

from prompt_catalog.airtable import (
    create_airtable_api,
    get_base_id_with_cache,
    get_all_table_ids_with_cache,
    get_data_with_cache,
    save_data,
)

base_name = "Prompt Engineering"
use_cache = True

api = create_airtable_api()
base_id = get_base_id_with_cache(api, base_name, use_cache)
base = api.base(base_id)
table_mapper = get_all_table_ids_with_cache(base, use_cache)
data = get_data_with_cache(api, base, table_mapper, use_cache)
save_data(data)

# -*- coding: utf-8 -*-

from rich import print as rprint
from whoosh.query import And, Term
from prompt_catalog.fts import element_dataset, element_choice_dataset


if __name__ == "__main__":
    # --- Search element
    res = element_dataset.search(query="role")
    rprint(res)
    role_element_id = res[0]["id"]

    # --- Search element choice
    query = "tech"
    query = element_choice_dataset._parse_query(query)
    query = And([query, Term("Element", role_element_id)])
    print(query)
    res = element_choice_dataset.search(query=query)
    rprint(res)

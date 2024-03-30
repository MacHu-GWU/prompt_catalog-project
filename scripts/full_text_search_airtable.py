# -*- coding: utf-8 -*-

from rich import print as rprint
from whoosh.query import Query, And, Term
from prompt_catalog.fts import element_dataset, element_choice_dataset


if __name__ == "__main__":
    # res = element_dataset.search(query="ins")
    # rprint(res)

    query = "tech"
    query = element_choice_dataset._parse_query(query)
    query = And([query, Term("Element", "reccTjRtCUPFdJruR")])
    print(query)
    res = element_choice_dataset.search(query=query)
    rprint(res)

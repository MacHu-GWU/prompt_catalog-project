# -*- coding: utf-8 -*-

"""
Provide full text search capability for the application.
"""

import typing as T
import json
import dataclasses

import sayt.api as sayt

from .cache import cache
from .paths import (
    path_airtable_data,
    dir_index,
)


@dataclasses.dataclass
class Element:
    id: str
    createdTime: str
    Name: str


@dataclasses.dataclass
class ElementChoice:
    id: str
    createdTime: str
    Name: str
    Body: str
    Element: str


@dataclasses.dataclass
class AirTableData:
    element_list: list[Element]
    element_choice_list: list[ElementChoice]


def load_data():
    """
    Load data from the Airtable JSON file.
    """
    data = json.loads(path_airtable_data.read_text())
    element_list = [
        Element(
            id=id,
            createdTime=dct["createdTime"],
            Name=dct["fields"]["Name"],
        )
        for id, dct in data["Element"].items()
    ]
    element_choice_list = [
        ElementChoice(
            id=id,
            createdTime=dct["createdTime"],
            Name=dct["fields"]["Name"],
            Body=dct["fields"].get("Body"),
            Element=dct["fields"]["Element"][0],
        )
        for id, dct in data["Element Choice"].items()
    ]
    airtable_data = AirTableData(
        element_list=element_list,
        element_choice_list=element_choice_list,
    )
    return airtable_data


class DownloaderCollection:
    def __init__(self):
        self.airtable_data = load_data()

    def element_downloader(self):
        return [
            dict(
                id=element.id,
                createdTime=element.createdTime,
                Name=element.Name,
                Name_ng=element.Name,
            )
            for element in self.airtable_data.element_list
        ]

    def element_choice_downloader(self):
        return [
            dict(
                id=element_choice.id,
                createdTime=element_choice.createdTime,
                Name=element_choice.Name,
                Name_ng=element_choice.Name,
                Body=element_choice.Body,
                Element=element_choice.Element,
            )
            for element_choice in self.airtable_data.element_choice_list
        ]


downloader_collection = DownloaderCollection()


def make_dataset(index_name: str, fields: list, downloader: T.Callable) -> sayt.DataSet:
    return sayt.DataSet(
        dir_index=dir_index,
        index_name=index_name,
        fields=fields,
        cache=cache,
        cache_key=index_name,
        cache_expire=24 * 60 * 60,
        cache_tag=index_name,
        downloader=downloader,
    )


element_fields = [
    sayt.IdField(name="id", stored=True),
    sayt.StoredField(name="createdTime"),
    # match by n-gram characters
    sayt.TextField(
        name="Name",
        stored=True,
    ),
    sayt.NgramField(
        name="Name_ng",
        stored=False,
        minsize=2,
        maxsize=6,
    ),
]

element_dataset = make_dataset(
    index_name="element-dataset",
    fields=element_fields,
    downloader=downloader_collection.element_downloader,
)


element_choice_fields = [
    sayt.IdField(name="id", stored=True),
    sayt.StoredField(name="createdTime"),
    sayt.TextField(
        name="Name",
        stored=True,
    ),
    sayt.NgramField(
        name="Name_ng",
        stored=False,
        minsize=2,
        maxsize=6,
    ),
    sayt.StoredField(name="Body"),
    sayt.IdField(name="Element", stored=False),
]


element_choice_dataset = make_dataset(
    index_name="element_choice-dataset",
    fields=element_choice_fields,
    downloader=downloader_collection.element_choice_downloader,
)

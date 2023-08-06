"""
The type declarations specific to the `David Rumsey Map Collection` data source.
"""

# pylint: disable=too-few-public-methods

from typing import List, TypedDict, Union

from typing_extensions import NotRequired

from ..typing import MetadataEntry as BaseMetadataEntry

TextWithLang = TypedDict('TextWithLang', {
    '@xml:lang': str,
    '#text': str,
})

Record = TypedDict('Record', {
    '@xmlns:dc': str,
    '@xmlns:oai_dc': str,
    '@xmlns:xsi': str,
    '@xsi:schemaLocation': str,
    'dc:identifier': Union[str, List[str]],
    'dc:relation': Union[str, List[str]],
    'dc:source': str,
    'dc:title': Union[str, List[Union[str, TextWithLang]]],

    # The author(s).
    'dc:creator': NotRequired[Union[str, List[str]]],
    'dc:date': NotRequired[Union[str, List[str]]],
    'dc:subject': NotRequired[Union[str, TextWithLang, List[Union[str, TextWithLang]], None]],
    'dc:coverage': NotRequired[Union[str, List[str], None]],
    'dc:format': NotRequired[Union[str, TextWithLang, List[Union[str, TextWithLang]]]],
    # For collections within the BnF, the language code has 3 characters.
    # For collections from outside, the language code can be arbitrary.
    'dc:language': NotRequired[Union[str, List[str]]],
    # Type of the document, e.g., monograph, map, image,
    # fascicle, manuscript, score, sound, object and video.
    'dc:type': NotRequired[List[Union[str, TextWithLang]]],
    'dc:rights': NotRequired[List[TextWithLang]],
    'dc:publisher': NotRequired[Union[str, List[str]]],
    'dc:description': NotRequired[Union[str, List[str]]],
    'dc:contributor': NotRequired[Union[str, List[str]]],
    '#text': NotRequired[str],
})


class Page(TypedDict):
    numero: Union[str, None]
    ordre: str
    pagination_type: Union[str, None]
    image_width: str
    image_height: str
    legend: NotRequired[str]


class SourceData(TypedDict):
    identifier: str
    record: NotRequired[Record]
    pages: NotRequired[List[Page]]


class MetadataEntry(BaseMetadataEntry):
    """The data structure of an entry in the metadata."""
    sourceData: SourceData

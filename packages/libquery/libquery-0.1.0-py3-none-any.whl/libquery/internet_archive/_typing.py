"""
The type declarations specific to the `Internet Archive` data source.
"""

# pylint: disable=too-few-public-methods

from typing import List, TypedDict, Union

from typing_extensions import NotRequired

from ..typing import MetadataEntry as BaseMetadataEntry


class FileMetadata(TypedDict):
    name: str
    source: str
    format: str
    md5: str
    btih: NotRequired[str]
    mtime: NotRequired[str]
    size: NotRequired[str]
    crc32: NotRequired[str]
    sha1: NotRequired[str]
    rotation: NotRequired[str]
    original: NotRequired[str]


"""The data directly returned from the url."""
InternetArchiveMetadata = TypedDict('InternetArchiveMetadata', {
    # The identifier that can be used to retrieve the item through
    # internetarchive.get_item(identifier)
    'identifier': str,
    'mediatype': str,
    'title': str,
    'publicdate': str,
    'uploader': str,
    'addeddate': str,
    'collection': Union[List[str], str],
    'description': NotRequired[Union[List[str], str]],
    'call_number': NotRequired[str],
    # The entries' corresponding location
    'coverage': NotRequired[Union[List[str], str]],
    'creator': NotRequired[Union[List[str], str]],
    # The publication date.
    'date': NotRequired[Union[List[str], str]],
    # The number of times the item has been viewed on archive.org
    'external-identifier': NotRequired[Union[List[str], str]],
    'format': NotRequired[str],
    'language': NotRequired[Union[List[str], str]],
    'map-type': NotRequired[Union[List[str], str]],
    'publisher': NotRequired[Union[List[str], str]],
    # Copyright information
    'rights': NotRequired[str],
    'scanner': NotRequired[str],
    'size': NotRequired[str],
    # The url of the entry in the original data source.
    'source': NotRequired[str],
    'subject': NotRequired[Union[List[str], str]],
    # The warning about the metadata.
    'warning': NotRequired[str],
    'year': NotRequired[str],
    'isbn': NotRequired[Union[List[str], str]],
    'issn': NotRequired[str],
    'date_range': NotRequired[str]
})


class SourceData(TypedDict):
    created: int
    d1: str
    d2: str
    dir: str
    files: List[FileMetadata]
    files_count: int
    item_last_updated: int
    item_size: int
    metadata: InternetArchiveMetadata
    server: str
    uniq: int
    workable_servers: List[str]
    reviews: NotRequired[List[str]]
    servers_unavailable: NotRequired[bool]


class MetadataEntry(BaseMetadataEntry):
    """The data structure of an entry in the metadata."""
    sourceData: SourceData

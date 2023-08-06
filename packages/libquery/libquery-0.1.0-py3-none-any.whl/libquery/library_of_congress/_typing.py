"""
The type declarations specific to the `Internet Archive` data source.

See reference on the response data structure at
<https://www.loc.gov/apis/json-and-yaml/responses/item-and-resource/>
"""

# pylint: disable=too-few-public-methods

from typing import Any, List, TypedDict, Union

from typing_extensions import NotRequired

from ..typing import MetadataEntry as BaseMetadataEntry


class RelatedItem(TypedDict):
    title: str
    url: str


class Creator(TypedDict):
    link: str
    role: str
    title: str


class Format(TypedDict):
    link: str
    title: str


class Item(TypedDict):
    created_published: NotRequired[Union[str, List[str]]]
    digital_id: NotRequired[List[str]]
    format: NotRequired[Union[str, List[str]]]
    language: NotRequired[Union[str, List[str]]]
    notes: NotRequired[List[str]]
    repository: NotRequired[Union[str, List[str]]]
    title: NotRequired[str]
    date: NotRequired[str]
    location: NotRequired[List[str]]
    medium: NotRequired[List[str]]
    other_title: NotRequired[List[str]]
    source_collection: NotRequired[Union[str, List[str]]]
    subjects: NotRequired[List[str]]
    translated_title: NotRequired[List[str]]
    call_number: NotRequired[Union[str, List[str]]]
    contributors: NotRequired[List[str]]
    number_former_id: NotRequired[List[str]]
    contents: NotRequired[Union[str, List[str]]]
    creator: NotRequired[str]
    genre: NotRequired[List[str]]
    summary: NotRequired[Union[str, List[str]]]
    rights: NotRequired[str]
    reproduction_number: NotRequired[Union[str, List[str]]]
    access_advisory: NotRequired[Union[str, List[str]]]
    related_items: NotRequired[List[RelatedItem]]
    rights_advisory: NotRequired[Union[str, List[str]]]
    control_number: NotRequired[str]
    created: NotRequired[str]
    created_published_date: NotRequired[str]
    creators: NotRequired[List[Creator]]
    display_offsite: NotRequired[bool]
    formats: NotRequired[List[Format]]
    id: NotRequired[str]
    link: NotRequired[str]
    marc: NotRequired[str]
    medium_brief: NotRequired[str]
    mediums: NotRequired[List[str]]
    modified: NotRequired[str]
    resource_links: NotRequired[List[str]]
    rights_information: NotRequired[str]
    service_low: NotRequired[str]
    service_medium: NotRequired[str]
    sort_date: NotRequired[str]
    source_created: NotRequired[str]
    source_modified: NotRequired[str]
    stmt_of_responsibility: NotRequired[str]
    subject_headings: NotRequired[List[str]]
    thumb_gallery: NotRequired[str]


class Resource(TypedDict):
    # The number of files.
    files: NotRequired[int]
    # The image URL.
    image: NotRequired[str]
    # The metadata query URL.
    search: NotRequired[str]
    segments: NotRequired[int]
    # The collection entry URL on loc.gov.
    url: NotRequired[str]
    caption: NotRequired[str]
    captions: NotRequired[Union[str, int]]
    zip: NotRequired[str]
    pdf: NotRequired[str]
    representative_index: NotRequired[int]
    djvu_text_file: NotRequired[str]
    fulltext_derivative: NotRequired[str]
    fulltext_file: NotRequired[str]
    paprika_resource_path: NotRequired[str]
    version: NotRequired[int]


class Segment(TypedDict):
    count: int
    link: str
    url: str


class Related(TypedDict):
    neighbors: str
    group_record: NotRequired[str]


class SourceData(TypedDict):
    access_restricted: bool
    # Alternative identifiers for documents (e.g., shortcut urls).
    aka: List[str]
    campaigns: List[Any]
    digitized: bool
    # Timestamp of most recent ETL (extract-transform-load)
    # process that produced this item. In ISO 8601 format, UTC.
    extract_timestamp: str
    # The ETL processes that produced this item.
    # For many items, different attributes are contributed by different ETL processes.
    group: List[str]
    # Whether this item has segmented data
    # (pages, bounding boxes of images, audio segmentation, etc.) in the index.
    hassegments: bool
    # HTTP version of the URL for the item, including its identifier. Always appears.
    id: str
    # URLs for images in various sizes, if available.
    # If the item is not something that has an image
    # (e.g. it's a book that's not digitized or an exhibit),
    # the URL for the image might be for an icon image file.
    image_url: List[str]
    index: int
    # The item attribute of the item response object provides
    # subfields with information for display of the item on the loc.gov website.
    item: Item
    # Formats available for download.
    mime_type: List[str]
    # Format available via the website.
    online_format: List[str]
    # The kind of object being described (not the digitized version).
    original_format: List[str]
    # Alternative language titles and other alternative titles.
    other_title: List[str]
    # Collections, divisions, units in the Library of Congress,
    # or any of a number of less formal groupings and subgroupings used for organizing content.
    partof: List[str]
    resources: List[Resource]
    # The primary sorting field of the item record.
    # This field really only has meaning within loc.gov, and is not a canonical identifier.
    shelf_id: str
    timestamp: str
    title: str
    # URL on the loc.gov website.
    # If the items is something in the library catalog,
    # the URL will start with lccn.loc.gov.
    url: str
    date: NotRequired[str]
    dates: NotRequired[List[str]]
    description: NotRequired[List[str]]
    language: NotRequired[List[str]]
    location: NotRequired[List[str]]
    number: NotRequired[List[str]]
    number_source_modified: NotRequired[List[str]]
    number_related_items: NotRequired[List[str]]
    segments: NotRequired[List[Segment]]
    site: NotRequired[List[str]]
    number_lccn: NotRequired[List[str]]
    subject: NotRequired[List[str]]
    contributor: NotRequired[List[str]]
    location_country: NotRequired[List[str]]
    location_county: NotRequired[List[str]]
    location_state: NotRequired[List[str]]
    location_city: NotRequired[List[str]]
    number_former_id: NotRequired[List[str]]
    number_carrier_type: NotRequired[List[str]]
    number_oclc: NotRequired[List[str]]
    type: NotRequired[List[str]]
    related: NotRequired[Related]
    reproductions: NotRequired[str]
    unrestricted: NotRequired[bool]
    publication_frequency: NotRequired[List[str]]


class MetadataEntry(BaseMetadataEntry):
    """The data structure of an entry in the metadata."""
    sourceData: SourceData

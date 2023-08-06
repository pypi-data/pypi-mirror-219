"""
Private utility functions for metadata.
"""

import os
from datetime import datetime, timezone
from typing import List

from dateutil import parser

from ..typing import MetadataEntry
from .jsonl import load_jl, save_jl


def deduplicate(metadata_path: str) -> None:
    """
    Deduplicate metadata.
    Load the metadata and deduplicate by `idInSource`.
    For the entries with the same `idInSource`, only keep the latest one.

    Args
    ----
    metadata_path : str
        The path to the metadata to be read and edited.
    """

    entries = load_jl(metadata_path)
    id_in_source_to_entry = {}
    for d in entries:
        id_in_source = d['idInSource']
        if id_in_source not in id_in_source_to_entry:
            id_in_source_to_entry[id_in_source] = d
            continue
        prev_access_date = parser.parse(
            id_in_source_to_entry[id_in_source]['accessDate'])
        new_access_date = parser.parse(d['accessDate'])
        if new_access_date > prev_access_date:
            id_in_source_to_entry[id_in_source] = d
    save_jl(id_in_source_to_entry.values(), metadata_path)


def filter_queries(queries: List[str],
                   metadata_path: str) -> List[str]:
    """
    Filter stale queries.
    Discard the metadata queries that have been executed
    in the recent 30 days.
    """

    metadata: List[MetadataEntry] = []
    if os.path.exists(metadata_path):
        metadata = load_jl(metadata_path)

    # Regard the data queried 30 days ago as stale.
    # Stale queries will be executed again.
    stale_threshold = 30
    now = datetime.now(timezone.utc)
    queried_urls = set()
    for d in metadata:
        access_date = parser.parse(d['accessDate'])
        delta = now - access_date
        if delta.days < stale_threshold:
            queried_urls.add(d['url'])
    return [d for d in queries if d not in queried_urls]

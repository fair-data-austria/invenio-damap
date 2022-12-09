# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 TU Wien.
#
# Invenio is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Functionality for exporting an RDM record to RDA DMP Common Standard."""

from flask import current_app


def export_as_madmp(record_item):
    """Export the given RecordItem in RDA DMP Common Standard."""
    metadata = record_item.data["metadata"]
    embargo_end_date = record_item.data["access"]["embargo"].get("until")

    # fields for "dataset"
    dataset_id = record_item.id
    title = metadata.get("title", "")
    description = metadata.get("description", "")
    publication_date = metadata.get("publication_date")
    keywords = [subject["subject"] for subject in metadata.get("subjects", [])]
    language = metadata["languages"][0]["id"] if metadata.get("languages") else None
    type_ = metadata["resource_type"]["title"]["en"]

    # some fields are basically constant across all records
    metadata_ = {
        "description": "Metadata according to the DataCite 4.3 kernel",
        "language": "eng",
        "metadata_standard_id": {
            "identifier": "http://schema.datacite.org/meta/kernel-4.3/",
            "type": "url",
        },
    }
    personal_data = "unknown"
    sensitive_data = "unknown"

    # not easily available from technical information:
    data_quality_assurance = None
    preservation_statement = None
    security_and_privacy = None
    technical_resource = None

    # fields for "distribution":
    if record_item._record.files.enabled:
        _files = list(record_item._record.files.values())
        download_url = record_item.links[
            "files"
        ]  # FIXME this only points to another JSON object
        byte_size = sum([file_rec.file.size for file_rec in _files])
        formats = [
            f.object_version.mimetype for f in _files if f.object_version.mimetype
        ]
    else:
        _files = []
        download_url = None  # TODO skip this record altogether?
        byte_size = 0
        formats = []

    landing_page_url = record_item.links["self_html"]
    available_until = None
    data_access = "open" if record_item.data["access"]["status"] == "open" else "closed"
    licenses = [
        {
            "license_ref": lic.get("props", {}).get("url"),
            "start_date": embargo_end_date or publication_date,
        }
        for lic in metadata.get("rights", [])
    ]
    host = {
        "title": str(current_app.config["THEME_SITENAME"]),
        "url": str(current_app.config["SITE_UI_URL"]),
        "availability": None,
        "backup_frequency": None,
        "backup_type": None,
        "certified_with": None,
        "description": None,
        "geo_location": None,
        "pid_system": None,
        "storage_type": None,
        "support_versioning": None,
    }

    # tying it together
    distribution = {
        "access_url": landing_page_url,
        "available_until": available_until,
        "byte_size": byte_size,
        "data_access": data_access,
        "description": description,
        "download_url": download_url,
        "format": formats,
        "host": host,
        "license": licenses,
        "title": title,
    }

    dataset = {
        "data_quality_assurance": data_quality_assurance,
        "dataset_id": dataset_id,
        "description": description,
        "distribution": [distribution],
        "issued": publication_date,
        "keyword": keywords,
        "language": language,
        "metadata": metadata_,
        "personal_data": personal_data,
        "preservation_statement": preservation_statement,
        "security_and_privacy": security_and_privacy,
        "sensitive_data": sensitive_data,
        "technical_resource": technical_resource,
        "title": title,
        "type": type_,
    }

    return dataset

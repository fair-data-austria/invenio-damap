# -*- coding: utf-8 -*-
#
# Copyright (C) 2022      Graz University of Technology.
# Copyright (C) 2023-2024 TU Wien.
#
# Invenio-DAMAP is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio-DAMAP resource configuration."""

import marshmallow as ma
from flask_resources import HTTPJSONException, ResourceConfig, create_error_handler
from invenio_i18n import lazy_gettext as _
from invenio_records_resources.resources.errors import ErrorHandlersMixin
from invenio_records_resources.resources.records.args import SearchRequestArgsSchema

from ..services.errors import InvenioDAMAPError

invenio_damap_error_handlers = {
    **ErrorHandlersMixin.error_handlers,
    InvenioDAMAPError: create_error_handler(
        lambda e: HTTPJSONException(
            code=400,
            description=e.description,
        )
    ),
}


class InvenioDAMAPSearchRequestArgsSchema(SearchRequestArgsSchema):
    """Invenio-DAMAP request parameters."""

    sort_direction = ma.fields.Str()


class InvenioDAMAPResourceConfig(ResourceConfig):
    """Invenio-DAMAP resource config."""

    # Blueprint configuration
    blueprint_name = "invenio_damap"
    url_prefix = "/invenio_damap"
    routes = {
        "damap-prefix": "/damap",
        "dmp-prefix": "/dmp",
        "list": "",
        "dataset": "/dataset",
        "record-id": "/<recid>",
        "dmp-id": "/<dmpid>",
        "user-prefix": "/user",
    }

    # Request parsing
    request_read_args = {}
    request_view_args = {
        "recid": ma.fields.String(),
        "dmpid": ma.fields.String(),
    }

    request_extra_args = {
        "title": ma.fields.String(),
        "description": ma.fields.String(),
    }
    request_search_args = InvenioDAMAPSearchRequestArgsSchema

    error_handlers = invenio_damap_error_handlers

# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2024 Graz University of Technology.
# Copyright (C) 2024 TU Wien.
#
# Invenio-DAMAP is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio-DAMAP service API configuration."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services import ServiceConfig
from invenio_records_resources.services.base.config import ConfiguratorMixin, FromConfig
from invenio_records_resources.services.records.links import pagination_links
from sqlalchemy import asc, desc

from invenio_damap.services.schema import InvenioDAMAPSchema, LinkedUserSchema

from ..services.permissions import InvenioDAMAPPermissionPolicy
from ..services.results import DMPItem, DMPList


class SearchOptions:
    """Search options."""

    sort_default = "created"
    sort_direction_default = "asc"

    sort_direction_options = {
        "asc": dict(
            title=_("Ascending"),
            fn=asc,
        ),
        "desc": dict(
            title=_("Descending"),
            fn=desc,
        ),
    }

    sort_options = {
        "name": dict(
            title=_("Name"),
            fields=["name"],
        ),
        "spec": dict(
            title=_("Spec"),
            fields=["spec"],
        ),
        "created": dict(
            title=_("Created"),
            fields=["created"],
        ),
        "updated": dict(
            title=_("Updated"),
            fields=["updated"],
        ),
    }
    pagination_options = {
        "default_results_per_page": 25,
    }


class InvenioDAMAPServiceConfig(ServiceConfig, ConfiguratorMixin):
    """Service factory configuration."""

    damap_base_url = FromConfig("DAMAP_BASE_URL", "")
    damap_person_function = FromConfig("DAMAP_PERSON_FUNCTION")
    damap_custom_header_function = FromConfig("DAMAP_CUSTOM_HEADER_FUNCTION")
    damap_shared_secret = FromConfig("DAMAP_SHARED_SECRET")

    service_id = "invenio_damap"

    # Common configuration
    permission_policy_cls = InvenioDAMAPPermissionPolicy
    result_item_cls = DMPItem
    result_list_cls = DMPList

    # Search configuration
    search = SearchOptions

    # Service schema
    schema = InvenioDAMAPSchema
    linked_user_schema = LinkedUserSchema

    links_item = {}

    links_search = {
        **pagination_links("{+api}/invenio_damap/damap/dmp{?args*}"),
    }

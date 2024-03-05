# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
# Copyright (C) 2024 TU Wien.
#
# Invenio-DAMAP is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio-DAMAP service."""

from typing import Optional

import requests
from flask_babelex import lazy_gettext as _
from flask_sqlalchemy import Pagination
from invenio_accounts.models import User
from invenio_rdm_records.proxies import current_rdm_records_service
from invenio_records_resources.records import Record
from invenio_records_resources.services import Service
from invenio_records_resources.services.base import LinksTemplate
from invenio_records_resources.services.records.schema import (
    ServiceSchemaWrapper,
)
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import text

from invenio_damap import export as InvenioDAMAPExport
from invenio_damap.resolvers import default_namespace_id_resolver
from invenio_damap.services.errors import (
    InvenioDAMAPDMPNotFoundError,
    InvenioDAMAPError,
)


class InvenioDAMAPService(Service):
    """Invenio-DAMAP service."""

    def __init__(self, config):
        """Init service with config."""
        super().__init__(config)

    @property
    def schema(self):
        """Returns the data schema instance."""
        return ServiceSchemaWrapper(self, schema=self.config.schema)

    @property
    def links_item_tpl(self):
        """Item links template."""
        return LinksTemplate(
            self.config.links_item,
        )

    def _create_headers(self, identity):
        """Creates the auth header and additonal ones, if defined."""
        headers = {
            "Authorization": self.config.damap_shared_secret,
        }

        headers.update(self.config.damap_custom_header_function(identity=identity))

        return headers

    def _get_user_id(self, identity):
        """Get the user id from the identity."""
        return self.config.damap_person_id_function(identity=identity)
    
    @property
    def resolve_user(self, namespaced_ids: dict) -> Optional[User]:
        """
        Resolves user from namespaced ID.

        Parameters:
            namespaced_ids (dict): A dictionary where namespace name and ids are stored.

        Returns:
            User: The resolved user object.
        """
        users = [
            self.config.damap_user_id_resolver(ns, ns_id)
            for ns, ns_id in namespaced_ids.items()
        ]

        # eliminate possible duplicates and "nulls"
        users = set(user for user in users if user is not None)

        if len(users) == 1:
            return users[0]
        else:
            return None

    def add_record_to_dmp(self, identity, recid, dmp_id, data):
        """Add the provided record to the DMP"""

        person_id = self._get_user_id(identity=identity)
        headers = self._create_headers(identity)

        # this will also perform permission checks, ensuring the user may access the record.
        record = current_rdm_records_service.read(identity, recid)
        exported_record = InvenioDAMAPExport.export_as_madmp(record, **data)

        r = requests.post(
            url=self.config.damap_base_url
            + "/api/invenio-damap/dmps/{}/{}".format(dmp_id, person_id),
            headers=headers,
            json=exported_record,
        )

        r.raise_for_status()

        return record

    def search(self, identity, params):
        """Perform search for DMPs."""
        self.require_permission(identity, "read")

        search_params = self._get_search_params(params)
        # TODO: get user id from resolver here
        person_id = self._get_user_id(identity=identity)
        headers = self._create_headers(identity)

        r = requests.get(
            url=self.config.damap_base_url
            + "/api/invenio-damap/dmps/person/{}".format(person_id),
            headers=headers,
            params=search_params,
        )

        r.raise_for_status()

        dmps = Pagination(
            query=None,
            items=r.json(),
            page=search_params["page"],
            per_page=search_params["size"],
            total=10,
        )

        return self.result_list(
            self,
            identity,
            dmps,
            params=search_params,
            links_tpl=LinksTemplate(self.config.links_search, context={"args": params}),
            links_item_tpl=self.links_item_tpl,
        )

    def _get_search_params(self, params):
        page = params.get("page", 1)
        size = params.get(
            "size",
            self.config.search.pagination_options.get("default_results_per_page"),
        )

        _search_cls = self.config.search

        _sort_name = (
            params.get("sort")
            if params.get("sort") in _search_cls.sort_options
            else _search_cls.sort_default
        )
        _sort_direction_name = (
            params.get("sort_direction")
            if params.get("sort_direction") in _search_cls.sort_direction_options
            else _search_cls.sort_direction_default
        )

        sort = _search_cls.sort_options.get(_sort_name)
        sort_direction = _search_cls.sort_direction_options.get(_sort_direction_name)

        query_params = params.get("q", "")

        return {
            "page": page,
            "size": size,
            "sort": sort.get("fields"),
            "sort_direction": sort_direction.get("fn"),
            "q": query_params,
        }

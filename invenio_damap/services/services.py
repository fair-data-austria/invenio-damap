# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2024 Graz University of Technology.
#
# Invenio-DAMAP is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio-DAMAP service."""

from time import time

import jwt
import requests
from flask_babelex import lazy_gettext as _
from flask_sqlalchemy import Pagination
from invenio_rdm_records.proxies import current_rdm_records_service
from invenio_records_resources.services import Service
from invenio_records_resources.services.base import LinksTemplate
from invenio_records_resources.services.records.schema import ServiceSchemaWrapper

from invenio_damap import export as InvenioDAMAPExport
from invenio_damap.services.errors import InvenioDAMAPPersonNotLinkedError


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
    def linked_user_schema(self):
        """Returns the linked user data schema instance."""
        return ServiceSchemaWrapper(self, schema=self.config.linked_user_schema)

    @property
    def links_item_tpl(self):
        """Item links template."""
        return LinksTemplate(
            self.config.links_item,
        )

    def _create_auth_jwt(self, identity, expires_in=600):
        """Creates an authorization jwt token for DAMAP."""
        return jwt.encode(
            {
                "exp": time() + expires_in,
                **self.config.damap_person_function(identity),
            },
            self.config.damap_shared_secret,
            algorithm="HS256",
        )

    def _create_headers(self, identity, *args, **kwargs):
        """Creates the auth header and additonal ones, if defined."""
        headers = {"Authorization": f"Bearer {self._create_auth_jwt(identity)}"}
        headers.update(self.config.damap_custom_header_function(identity=identity))
        print("Headers: ", headers, flush=True)
        return headers

    def _get_linked_user(self, identity, user_id=None, **kwargs):
        """Read the linked user either from the identity or the provided user id."""
        headers = self._create_headers(identity)

        r = requests.post(
            url=self.config.damap_base_url
            + "/api/invenio-damap/dmps/",
            headers=headers,
        )

        r.raise_for_status()

        return r.status_code

    def read_linked_user(self, identity, **kwargs):
        """Read the linked user from the identity."""
        linked_user = self._get_linked_user(identity, **kwargs)

        return self.result_item(
            self,
            identity,
            linked_user,
            schema=self.linked_user_schema,
            links_tpl=None,
        )

    def add_record_to_dmp(self, identity, recid, dmp_id, data, **kwargs):
        """Add the provided record to the DMP"""

        person_id = self._get_linked_user(identity=identity)["id"]
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

    def search(self, identity, params, **kwargs):
        """Perform search for DMPs."""
        self.require_permission(identity, "read")

        search_params = self._get_search_params(params)
        person_id = self._get_linked_user(identity=identity)["id"]
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

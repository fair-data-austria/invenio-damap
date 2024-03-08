# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
# Copyright (C) 2022-2024 TU Wien.
#
# Invenio-DAMAP is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module for connection to DAMAP."""

from invenio_damap.resources import InvenioDAMAPResource, InvenioDAMAPResourceConfig
from invenio_damap.services import InvenioDAMAPService, InvenioDAMAPServiceConfig

from . import config


class InvenioDAMAP(object):
    """Invenio-DAMAP extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["invenio-damap"] = self

        self.init_services(app)
        self.init_resource(app)

    def init_config(self, app):
        """Initialize configuration.

        Override configuration variables with the values in this package.
        """
        for k in dir(config):
            if k.startswith("DAMAP_"):
                app.config.setdefault(k, getattr(config, k))

    def init_services(self, app):
        """Initialize service."""
        # Services
        self.invenio_damap_service = InvenioDAMAPService(
            InvenioDAMAPServiceConfig.build(app),
        )

    def init_resource(self, app):
        """Initialize resources."""
        # Resources
        self.invenio_damap_resource = InvenioDAMAPResource(
            InvenioDAMAPResourceConfig(),
            self.invenio_damap_service,
        )

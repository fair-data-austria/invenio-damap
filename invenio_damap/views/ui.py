# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 Graz University of Technology.
# Copyright (C) 2024 TU Wien.
#
# Invenio-DAMAP is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""UI views."""

from flask import Blueprint, current_app, g


#
# Registration
#
def create_ui_blueprint(app):
    """Register blueprint routes on app."""
    blueprint = Blueprint(
        "invenio_damap",
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    @blueprint.app_template_global("create_auth_jwt")
    def create_auth_jwt():
        """Helper function for jinja templates to create a JWT token for the user."""

        jwt = current_app.extensions[
            "invenio-damap"
        ].invenio_damap_service._create_auth_jwt(g.identity)

        return jwt

    @blueprint.app_template_global("query_damap_madmps")
    def query_damap_madmps(user_jwt):
        """Helper function for jinja templates to fetch maDMPs."""

        dmps = current_app.extensions["invenio-damap"].invenio_damap_service.search(
            g.identity, params={}, jwt_token=user_jwt
        )

        return dmps

    return blueprint

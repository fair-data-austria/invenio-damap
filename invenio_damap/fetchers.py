# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
# Copyright (C) 2024 TU Wien.
#
# Invenio-DAMAP is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

from flask import current_app
from invenio_oauthclient.models import RemoteAccount


def custom_header_fetcher(identity, user_id=None, *args, **kwargs):
    return {}


def user_fetcher(identity, user_id=None, *args, **kwargs):
    ra = RemoteAccount.get(
        user_id=user_id or identity.id, client_id=current_app.config["DAMAP_REMOTE_CLIENT_ID"]
    )
    return ra.user if ra is not None else None

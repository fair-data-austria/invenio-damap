# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#
# Invenio-DAMAP is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Utility functions."""

from requests import get


def parse_tiss_response(url):
    response = get(url)

    if response.status_code == 200 and "application/json" in response.headers.get(
        "Content-Type", ""
    ):

        to_json = response.json()
        person_email = to_json.get("main_email")

        return person_email
    return None

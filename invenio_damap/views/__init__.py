# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 Graz University of Technology.
#
# Invenio-DAMAP is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Views."""

from .api import blueprint, create_invenio_damap_api_blueprint

__all__ = (
    "blueprint",
    "create_invenio_damap_api_blueprint",
)

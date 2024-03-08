# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2024 TU Wien.
#
# Invenio-DAMAP is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""JS/CSS Webpack bundles for Invenio-DAMAP."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    import_name=__name__,
    folder="assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "invenio-damap": "./js/invenio_damap/index.js",
            },
            dependencies={
                "jquery": "^3.2.1",
            },
        ),
    },
)

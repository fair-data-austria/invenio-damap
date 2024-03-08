# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2024 Graz University of Technology.
#
# Invenio-DAMAP is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio-DAMAP API schemas."""

from marshmallow import EXCLUDE, Schema, fields, validate
from marshmallow_utils.fields import NestedAttribute, SanitizedUnicode


class InvenioDAMAPProjectSchema(Schema):
    """Marshmallow schema for Invenio-DAMAP project."""

    id = fields.Int()
    description = SanitizedUnicode(load_default=None, dump_default=None)
    title = SanitizedUnicode(required=True, validate=validate.Length(min=1, max=255))

    class Meta:
        """Meta attributes for the schema."""

        unknown = EXCLUDE
        ordered = True


class InvenioDAMAPDatasetSchema(Schema):
    """Marshmallow schema for Invenio-DAMAP dataset."""

    class InvenioDAMAPDatasetIdentifier(Schema):
        """Marshmallow schema for the dataset identifier."""

        type = fields.Str()
        identifier = fields.Str()

    description = SanitizedUnicode(load_default=None, dump_default=None)
    title = SanitizedUnicode(required=True, validate=validate.Length(min=1, max=255))
    datasetId = fields.Nested(
        data_key="datasetId", nested=InvenioDAMAPDatasetIdentifier
    )

    class Meta:
        """Meta attributes for the schema."""

        unknown = EXCLUDE
        ordered = True


class InvenioDAMAPSchema(Schema):
    """Marshmallow schema for Invenio-DAMAP maDMP."""

    id = fields.Int()
    created = fields.Str()
    project = fields.Nested(nested=InvenioDAMAPProjectSchema)
    datasets = fields.List(fields.Nested(nested=InvenioDAMAPDatasetSchema))

    class Meta:
        """Meta attributes for the schema."""

        unknown = EXCLUDE
        ordered = True


class LinkedUserSchema(Schema):
    """Marshmallow schema for DAMAP user."""

    id = fields.Str()

    class Meta:
        """Meta attributes for the schema."""

        unknown = EXCLUDE
        ordered = True

# -*- coding: utf-8 -*-
#
# Copyright (C) 2022      Graz University of Technology.
# Copyright (C) 2023-2024 TU Wien.
#
# Invenio-DAMAP is free software; you can redistribute it and/or modify
# under the terms of the MIT License; see LICENSE file for more details.

"""Errors for InvenioDAMAP."""

from invenio_i18n import gettext as _


class InvenioDAMAPError(Exception):
    """Base class for InvenioDAMAP errors."""

    def __init__(self, *args: object):
        """Constructor."""
        super().__init__(*args)


class InvenioDAMAPDMPNotFoundError(InvenioDAMAPError):
    """Class when a DMP can not be found."""

    def __init__(self, id, *args: object):
        """Constructor."""
        super().__init__(_("Can not find DMP with id `{}`".format(id)), *args)

# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#
# Invenio-DAMAP is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Identity resolvers."""

from typing import Union

from invenio_accounts.models import User
from requests import get

from .utils import parse_tiss_response


def default_namespace_id_resolver(namespace: str, id_: str) -> Union[User, None]:
    """
    Resolves identity given a namespace.
    This is the default resolver, modify it according to your needs.

    Parameters:
        namespace (str): Namespace type, can indicate a field like email or a system.
        id_ (str): person ID to look for if the namespace is another system

    Returns:
        User: Resolved User object or None.
    """
    if namespace == "email":
        return None
    elif namespace == "tiss":
        return parse_tiss_response(get(f"https://tiss.tuwien.ac.at/api/person/{id_}"))
    else:
        return None

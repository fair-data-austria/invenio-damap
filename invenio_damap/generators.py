# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#
# Invenio-DAMAP is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Identity generators."""

from invenio_accounts.models import User


def default_namespaced_id_generator(user: User) -> dict[str, str]:
    """
    Generates user identities mapped to namespace names.
    This is the default generator, modify it according to your needs.

    Parameters:
        user (User): The user object.

    Returns:
        dict: Namespaces with the user identifiers.
    """
    return {
        "email": user.email,
        "keycloak_id": user.external_accounts[0].id,
    }

# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#
# Invenio-DAMAP is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Identity generators."""

import jwt

from typing import Union

from flask import current_app
from flask_principal import AnonymousIdentity


def default_namespaced_id_generator(
    identity, *args, **kwargs
) -> Union[dict[str, str], None]:
    """
    Generates user identities mapped to namespace names.
    This is the default generator, which returns the user email as the primary identity.
    Modify it according to your needs.

    Parameters:
        identity: The user identity.

    Returns:
        dict: Namespaces with the user identifiers, othwerwise None if user is unverified.
    """
    if identity and not isinstance(identity, AnonymousIdentity):
        user = identity.user
        for ra in user.remote_accounts:
            for token in ra.remote_tokens:
                dec_token = jwt.decode(
                    token, current_app.config["SECRET_KEY"], algorithms=["RS256"]
                )

                # email value can be also taken from the decoded token
                if dec_token["email_verified"]:
                    return {"email": user.email}
                
        # if there's no remote token with verified email, return the user account email
        return {"email": user.email}

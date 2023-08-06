# Copyright 2023 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

from qctrlclient import (
    CliAuth,
    GraphQLClient,
    get_default_api_url,
    get_default_cli_auth,
)
from qctrlclient.core import (
    ApiRouter,
    CoreClientSettings,
    LocalRouter,
    Product,
)
from qctrlclient.core.utils import show_error_message
from qctrlclient.exceptions import GraphQLClientError
from qctrlclient.globals import global_value

from .constants import INVALID_SUBSCRIPTION_ERROR


def _get_graphql_client(api_url: str, auth: CliAuth) -> GraphQLClient:
    """Returns a `GraphQLClient` and checks the user
    has the required access for CLI usage.
    """
    client = GraphQLClient(api_url, auth=auth)

    try:
        client.check_user_role("fire-opal-cli-access")
    except GraphQLClientError:
        show_error_message(INVALID_SUBSCRIPTION_ERROR)

    return client


def get_default_router() -> ApiRouter:
    """Returns the default router that the Fire Opal
    client uses.
    """
    client = _get_graphql_client(get_default_api_url(), get_default_cli_auth())
    settings = get_config()
    return ApiRouter(client, settings)


@global_value("FIRE_OPAL_CONFIG")
def get_config() -> CoreClientSettings:
    """Returns the global Fire Opal settings."""
    return CoreClientSettings(router=get_default_router, product=Product.FIRE_OPAL)


def configure(**kwargs) -> None:  # type: ignore
    """
    Updates the global Fire Opal settings. See `CoreClientSettings`
    for details on which fields can be updated.

    Parameters
    ----------
    **kwargs
        Arbitrary keyword arguments to update the configuration.
    """
    config = get_config()
    config.update(**kwargs)


def configure_api(api_url: str, oidc_url: str) -> None:
    """Convenience function to configure Fire Opal for API
    routing.

    Parameters
    ----------
    api_url : str
        URL of the GraphQL schema
    oidc_url : str
        Base URL of the OIDC provider e.g. Keycloak
    """
    client = _get_graphql_client(api_url, CliAuth(oidc_url))
    settings = get_config()

    configure(router=ApiRouter(client, settings))


def configure_local(resolver: "BaseResolver") -> None:  # type: ignore
    """Convenience function to configure Fire Opal for local
    routing.

    Parameters
    ----------
    resolver : BaseResolver
        A local implementation of a workflow resolver which uses
        a registry that implements all of the available Fire Opal
        workflows
    """
    configure(router=LocalRouter(resolver))


def configure_organization(organization_slug: str) -> None:
    """Convenience function to configure the organization.

    Parameters
    ----------
    organization_slug : str
        Unique slug for the organization.
    """
    configure(organization=organization_slug)

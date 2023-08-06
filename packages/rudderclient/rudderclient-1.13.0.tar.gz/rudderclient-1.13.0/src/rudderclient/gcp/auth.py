"""
GCP Authentication library.

This library provides an easy way for authenticating to GCP services. Also offers a simple method
to read a value secret interacting with secretmanager API.

"""


from google.cloud import secretmanager
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from google.oauth2 import service_account


def get_secret(secret_id):
    """
    Returns a secret value from secret manager service.

    Parameters:
    ----------
        secret_id: str
            Secret resource name like projects/xxxxxx/secrets/xxxxxxxx/versions/latest

    Returns:
    -------
    The value of the secret.
    """
    client = secretmanager.SecretManagerServiceClient()
    secret = client.access_secret_version(request={"name": secret_id})
    value = secret.payload.data.decode("UTF-8")
    return value


def get_oidc_token_iap_request(client_id, **kwargs):
    """
    Returns a token for doing an HTTP request to an application protected by Identity-Aware Proxy.

    Parameters:
    ----------
        client_id: The client ID used by Identity-Aware Proxy
        **kwargs: Any of the parameters defined for the request function:
                https://github.com/requests/requests/blob/master/requests/api.py
                If no timeout is provided, it is set to 90 by default.

    Returns:
    -------
    An OpenID Connect (OIDC) token from metadata server.
    """
    # Set the default timeout, if missing
    if "timeout" not in kwargs:
        kwargs["timeout"] = 90

    # Obtain an OpenID Connect (OIDC) token from metadata server or using service
    # account.
    open_id_connect_token = id_token.fetch_id_token(Request(), client_id)

    return open_id_connect_token


def get_workspace_impersonate_credentials_sa(
    credentials_info, scopes, impersonate_mail
):
    """
    Obtain the credentials with the permissions of the service account, in an impersonal way.

    Parameters:
    ----------
        credentials_info: json access key of the service account.
        scopes: Array of the granular permissions that determine what specific resources and operations the service
                account can access.
        impersonate_mail: Email to impersonate the service account.

    Returns:
    -------
    The impersonate credentials with the service account and scope permissions.
    """
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info
    )

    scoped_credentials = credentials.with_scopes(scopes)

    impersonate_credentials = scoped_credentials.with_subject(impersonate_mail)

    return impersonate_credentials

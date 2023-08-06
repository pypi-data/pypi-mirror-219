import requests
import json

from requests.structures import CaseInsensitiveDict


def get_bearer_token(tenant, client_id, scope, client_secret, grant_type):
    """
    Return an access token using the client secret.

    Parameters:
    ----------
        tenant: The directory tenant that you want to request permission from.
        client_id: The application ID that the Azure app registration portal assigned when you registered your app.
        scope: the identifier (app ID URI) of the resource you want, affixed with the .default suffix.
            For example, the Microsoft Graph resource app ID URI is https://graph.microsoft.com/.
            For Microsoft Graph, the value of scope is therefore https://graph.microsoft.com/.default.
        client_secret: The client secret that you generated for your app in the app registration portal.
            Ensure that it's URL encoded.
        grant_type: Must be `client_credentials`.

    """

    url_get_token = (
        f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    )
    headers_token = CaseInsensitiveDict()
    headers_token["Content_Type"] = "x-www-form-urlencoded"
    data = {
        "client_id": {client_id},
        "scope": {scope},
        "client_secret": {client_secret},
        "grant_type": {grant_type},
    }

    r_token = requests.get(url_get_token, data=data, headers=headers_token)
    response = r_token.content
    reponse_decode = response.decode("utf-8")
    json_response = json.loads(reponse_decode)

    bearer_token = json_response["access_token"]

    return bearer_token


def get_user(userPrincipalName, token):
    """
    Retrieve the properties and relationships of the user object.

    Parameters:
    ----------
    userPrincipalName: email of the user registered.
    token: Bearer {token}.

    """

    headers = CaseInsensitiveDict()
    headers["Authorization"] = f"Bearer {token}"

    url_get_user = (
        f"https://graph.microsoft.com/v1.0/users/{userPrincipalName}"
    )
    get_response = requests.get(url_get_user, headers=headers)
    return get_response.status_code


def delete_user(userPrincipalName, token):
    """
    Delete an Azure account.

    Parameters:
    ----------
    userPrincipalName: email of the user registered.
    token: Bearer {token}.

    """

    headers = CaseInsensitiveDict()
    headers["Authorization"] = f"Bearer {token}"

    url_delete_user = (
        f"https://graph.microsoft.com/v1.0/users/{userPrincipalName}"
    )
    requests.delete(url_delete_user, headers=headers)


def create_user(userPrincipalName, displayName, pwd, token):
    """
    Create an Azure account.

    Parameters:
    ----------
    userPrincipalName: email of the user registered.
    displayName: the name to display in the address book for the user.
    pwd: random password profile for the user.
    token: Bearer {token}.

    """

    headers = CaseInsensitiveDict()
    headers["Authorization"] = f"Bearer {token}"
    headers["Content-Type"] = "application/json"

    url_create_user = "https://graph.microsoft.com/v1.0/users"

    mailNickname = userPrincipalName.split("@")[0]

    data = {
        "accountEnabled": True,
        "displayName": f"{displayName}",
        "mailNickname": f"{mailNickname}",
        "userPrincipalName": f"{userPrincipalName}",
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": f"{pwd}",
        },
    }

    json_data = json.dumps(data)

    response = requests.post(url_create_user, data=json_data, headers=headers)

    return response.status_code

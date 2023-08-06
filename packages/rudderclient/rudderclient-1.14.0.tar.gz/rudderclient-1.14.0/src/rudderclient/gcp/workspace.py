"""
This library provides an easy way to interact with workspace API.

"""

from googleapiclient.discovery import build
from google.oauth2 import service_account


def create_service(service_name, version, credentials):
    """
    Create the necessary service to interact with a specific Google Workspace service in a specific version of its API.

    Parameters:
    ----------
        serviceName: Name of the service.
        version: Version of the service.
        credentials: oauth2client.Credentials or google.auth.credentials.Credentials, credentials to be used for
            authentication. You can get them with 'get_workspace_impersonate_credentials_sa' method.

    """
    service = build(service_name, version, credentials=credentials)
    return service


def user_workspace_exist(credentials, work_email, domain):
    """
    Return true if the user email exists in the Google Workspce domain specificated, and false if not.

    Parameters:
    ----------
        credentials: oauth2client.Credentials or google.auth.credentials.Credentials, credentials to be used for
            authentication. You can get them with 'get_workspace_impersonate_credentials_sa' method.
        work_email: Primary email address of the user to search for.
        domain: The domain name where you want to search for.
    """
    service = create_service("admin", "directory_v1", credentials)
    result = (
        service.users()
        .list(query=work_email, orderBy="email", domain=domain)
        .execute()
    )

    if "users" in result and len(result["users"]) > 0:
        exists = True
    else:
        exists = False

    return exists


def create_workspace_user(
    name,
    surname,
    second_surname,
    personal_email,
    primary_email,
    password,
    credentials,
):
    """
    Create a user in Google workspace.

    Parameters:
    ----------
        name: Name of the user to create.
        surname: First surname of the user to create.
        second_surname: Second surname of the user to create.
        personal_email: Personal email of the user.
        primary_email: Primary email of the user.
        password: First password.
        credentials: oauth2client.Credentials or google.auth.credentials.Credentials, credentials to be used for
            authentication. You can get them with 'get_workspace_impersonate_credentials_sa' method.
    """
    service = create_service("admin", "directory_v1", credentials)

    user_json = {
        "primaryEmail": primary_email,
        "name": {
            "givenName": name,
            "familyName": surname + " " + second_surname,
            "fullName": name + " " + surname + " " + second_surname,
        },
        "password": password,
        "changePasswordAtNextLogin": "true",
        "emails": [
            {"address": personal_email, "type": "home"},
            {"address": primary_email, "type": "work", "primary": "true"},
        ],
        "languages": [
            {"languageCode": "es", "preference": "preferred"},
            {"languageCode": "en-GB", "preference": "preferred"},
        ],
        "orgUnitPath": "/",
        "includeInGlobalAddressList": "true",
    }
    service.users().insert(body=user_json).execute()


def add_member_workspace_group(primary_email, role, group, credentials):
    """
    Add a member into a Google Workspace group with the specified role.

    Parameters:
        primary_email:
        role: The member's role in the group.
            Acceptable values are: MANAGER, OWNER, MEMBER. Visit this link for more information https://developers.google.com/admin-sdk/directory/reference/rest/v1/members#Member
        group: Identifier for the group.
        credentials: oauth2client.Credentials or google.auth.credentials.Credentials, credentials to be used for
            authentication. You can get them with 'get_workspace_impersonate_credentials_sa' method.
    """
    service = create_service("admin", "directory_v1", credentials)

    member_json = {
        "email": primary_email,
        "role": role,
    }
    service.members().insert(body=member_json, groupKey=group).execute()


def update_workspace_license(
    current_product_id,
    current_sku_id,
    current_user_id,
    license_instance,
    credentials,
):
    """
    Update the Google Workspace license of a user already created.

    Parameters:
    ----------
        current_product_id: The current product's unique identifier. You can check it in this link https://developers.google.com/admin-sdk/licensing/v1/how-tos/products
        current_sku_id: The current product SKU's unique identifier. You can check it in this link https://developers.google.com/admin-sdk/licensing/v1/how-tos/products
        current_user_id: The user's current primary email address.
        license_instance: License object instance for the updated.
        Example: {
                    'productId': "Google-Apps",
                    'skuId': "1010020030",
                    'userId': xxxxxx
                    }
        credentials: oauth2client.Credentials or google.auth.credentials.Credentials, credentials to be used for
            authentication. You can get them with 'get_workspace_impersonate_credentials_sa' method.
    """
    service = create_service("licensing", "v1", credentials)
    service.licenseAssignments().update(
        productId=current_product_id,
        skuId=current_sku_id,
        userId=current_user_id,
        body=license_instance,
    ).execute()


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

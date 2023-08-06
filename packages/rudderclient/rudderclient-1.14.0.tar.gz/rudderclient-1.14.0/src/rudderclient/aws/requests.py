"""This library provides an easy way to interact with boto3, the official Python library of AWS."""


import boto3


def get_boto3_client(resource, region, acces_key_id, secret_access_key):
    """
    Returns a low-level service client.

    Parameters:
    ----------
        resource: The name of a service, e.g 'identitystore'. You can get a list of available
                services via get_available_services().
        region: The name of the region associated with the client. A client is associated with a single region.
        access_key_id: The access key to use when creating the client.
        secret_access_key: The secret key to use when creating the client.
    """
    client = boto3.client(
        resource,
        region_name=region,
        aws_access_key_id=acces_key_id,
        aws_secret_access_key=secret_access_key,
    )
    return client


def delete_user(operation_parameters, region, acces_key_id, secret_access_key):
    """
    Deletes a user of a unique identityStore.

    Parameters:
    ----------
        operation_parameters: A dict with the IdentityStoreId and the UserId you want to delete.
                            Example: {'IdentityStoreId': identityStoreId, 'UserId': user_id}
        region: The name of the region associated with the identityStore.
        access_key_id: The access key to use when creating the client.
        secret_access_key: The secret key to use when creating the client.
    """
    # Create IAM client
    client = get_boto3_client(
        "identitystore", region, acces_key_id, secret_access_key
    )

    delete_response = client.delete_user(**operation_parameters)

    return delete_response


def get_identitystore_id(region, acces_key_id, secret_access_key):
    """
    Returns the ID of your organization Identity Store in a unique region.

    Parameters:
    ----------
        region: The name of the region associated with the identityStore.
        access_key_id: The access key to use when creating the client.
        secret_access_key: The secret key to use when creating the client.
    """
    client = get_boto3_client(
        "sso-admin", region, acces_key_id, secret_access_key
    )
    identitystore = client.list_instances()
    identitystore_id = identitystore["Instances"][0]["IdentityStoreId"]
    return identitystore_id


def describe_user(user_id, region, acces_key_id, secret_access_key):
    """
    Returns information of a user.

    Parameters:
    ----------
        user_id: The ID of the user.
        region: The name of the region associated with the identityStore.
        access_key_id: The access key to use when creating the client.
        secret_access_key: The secret key to use when creating the client.

    """
    client = get_boto3_client(
        "identitystore", region, acces_key_id, secret_access_key
    )
    identitystore = get_identitystore_id(
        region, acces_key_id, secret_access_key
    )
    response = client.describe_user(
        IdentityStoreId=identitystore, UserId=user_id
    )
    return response


def create_user(
    user_email, first_name, surnames, region, acces_key_id, secret_access_key
):
    """
    Creates a user in an identity Store.

    Parameters:
    ----------
        userEmail: the work email of the user.
        firstName: Name of the user.
        surnames: One or two surnames of the user.
        region: The name of the region associated with the identityStore.
        access_key_id: The access key to use when creating the client.
        secret_access_key: The secret key to use when creating the client.
    """
    client = get_boto3_client(
        "identitystore", region, acces_key_id, secret_access_key
    )
    identitystore = get_identitystore_id(
        region, acces_key_id, secret_access_key
    )
    display_name = f"{first_name} {surnames}"

    response = client.create_user(
        IdentityStoreId=identitystore,
        UserName=user_email,
        DisplayName=display_name,
        Name={"FamilyName": first_name, "GivenName": surnames},
        Emails=[{"Value": user_email, "Type": "Work", "Primary": True}],
    )
    return response


def pagination(
    action, operation_parameters, region, acces_key_id, secret_access_key
):
    """
    Paginates a list result.

    Parameters:
    ----------
        action: The action you want to paginate. For example, 'list_users'.
        operation_parameters: Necessary parameters for doing the action.
                            For example {'IdentityStoreId': identityStoreId, 'UserId': user_id}
        region: The name of the region associated with the identityStore.
        access_key_id: The access key to use when creating the client.
        secret_access_key: The secret key to use when creating the client.
    """
    # Create IAM client
    client = get_boto3_client(
        "identitystore", region, acces_key_id, secret_access_key
    )

    paginator = client.get_paginator(action)
    page_iterator = paginator.paginate(**operation_parameters)

    return page_iterator

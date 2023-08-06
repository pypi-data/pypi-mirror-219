"""
This library provides an easy way to interact with IAM API.

"""

from googleapiclient.discovery import build


def get_policy(
    credentials,
    project_id: str,
    version: int = 1,
) -> dict:
    """
    Gets IAM policy for a project.

    Parameters:
    ----------
        credentials: oauth2client.Credentials or google.auth.credentials.Credentials, credentials to be used for
            authentication. You can get them with 'get_workspace_impersonate_credentials_sa' method.
        project_id: Name id of the project where you want to get policies.
        version: Version of the policy. By default: 1.
    """

    service = build("cloudresourcemanager", "v1", credentials=credentials)
    policy = (
        service.projects()
        .getIamPolicy(
            resource=project_id,
            body={"options": {"requestedPolicyVersion": version}},
        )
        .execute()
    )

    return policy


def modify_policy_add_member(policy: dict, role: str, member: str) -> dict:
    """
    Adds a new member to a role binding.

    Parameters:
    ----------
        policy: Policy to modify.
        role: The name of the role that you want to grant in the project.
            * Predefined roles: 'SERVICE.IDENTIFIER'
            * Project-level custom roles: 'IDENTIFIER'
        member: User email identifier.
    """
    try:
        binding = next(b for b in policy["bindings"] if b["role"] == role)
        binding["members"].append(member)
        print(f"------------------Binding----------- {binding}")
    except StopIteration:
        binding = {"role": role, "members": [member]}
        policy["bindings"].append(binding)

    return policy


def set_policy(credentials, project_id: str, policy: dict) -> dict:
    """
    Sets IAM policy for a project.

    Parameters:
    ----------
        credentials: oauth2client.Credentials or google.auth.credentials.Credentials, credentials to be used for
            authentication. You can get them with 'get_workspace_impersonate_credentials_sa' method.
        project_id: Name id of the project where you want to get policies.
        policy: Policy to modify.
    """

    service = build("cloudresourcemanager", "v1", credentials=credentials)

    policy = (
        service.projects()
        .setIamPolicy(resource=project_id, body={"policy": policy})
        .execute()
    )

    return policy


def modify_policy_remove_member(policy: dict, role: str, member: str) -> dict:
    """
    Removes a  member from a role binding.
    Parameters:
    ----------
        policy: Policy to modify.
        role: The name of the role that you want to grant in the project.
            * Predefined roles: 'SERVICE.IDENTIFIER'
            * Project-level custom roles: 'IDENTIFIER'
        member: User email identifier.
    """
    binding = next(b for b in policy["bindings"] if b["role"] == role)
    if "members" in binding and member in binding["members"]:
        binding["members"].remove(member)
    print(binding)
    return policy


def remove_user_from_all_projects(credentials, user):
    """
    Remove a user from all GCP projects.

    Parameters:
    ----------
        credentials: oauth2client.Credentials or google.auth.credentials.Credentials, credentials to be used for
            authentication. You can get them with 'get_workspace_impersonate_credentials_sa' method.
        user: User email identifier.
    """
    user_iam_policy = f"user:{user}"
    service = build("cloudresourcemanager", "v1", credentials=credentials)
    response = service.projects().list().execute()

    for project in response["projects"]:
        policy = get_policy(credentials, project["projectId"])
        policy = policy.get("bindings")
        iam_policy_has_been_modified = False

        for role in policy:
            project_members = role["members"]

            if user_iam_policy in project_members:
                project_members.remove(user_iam_policy)
                print(project["projectId"])
                print(policy)
                iam_policy_has_been_modified = True

        if iam_policy_has_been_modified:
            set_policy(credentials, project["projectId"], {"bindings": policy})

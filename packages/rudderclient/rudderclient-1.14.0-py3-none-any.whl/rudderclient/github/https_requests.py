import json
import requests


def get_all_organizations(token):
    """
    List organizations for the authenticated user.

    Parameters:
        token: Personal Access Token of the user with the necessary permissions.
    """
    url = "https://api.github.com/user/orgs"
    token = token

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.request("GET", url, headers=headers, data={})

    return response.json()


def remove_user_from_an_organization(org, username, token):
    """
    Remove an organization member.
    * Remove a user form a organization will remove it from all teams and they will no longer
    have any access to the organization's repositories.

    Parameters:
        org - string
            the organization name to remove from.
        username - string
            the username for the Github user account.
        token - string
            Personal Access Token of the user with the necessary permissions.
    """
    url = f"https://api.github.com/orgs/{org}/members/{username}"
    token = token

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.request("DELETE", url, headers=headers, data={})

    return response.status_code


def get_team_id(org, slug, token):
    """
    Get the team integer id by its slug* .
    * The slug for Github is the name of the team, but replacing special characters, changes all words to lowercase, and
    replaces spaces with a - separator. For example: team name -> "My TEam Näme" slug -> "my-team-name"

    Parameters:
        org - string
            the organization name to remove from.
        slug - string
            the slug for the team name.
        token - string
            Personal Access Token of the user with the necessary permissions.
    """
    url = f"https://api.github.com/orgs/{org}/teams/{slug}"
    token = token

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.request("GET", url, headers=headers, data={})

    # Parse to json the content response to get team id
    content = response.content
    content_string = content.decode("utf-8")
    json_content = json.loads(content_string)

    return json_content["id"]


def invite_users(github_user, org, teams, role, token):
    """
    Invite people to an organization. Also, when the invitation was accepted for the users, they will be a member
    for the teams indicated if any.

    Parameters:
        github_user - string
            email address of the user to invite.
        org - string
            the organization name to remove from.
        teams - array of integers
            the specify IDs for th teams you want to invite the user.
        role - string
            the organization role for the new member.
                * admin - Organization owners with full administrative rights to the organization
                and complete access to all repositories and teams.
                * direct_member - Non-owner organization members with ability to see other members
                and join teams by invitation.
                * billing_manager - Non-owner organization members with ability to manage the billing
                settings of your organization.
        token - string
            Personal Access Token of the user with the necessary permissions.
    """
    url = f"https://api.github.com/orgs/{org}/invitations"
    token = token

    headers = {"Authorization": f"Bearer {token}"}

    data = {"email": github_user, "role": role, "team_ids": teams}

    # Parse data to bytestring
    res_bytes = json.dumps(data).encode("utf-8")

    response = requests.request("POST", url, headers=headers, data=res_bytes)

    return response.status_code

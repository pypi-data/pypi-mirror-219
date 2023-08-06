"""
HTTP requests library.

This library provides an easy way to do HTTP request.

"""


import http.client
import requests

import google.auth.transport.requests
import google.oauth2.id_token


def iap_http_request(
    method: str,
    api_url: str,
    request_url: str,
    body: str,
    headers: dict[str, str],
):
    """
    Makes an http request to an API protected by Identity-Aware Proxy.

    Parameters:
    ----------
        method: Method of the request. "POST", "PATCH", "DELETE", "GET", "PUT".
        api_url: The DNS of the API. For example "api-dev.api.test.cloud"
        request_url: The request url. For example "/api/v1/users"
        body: Body of the requests.
        headers: Necessary headers for the requests. The "Authentication: Bearer {token}" token
        is mandatory. The token value is an OIDC token.
    """
    conn = http.client.HTTPSConnection(api_url)
    conn.request(method=method, url=request_url, body=body, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return data.decode("utf-8")


def make_authorized_post_request(endpoint, audience, body):
    """
    Makes a POST request to another HTTP Cloud Run
    by authenticating with the ID token obtained from the google-auth client library
    using the specified audience value.

    Parameters:
    ----------
        endpoint: The URL (hostname + path) receiving the request. For example: 'https://my-cloud-run-service.run.app/my/awesome/url'
        audience: Your service's hostname. For example: 'https://my-cloud-run-service.run.app/'
        body: The body of the request.
    """

    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)

    headers = {"Authorization": f"Bearer {id_token}"}

    response = requests.request("POST", endpoint, headers=headers, json=body)

    print(response.request)

    return response.status_code

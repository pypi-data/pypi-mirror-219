from http import HTTPStatus
from typing import Any, Dict, Optional, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_api_v1_submissions_bulk_approve_json_body import PostApiV1SubmissionsBulkApproveJsonBody
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: PostApiV1SubmissionsBulkApproveJsonBody,
    authorization: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/submissions/bulk-approve/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    headers["Authorization"] = authorization

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[str]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(str, response.json())
        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: PostApiV1SubmissionsBulkApproveJsonBody,
    authorization: str,
) -> Response[str]:
    """Bulk approve submissions

     Bulk approve study submissions to pay participants after they have
    completed your survey or experiment. You need the list of the participant
    IDs you want to approve and the study id.

    Args:
        authorization (str):
        json_body (PostApiV1SubmissionsBulkApproveJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        authorization=authorization,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: PostApiV1SubmissionsBulkApproveJsonBody,
    authorization: str,
) -> Optional[str]:
    """Bulk approve submissions

     Bulk approve study submissions to pay participants after they have
    completed your survey or experiment. You need the list of the participant
    IDs you want to approve and the study id.

    Args:
        authorization (str):
        json_body (PostApiV1SubmissionsBulkApproveJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: PostApiV1SubmissionsBulkApproveJsonBody,
    authorization: str,
) -> Response[str]:
    """Bulk approve submissions

     Bulk approve study submissions to pay participants after they have
    completed your survey or experiment. You need the list of the participant
    IDs you want to approve and the study id.

    Args:
        authorization (str):
        json_body (PostApiV1SubmissionsBulkApproveJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        authorization=authorization,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: PostApiV1SubmissionsBulkApproveJsonBody,
    authorization: str,
) -> Optional[str]:
    """Bulk approve submissions

     Bulk approve study submissions to pay participants after they have
    completed your survey or experiment. You need the list of the participant
    IDs you want to approve and the study id.

    Args:
        authorization (str):
        json_body (PostApiV1SubmissionsBulkApproveJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            authorization=authorization,
        )
    ).parsed

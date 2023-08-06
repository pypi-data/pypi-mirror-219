from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.study import Study
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: Study,
    authorization: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/studies/{id}/".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    headers["Authorization"] = authorization

    json_json_body = json_body.to_dict()

    return {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Study]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Study.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Study]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: Study,
    authorization: str,
) -> Response[Study]:
    """Update a study

     You can update any field for a draft study.

    Once the study has been published only the following fields can be updated with some restrictions:
    - internal_name: Internal name of the study, not shown to participants
    - total_available_places: Only increasing is allowed. A completed study will become active again and
    resume recruiting of participants. For more information, check the [guide](https://researcher-
    help.prolific.co/hc/en-gb/articles/360009222553)

    Args:
        id (str):
        authorization (str):
        json_body (Study):  Example: {'id': '60d9aadeb86739de712faee0', 'name': "Study about
            API's", 'internal_name': "WIT-2021 Study about API's version 2", 'description': 'This
            study aims to determine how to make a good public API', 'external_study_url':
            'https://eggs-experriment.com?participant={{%PROLIFIC_PID%}}', 'prolific_id_option':
            'url_parameters', 'completion_option': 'url', 'completion_codes': [{'code': 'ABC123',
            'code_type': 'COMPLETED', 'actions': [{'action': 'AUTOMATICALLY_APPROVE'}]}, {'code':
            'DEF234', 'code_type': 'FOLLOW_UP_STUDY', 'actions': [{'action': 'AUTOMATICALLY_APPROVE'},
            {'action': 'ADD_TO_PARTICIPANT_GROUP', 'participant_group':
            '619e049f7648a4e1f8f3645b'}]}], 'total_available_places': 30, 'estimated_completion_time':
            5, 'maximum_allowed_time': 25, 'reward': 100, 'device_compatibility': ['desktop'],
            'peripheral_requirements': [], 'eligibility_requirements': [], 'status': 'UNPUBLISHED'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Study]
    """

    kwargs = _get_kwargs(
        id=id,
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
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: Study,
    authorization: str,
) -> Optional[Study]:
    """Update a study

     You can update any field for a draft study.

    Once the study has been published only the following fields can be updated with some restrictions:
    - internal_name: Internal name of the study, not shown to participants
    - total_available_places: Only increasing is allowed. A completed study will become active again and
    resume recruiting of participants. For more information, check the [guide](https://researcher-
    help.prolific.co/hc/en-gb/articles/360009222553)

    Args:
        id (str):
        authorization (str):
        json_body (Study):  Example: {'id': '60d9aadeb86739de712faee0', 'name': "Study about
            API's", 'internal_name': "WIT-2021 Study about API's version 2", 'description': 'This
            study aims to determine how to make a good public API', 'external_study_url':
            'https://eggs-experriment.com?participant={{%PROLIFIC_PID%}}', 'prolific_id_option':
            'url_parameters', 'completion_option': 'url', 'completion_codes': [{'code': 'ABC123',
            'code_type': 'COMPLETED', 'actions': [{'action': 'AUTOMATICALLY_APPROVE'}]}, {'code':
            'DEF234', 'code_type': 'FOLLOW_UP_STUDY', 'actions': [{'action': 'AUTOMATICALLY_APPROVE'},
            {'action': 'ADD_TO_PARTICIPANT_GROUP', 'participant_group':
            '619e049f7648a4e1f8f3645b'}]}], 'total_available_places': 30, 'estimated_completion_time':
            5, 'maximum_allowed_time': 25, 'reward': 100, 'device_compatibility': ['desktop'],
            'peripheral_requirements': [], 'eligibility_requirements': [], 'status': 'UNPUBLISHED'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Study
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: Study,
    authorization: str,
) -> Response[Study]:
    """Update a study

     You can update any field for a draft study.

    Once the study has been published only the following fields can be updated with some restrictions:
    - internal_name: Internal name of the study, not shown to participants
    - total_available_places: Only increasing is allowed. A completed study will become active again and
    resume recruiting of participants. For more information, check the [guide](https://researcher-
    help.prolific.co/hc/en-gb/articles/360009222553)

    Args:
        id (str):
        authorization (str):
        json_body (Study):  Example: {'id': '60d9aadeb86739de712faee0', 'name': "Study about
            API's", 'internal_name': "WIT-2021 Study about API's version 2", 'description': 'This
            study aims to determine how to make a good public API', 'external_study_url':
            'https://eggs-experriment.com?participant={{%PROLIFIC_PID%}}', 'prolific_id_option':
            'url_parameters', 'completion_option': 'url', 'completion_codes': [{'code': 'ABC123',
            'code_type': 'COMPLETED', 'actions': [{'action': 'AUTOMATICALLY_APPROVE'}]}, {'code':
            'DEF234', 'code_type': 'FOLLOW_UP_STUDY', 'actions': [{'action': 'AUTOMATICALLY_APPROVE'},
            {'action': 'ADD_TO_PARTICIPANT_GROUP', 'participant_group':
            '619e049f7648a4e1f8f3645b'}]}], 'total_available_places': 30, 'estimated_completion_time':
            5, 'maximum_allowed_time': 25, 'reward': 100, 'device_compatibility': ['desktop'],
            'peripheral_requirements': [], 'eligibility_requirements': [], 'status': 'UNPUBLISHED'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Study]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
        authorization=authorization,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    json_body: Study,
    authorization: str,
) -> Optional[Study]:
    """Update a study

     You can update any field for a draft study.

    Once the study has been published only the following fields can be updated with some restrictions:
    - internal_name: Internal name of the study, not shown to participants
    - total_available_places: Only increasing is allowed. A completed study will become active again and
    resume recruiting of participants. For more information, check the [guide](https://researcher-
    help.prolific.co/hc/en-gb/articles/360009222553)

    Args:
        id (str):
        authorization (str):
        json_body (Study):  Example: {'id': '60d9aadeb86739de712faee0', 'name': "Study about
            API's", 'internal_name': "WIT-2021 Study about API's version 2", 'description': 'This
            study aims to determine how to make a good public API', 'external_study_url':
            'https://eggs-experriment.com?participant={{%PROLIFIC_PID%}}', 'prolific_id_option':
            'url_parameters', 'completion_option': 'url', 'completion_codes': [{'code': 'ABC123',
            'code_type': 'COMPLETED', 'actions': [{'action': 'AUTOMATICALLY_APPROVE'}]}, {'code':
            'DEF234', 'code_type': 'FOLLOW_UP_STUDY', 'actions': [{'action': 'AUTOMATICALLY_APPROVE'},
            {'action': 'ADD_TO_PARTICIPANT_GROUP', 'participant_group':
            '619e049f7648a4e1f8f3645b'}]}], 'total_available_places': 30, 'estimated_completion_time':
            5, 'maximum_allowed_time': 25, 'reward': 100, 'device_compatibility': ['desktop'],
            'peripheral_requirements': [], 'eligibility_requirements': [], 'status': 'UNPUBLISHED'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Study
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
            authorization=authorization,
        )
    ).parsed

from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PostApiV1SubmissionsBulkApproveJsonBody")


@attr.s(auto_attribs=True)
class PostApiV1SubmissionsBulkApproveJsonBody:
    """
    Attributes:
        study_id (Union[Unset, str]):
        participant_ids (Union[Unset, List[str]]):
    """

    study_id: Union[Unset, str] = UNSET
    participant_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        study_id = self.study_id
        participant_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.participant_ids, Unset):
            participant_ids = self.participant_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if study_id is not UNSET:
            field_dict["study_id"] = study_id
        if participant_ids is not UNSET:
            field_dict["participant_ids"] = participant_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        study_id = d.pop("study_id", UNSET)

        participant_ids = cast(List[str], d.pop("participant_ids", UNSET))

        post_api_v1_submissions_bulk_approve_json_body = cls(
            study_id=study_id,
            participant_ids=participant_ids,
        )

        post_api_v1_submissions_bulk_approve_json_body.additional_properties = d
        return post_api_v1_submissions_bulk_approve_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.get_api_v1_studies_id_export_response_200_status import GetApiV1StudiesIdExportResponse200Status
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetApiV1StudiesIdExportResponse200")


@attr.s(auto_attribs=True)
class GetApiV1StudiesIdExportResponse200:
    """A status report if the email method is provided.

    Attributes:
        status (Union[Unset, GetApiV1StudiesIdExportResponse200Status]):
    """

    status: Union[Unset, GetApiV1StudiesIdExportResponse200Status] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _status = d.pop("status", UNSET)
        status: Union[Unset, GetApiV1StudiesIdExportResponse200Status]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = GetApiV1StudiesIdExportResponse200Status(_status)

        get_api_v1_studies_id_export_response_200 = cls(
            status=status,
        )

        get_api_v1_studies_id_export_response_200.additional_properties = d
        return get_api_v1_studies_id_export_response_200

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

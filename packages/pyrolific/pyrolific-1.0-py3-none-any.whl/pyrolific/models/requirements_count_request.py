from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.requirement import Requirement


T = TypeVar("T", bound="RequirementsCountRequest")


@attr.s(auto_attribs=True)
class RequirementsCountRequest:
    """
    Attributes:
        eligibility_requirements (Union[Unset, List['Requirement']]): List of all requirements. We recommend re-using
            the response
            from the GET and setting a value. Only requirements with a non null value
            are needed, we will skip the null ones.
    """

    eligibility_requirements: Union[Unset, List["Requirement"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        eligibility_requirements: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.eligibility_requirements, Unset):
            eligibility_requirements = []
            for eligibility_requirements_item_data in self.eligibility_requirements:
                eligibility_requirements_item = eligibility_requirements_item_data.to_dict()

                eligibility_requirements.append(eligibility_requirements_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if eligibility_requirements is not UNSET:
            field_dict["eligibility_requirements"] = eligibility_requirements

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.requirement import Requirement

        d = src_dict.copy()
        eligibility_requirements = []
        _eligibility_requirements = d.pop("eligibility_requirements", UNSET)
        for eligibility_requirements_item_data in _eligibility_requirements or []:
            eligibility_requirements_item = Requirement.from_dict(eligibility_requirements_item_data)

            eligibility_requirements.append(eligibility_requirements_item)

        requirements_count_request = cls(
            eligibility_requirements=eligibility_requirements,
        )

        requirements_count_request.additional_properties = d
        return requirements_count_request

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

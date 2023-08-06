from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="PostApiV1ParticipantGroupsJsonBody")


@attr.s(auto_attribs=True)
class PostApiV1ParticipantGroupsJsonBody:
    """
    Attributes:
        project_id (str): The id of the project to create the participant group in Example: 5e9b9c9b0f9c9a0001b0b1f4.
        name (str): The name of the participant group Example: Group 1.
    """

    project_id: str
    name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        project_id = self.project_id
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_id = d.pop("project_id")

        name = d.pop("name")

        post_api_v1_participant_groups_json_body = cls(
            project_id=project_id,
            name=name,
        )

        post_api_v1_participant_groups_json_body.additional_properties = d
        return post_api_v1_participant_groups_json_body

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

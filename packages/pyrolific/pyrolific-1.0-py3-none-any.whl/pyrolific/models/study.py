from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..models.create_study_completion_option import CreateStudyCompletionOption
from ..models.create_study_device_compatibility_item import CreateStudyDeviceCompatibilityItem
from ..models.create_study_peripheral_requirements_item import CreateStudyPeripheralRequirementsItem
from ..models.create_study_prolific_id_option import CreateStudyProlificIdOption
from ..models.study_status import StudyStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_study_completion_codes_item import CreateStudyCompletionCodesItem
    from ..models.create_study_submissions_config import CreateStudySubmissionsConfig
    from ..models.requirement import Requirement


T = TypeVar("T", bound="Study")


@attr.s(auto_attribs=True)
class Study:
    r"""
    Example:
        {'id': '60d9aadeb86739de712faee0', 'name': "Study about API's", 'internal_name': "WIT-2021 Study about API's
            version 2", 'description': 'This study aims to determine how to make a good public API', 'external_study_url':
            'https://eggs-experriment.com?participant={{%PROLIFIC_PID%}}', 'prolific_id_option': 'url_parameters',
            'completion_option': 'url', 'completion_codes': [{'code': 'ABC123', 'code_type': 'COMPLETED', 'actions':
            [{'action': 'AUTOMATICALLY_APPROVE'}]}, {'code': 'DEF234', 'code_type': 'FOLLOW_UP_STUDY', 'actions':
            [{'action': 'AUTOMATICALLY_APPROVE'}, {'action': 'ADD_TO_PARTICIPANT_GROUP', 'participant_group':
            '619e049f7648a4e1f8f3645b'}]}], 'total_available_places': 30, 'estimated_completion_time': 5,
            'maximum_allowed_time': 25, 'reward': 100, 'device_compatibility': ['desktop'], 'peripheral_requirements': [],
            'eligibility_requirements': [], 'status': 'UNPUBLISHED'}

    Attributes:
        name (str): Public name or title of the study
        description (str): Description of the study for the participants to read before
            starting the study
        external_study_url (str): URL of the survey or experiment you want participant to access. You can pass URL
            search parameters to your survey or experiment

            * Participant id {{%PROLIFIC_PID%}}
            * Study id {{%STUDY_ID%}}
            * Session id {{%SESSION_ID%}}

            For example `https://eggs-experriment.com?participant={{%PROLIFIC_PID%}}`
        prolific_id_option (CreateStudyProlificIdOption): Use 'question' if you will add a question in your survey or
            experiment asking the participant ID

            **Recommended** Use 'url_parameters' if your survey or experiment can retrieve and store those parameters for
            your analysis.

            Use 'not_required' if you don't need to record them
        completion_option (CreateStudyCompletionOption): Use 'url' if you will redirect the user back to prolific using
            a url,
            the url you will use in your experiment
            or survey to go back is https://app.prolific.co/submissions/complete?cc={code}

            Use 'code' when the participants will manually input the code, at the
            end of the experiment you will tell the participants the code. Note that
            the {code} you have to give is one of the completion codes you define below in the `completion_codes` argument.
        completion_codes (List['CreateStudyCompletionCodesItem']): Specify at least one completion code for your study.
            A participant will enter one of these codes when they complete your study.

            Each code must be unique within a study.

            You can specify as many actions as you like per code.
        total_available_places (float): How many participants are you looking to recruit
        estimated_completion_time (float): Estimated duration in minutes of the experiment or survey
        reward (float): How much are you going to pay the participants in cents. We
            use the currency of your account.
        id (str): Study id. It is created by Prolific. **Read only**.
        status (StudyStatus): Status of the study. **Read only**.

            To change the status you can use `/api/v1/studies/{id}/transition/`
        internal_name (Union[Unset, None, str]): Internal name of the study, not shown to participants
        maximum_allowed_time (Union[Unset, float]): Max time in minutes for a participant to finish the submission.
            Submissions are timed out if it takes longer.

            If it is not provided the default value is set to the max value.

            The min value is calculated as two minutes plus two times the estimated time plus two times the square root of
            the estimated time
        device_compatibility (Union[Unset, List[CreateStudyDeviceCompatibilityItem]]): Add all devices that participants
            can use.
            You can include one or more options.

            An empty array indicates that all options are available.
        peripheral_requirements (Union[Unset, List[CreateStudyPeripheralRequirementsItem]]): Add all requirements that
            participants have to meet.

            An empty array indicates that there are no extra peripheral requirements.
        eligibility_requirements (Optional[List['Requirement']]): Array of requirements.

            Use empty array for "Everyone"
        naivety_distribution_rate (Union[Unset, None, float]): Control the balance between speed of your studies and the
            naivety of the participants.

            If not defined, by default Prolific calculates the best rate for most studies
            taking into account the `eligibility_requirements` and the `total_available_places` needed for this study.

            Use 0 if your priority is speed. When this property is set to 0 all eligible participants will have access
            to your study at the same time, without any prioritization.

            You can also set this at a workspace and project level.
        project (Union[Unset, str]): Project id, this is optional and if not supplied with be the put in the default
            workspace and project.
        submissions_config (Union[Unset, CreateStudySubmissionsConfig]): **BETA**: This is a beta feature and is
            currently only available to selected workspaces.
            It is being tested and evaluated for effectiveness and user experience before being released to all users.

            **Advanced**: This helps with faster data collection. Your survey system will need to handle providing a
            unique experience each time the participant takes the study.

            Configuration related to study submissions. The purpose of this field is to capture any configuration options
            that impact the submissions made by participants in a study.
        metadata (Union[Unset, None, str]): This field can be used to store extra information required for a system
            integration.
            For example, it could be some JSON, XML, an integer, or a string.

            Examples could include:

              - `123345` - An ID from your system, that helps with linkage when returning the study.
              - `{ \"id\": \"45\", \"type\": \"finance\"}` - Some JSON that you want to store.
    """

    name: str
    description: str
    external_study_url: str
    prolific_id_option: CreateStudyProlificIdOption
    completion_option: CreateStudyCompletionOption
    completion_codes: List["CreateStudyCompletionCodesItem"]
    total_available_places: float
    estimated_completion_time: float
    reward: float
    id: str
    status: StudyStatus
    eligibility_requirements: Optional[List["Requirement"]]
    internal_name: Union[Unset, None, str] = UNSET
    maximum_allowed_time: Union[Unset, float] = UNSET
    device_compatibility: Union[Unset, List[CreateStudyDeviceCompatibilityItem]] = UNSET
    peripheral_requirements: Union[Unset, List[CreateStudyPeripheralRequirementsItem]] = UNSET
    naivety_distribution_rate: Union[Unset, None, float] = UNSET
    project: Union[Unset, str] = UNSET
    submissions_config: Union[Unset, "CreateStudySubmissionsConfig"] = UNSET
    metadata: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        external_study_url = self.external_study_url
        prolific_id_option = self.prolific_id_option.value

        completion_option = self.completion_option.value

        completion_codes = []
        for completion_codes_item_data in self.completion_codes:
            completion_codes_item = completion_codes_item_data.to_dict()

            completion_codes.append(completion_codes_item)

        total_available_places = self.total_available_places
        estimated_completion_time = self.estimated_completion_time
        reward = self.reward
        id = self.id
        status = self.status.value

        internal_name = self.internal_name
        maximum_allowed_time = self.maximum_allowed_time
        device_compatibility: Union[Unset, List[str]] = UNSET
        if not isinstance(self.device_compatibility, Unset):
            device_compatibility = []
            for device_compatibility_item_data in self.device_compatibility:
                device_compatibility_item = device_compatibility_item_data.value

                device_compatibility.append(device_compatibility_item)

        peripheral_requirements: Union[Unset, List[str]] = UNSET
        if not isinstance(self.peripheral_requirements, Unset):
            peripheral_requirements = []
            for peripheral_requirements_item_data in self.peripheral_requirements:
                peripheral_requirements_item = peripheral_requirements_item_data.value

                peripheral_requirements.append(peripheral_requirements_item)

        if self.eligibility_requirements is None:
            eligibility_requirements = None
        else:
            eligibility_requirements = []
            for eligibility_requirements_item_data in self.eligibility_requirements:
                eligibility_requirements_item = eligibility_requirements_item_data.to_dict()

                eligibility_requirements.append(eligibility_requirements_item)

        naivety_distribution_rate = self.naivety_distribution_rate
        project = self.project
        submissions_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.submissions_config, Unset):
            submissions_config = self.submissions_config.to_dict()

        metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "external_study_url": external_study_url,
                "prolific_id_option": prolific_id_option,
                "completion_option": completion_option,
                "completion_codes": completion_codes,
                "total_available_places": total_available_places,
                "estimated_completion_time": estimated_completion_time,
                "reward": reward,
                "id": id,
                "status": status,
                "eligibility_requirements": eligibility_requirements,
            }
        )
        if internal_name is not UNSET:
            field_dict["internal_name"] = internal_name
        if maximum_allowed_time is not UNSET:
            field_dict["maximum_allowed_time"] = maximum_allowed_time
        if device_compatibility is not UNSET:
            field_dict["device_compatibility"] = device_compatibility
        if peripheral_requirements is not UNSET:
            field_dict["peripheral_requirements"] = peripheral_requirements
        if naivety_distribution_rate is not UNSET:
            field_dict["naivety_distribution_rate"] = naivety_distribution_rate
        if project is not UNSET:
            field_dict["project"] = project
        if submissions_config is not UNSET:
            field_dict["submissions_config"] = submissions_config
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_study_completion_codes_item import CreateStudyCompletionCodesItem
        from ..models.create_study_submissions_config import CreateStudySubmissionsConfig
        from ..models.requirement import Requirement

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        external_study_url = d.pop("external_study_url")

        prolific_id_option = CreateStudyProlificIdOption(d.pop("prolific_id_option"))

        completion_option = CreateStudyCompletionOption(d.pop("completion_option"))

        completion_codes = []
        _completion_codes = d.pop("completion_codes")
        for completion_codes_item_data in _completion_codes:
            completion_codes_item = CreateStudyCompletionCodesItem.from_dict(completion_codes_item_data)

            completion_codes.append(completion_codes_item)

        total_available_places = d.pop("total_available_places")

        estimated_completion_time = d.pop("estimated_completion_time")

        reward = d.pop("reward")

        id = d.pop("id")

        status = StudyStatus(d.pop("status"))

        internal_name = d.pop("internal_name", UNSET)

        maximum_allowed_time = d.pop("maximum_allowed_time", UNSET)

        device_compatibility = []
        _device_compatibility = d.pop("device_compatibility", UNSET)
        for device_compatibility_item_data in _device_compatibility or []:
            device_compatibility_item = CreateStudyDeviceCompatibilityItem(device_compatibility_item_data)

            device_compatibility.append(device_compatibility_item)

        peripheral_requirements = []
        _peripheral_requirements = d.pop("peripheral_requirements", UNSET)
        for peripheral_requirements_item_data in _peripheral_requirements or []:
            peripheral_requirements_item = CreateStudyPeripheralRequirementsItem(peripheral_requirements_item_data)

            peripheral_requirements.append(peripheral_requirements_item)

        eligibility_requirements = []
        _eligibility_requirements = d.pop("eligibility_requirements")
        for eligibility_requirements_item_data in _eligibility_requirements or []:
            eligibility_requirements_item = Requirement.from_dict(eligibility_requirements_item_data)

            eligibility_requirements.append(eligibility_requirements_item)

        naivety_distribution_rate = d.pop("naivety_distribution_rate", UNSET)

        project = d.pop("project", UNSET)

        _submissions_config = d.pop("submissions_config", UNSET)
        submissions_config: Union[Unset, CreateStudySubmissionsConfig]
        if isinstance(_submissions_config, Unset):
            submissions_config = UNSET
        else:
            submissions_config = CreateStudySubmissionsConfig.from_dict(_submissions_config)

        metadata = d.pop("metadata", UNSET)

        study = cls(
            name=name,
            description=description,
            external_study_url=external_study_url,
            prolific_id_option=prolific_id_option,
            completion_option=completion_option,
            completion_codes=completion_codes,
            total_available_places=total_available_places,
            estimated_completion_time=estimated_completion_time,
            reward=reward,
            id=id,
            status=status,
            internal_name=internal_name,
            maximum_allowed_time=maximum_allowed_time,
            device_compatibility=device_compatibility,
            peripheral_requirements=peripheral_requirements,
            eligibility_requirements=eligibility_requirements,
            naivety_distribution_rate=naivety_distribution_rate,
            project=project,
            submissions_config=submissions_config,
            metadata=metadata,
        )

        study.additional_properties = d
        return study

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

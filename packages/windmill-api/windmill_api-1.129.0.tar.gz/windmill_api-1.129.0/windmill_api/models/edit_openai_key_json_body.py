from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditOpenaiKeyJsonBody")


@attr.s(auto_attribs=True)
class EditOpenaiKeyJsonBody:
    """
    Attributes:
        openai_key (Union[Unset, str]):
    """

    openai_key: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        openai_key = self.openai_key

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if openai_key is not UNSET:
            field_dict["openai_key"] = openai_key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        openai_key = d.pop("openai_key", UNSET)

        edit_openai_key_json_body = cls(
            openai_key=openai_key,
        )

        edit_openai_key_json_body.additional_properties = d
        return edit_openai_key_json_body

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

from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.framework import Framework
from ..models.python_version import PythonVersion
from ..types import UNSET, Unset

T = TypeVar("T", bound="Conversion")


@attr.s(auto_attribs=True)
class Conversion:
    """ 
        Attributes:
            framework (Framework):
            requirements (List[str]):
            python_version (Union[Unset, PythonVersion]):
     """

    framework: Framework
    requirements: List[str]
    python_version: Union[Unset, PythonVersion] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        framework = self.framework.value

        requirements = self.requirements




        python_version: Union[Unset, str] = UNSET
        if not isinstance(self.python_version, Unset):
            python_version = self.python_version.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "framework": framework,
            "requirements": requirements,
        })
        if python_version is not UNSET:
            field_dict["python_version"] = python_version

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        framework = Framework(d.pop("framework"))




        requirements = cast(List[str], d.pop("requirements"))


        _python_version = d.pop("python_version", UNSET)
        python_version: Union[Unset, PythonVersion]
        if isinstance(_python_version,  Unset):
            python_version = UNSET
        else:
            python_version = PythonVersion(_python_version)




        conversion = cls(
            framework=framework,
            requirements=requirements,
            python_version=python_version,
        )

        conversion.additional_properties = d
        return conversion

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

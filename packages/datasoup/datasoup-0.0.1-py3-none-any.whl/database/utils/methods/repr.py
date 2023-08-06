from typing import Dict, Any

from sqlalchemy.orm.exc import DetachedInstanceError


def repr_factory(self, **fields: Dict[str, Any]) -> str:
    field_strings = []
    at_least_one_attached_attribute = False
    for key, field in fields.items():
        try:
            field_strings.append(f'{key}={field!r}')
        except DetachedInstanceError:
            field_strings.append(f'{key}=DetachedInstanceError')
        else:
            at_least_one_attached_attribute = True
    if at_least_one_attached_attribute:
        return f"{self.__class__.__name__}({', '.join(field_strings)})"
    return f"{self.__class__.__name__} {id(self)}"
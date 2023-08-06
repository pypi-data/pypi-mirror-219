from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class Workspace(BaseModel):
    admin_ids: list[str] | None
    color: str
    created: datetime
    domain: str
    id: str
    master_id: str
    name: str
    photo: str

    def dict(self, *, include: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None,
             exclude: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None, by_alias: bool = False,
             skip_defaults: Optional[bool] = None, exclude_unset: bool = False, exclude_defaults: bool = False,
             exclude_none: bool = False) -> 'DictStrAny':
        data = super().dict(include=include, exclude=exclude, by_alias=by_alias, skip_defaults=skip_defaults,
                            exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none)
        if 'created' in data:
            data['created'] = data['created'].isoformat()
        return data

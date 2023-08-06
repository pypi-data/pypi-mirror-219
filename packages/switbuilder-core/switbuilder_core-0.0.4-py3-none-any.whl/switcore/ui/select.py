from pydantic import BaseModel


class Option(BaseModel):
    label: str
    action_id: str


class Style(BaseModel):
    variant: str | None


class Select(BaseModel):
    type: str = 'select'
    placeholder: str | None
    trigger_on_input: bool
    value: list[str] | None
    options: list[Option] = []
    style: Style | None = None

from pydantic import BaseModel

from switcore.ui.static_action import StaticAction


class TextStyle(BaseModel):
    bold: bool = False
    color: str
    size: str
    max_lines: int


class Background(BaseModel):
    color: str


class MetadataItem(BaseModel):
    type: str
    content: str | None
    style: dict | None
    image_url: str | None


class StartSection(BaseModel):
    type: str
    image_url: str
    alt: str
    style: dict


class TextContent(BaseModel):
    type: str = "text"
    content: str
    style: TextStyle | None


class TextSection(BaseModel):
    text: TextContent
    metadata_items: list[MetadataItem] | None


class CollectionEntry(BaseModel):
    type: str = "collection_entry"
    text_sections: list[TextSection]
    start_section: StartSection | None
    vertical_alignment: str
    background: Background
    action_id: str | None
    static_action: StaticAction | None
    draggable: bool = False

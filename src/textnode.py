from enum import Enum
from typing import Optional

class TextType(Enum):
    """
    Defines the supported types of inline markdown elements.
    Using an Enum prevents 'magic strings' and provides autocomplete/type safety.
    """
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    """
    An intermediate representation of inline text elements.
    """
    def __init__(
        self,
        text: str,
        text_type: TextType,
        url: Optional[str] = None
    ) -> None:
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: Optional[str] = url

    def __eq__(self, other: object) -> bool:
        """
        Determines if two TextNodes are data-equivalent.
        """
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self) -> str:
        """
        Provides a developer-friendly string representation of the object.
        """
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

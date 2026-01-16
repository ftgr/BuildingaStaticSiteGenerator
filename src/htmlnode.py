from __future__ import annotations

from typing import Dict, List, Optional


class HTMLNode:
    """
    Represents a node in the HTML DOM tree.
    """

    def __init__(
            self,
            tag: Optional[str] = None,
            value: Optional[str] = None,
            children: Optional[List[HTMLNode]] = None,
            props: Optional[Dict[str, str]] = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        """
        Child classes will override this to render HTML.
        """
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        """
        Converts the props dictionary into an HTML attribute string.
        Example: {'href': 'https://google.com'} -> ' href="https://google.com"'
        """
        if self.props is None:
            return ""

        # Functional Pragmatism:
        # We create a generator yielding formatted strings, then join them.
        # This avoids the "trailing space" issue and is memory efficient.
        attributes = []
        for key, value in self.props.items():
            attributes.append(f' {key}="{value}"')

        return "".join(attributes)

    def __repr__(self) -> str:
        """
        Helpful string representation for debugging.
        """
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    """
    Represents a leaf in the HTML tree (a node with no children).
    Example: <p>I am a paragraph</p>
    """

    def __init__(
            self,
            tag: Optional[str],
            value: str,
            props: Optional[Dict[str, str]] = None
    ) -> None:
        # Architectural Decision:
        # We enforce strict positional arguments for tag and value here,
        # but we pass children=None to the parent to ensure this node
        # is physically incapable of holding a list of children in our model.
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        """
        Renders the node as an HTML string.
        Raises ValueError if value is None.
        """
        if self.value is None:
            raise ValueError("Invalid HTML: LeafNode must have a value")

        # Case 1: Raw text (no tag)
        if self.tag is None:
            return self.value

        # Case 2: Render HTML tag
        # Functional Pragmatism: We reuse the parent's props_to_html logic
        # to ensure attribute formatting is consistent across the entire app.
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    """
    Represents a branch in the HTML tree.
    It contains other nodes but no direct value.
    """

    def __init__(
            self,
            tag: str,
            children: List[HTMLNode],
            props: Optional[Dict[str, str]] = None
    ) -> None:
        # Architectural Decision:
        # ParentNodes cannot have a value (text). They only hold other nodes.
        # We pass None for the value argument to the superclass.
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        """
        Recursively renders the HTML for this node and all its children.
        """
        if self.tag is None:
            raise ValueError("Invalid HTML: ParentNode must have a tag")
        if self.children is None:
            raise ValueError("Invalid HTML: ParentNode must have children")

        # Functional Pragmatism:
        # We use a generator expression inside join() to recursively call to_html().
        # This is more memory efficient than building a large string with += in a loop.
        children_html = "".join(child.to_html() for child in self.children)

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {len(self.children)}, {self.props})"
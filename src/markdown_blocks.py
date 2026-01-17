from enum import Enum
from typing import List

from htmlnode import ParentNode, HTMLNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found")

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> List[str]:
    """
    Splits a raw markdown string into a list of block strings.
    """
    # Step 1: Split by double newline to identify potential blocks
    blocks = markdown.split("\n\n")
    filtered_blocks = []

    for block in blocks:
        # Step 2: Strip leading/trailing whitespace
        # This removes indentation artifacts or extra newlines
        if block == "":
            continue

        block = block.strip()

        # Step 3: Filter out empty blocks
        # This handles cases where the user put 3+ newlines between paragraphs
        if block != "":
            filtered_blocks.append(block)

    return filtered_blocks

def block_to_block_type(block: str) -> BlockType:
    """
    Determines the Markdown BlockType of a given text block.
    """
    lines = block.split("\n")

    # 1. Headings (starts with #)
    # Architectural decision: We check for 1-6 # followed by a space.
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # 2. Code blocks (starts/ends with ```)
    # We check len > 6 to ensure it's not just "``````"
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    # 3. Quote blocks (all lines start with >)
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    # 4. Unordered List (all lines start with - )
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    # 5. Ordered List (1. 2. 3. ...)
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    # 6. Fallback
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    Converts a full markdown document into a single HTML <div> node
    containing all the block elements as children.
    """
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        # Dispatch Pattern: Delegate based on type
        if block_type == BlockType.PARAGRAPH:
            children.append(block_to_paragraph(block))
        elif block_type == BlockType.HEADING:
            children.append(block_to_heading(block))
        elif block_type == BlockType.CODE:
            children.append(block_to_code(block))
        elif block_type == BlockType.QUOTE:
            children.append(block_to_quote(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(block_to_ul(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(block_to_ol(block))
        else:
            raise ValueError("Invalid block type")

    return ParentNode("div", children, None)


def text_to_children(text: str) -> List[HTMLNode]:
    """
    Shared helper: converts a string of text into a list of HTMLNodes
    by parsing inline markdown (bold, italic, etc).
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def block_to_paragraph(block: str) -> HTMLNode:
    # Paragraphs just need their newlines replaced by spaces
    # to render nicely in HTML
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def block_to_heading(block: str) -> HTMLNode:
    # Determine level by counting #
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break

    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")

    text = block[level + 1:]  # Strip the '# ' prefix
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def block_to_code(block: str) -> HTMLNode:
    # Strip the ``` lines.
    # Architectural decision: We assume the block is already validated
    # to start and end with ``` by block_to_block_type
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")

    text = block[4:-3]  # Remove ```\n and ```

    # Code blocks do NOT parse inline markdown. They are raw text.
    children = text_to_children(text)

    # Structure: <pre><code>...</code></pre>
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def block_to_quote(block: str) -> HTMLNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        # Strip the "> " prefix
        new_lines.append(line.lstrip(">").strip())

    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def block_to_ul(block: str) -> HTMLNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]  # Strip "- "
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def block_to_ol(block: str) -> HTMLNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        # Strip "1. " (finding the first space is safer than fixed slicing)
        text = item[item.find(" ") + 1:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)
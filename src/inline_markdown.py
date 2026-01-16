import re
from typing import List, Tuple

from textnode import TextNode, TextType


def split_nodes_delimiter(
        old_nodes: List[TextNode],
        delimiter: str,
        text_type: TextType
) -> List[TextNode]:
    """
    Splits a list of TextNodes based on a markdown delimiter.
    Only strictly splits TEXT_TYPE nodes.
    """
    new_nodes = []

    for node in old_nodes:
        # 1. Logic Gate: Non-text nodes are already processed/atomic.
        # We append them as references and move on.
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # 2. The Split Operation
        split_nodes = []
        sections = node.text.split(delimiter)

        # 3. Markdown Validation
        # If segments are even, it means we have an odd number of delimiters
        # (e.g. "bold ** text" -> 2 segments).
        if len(sections) % 2 == 0:
            raise Exception(f"Invalid markdown, formatted section not closed: {node.text}")

        # 4. Reassembly
        for i in range(len(sections)):
            if sections[i] == "":
                continue

            if i % 2 == 0:
                # Even indices are the content OUTSIDE the delimiter (Original Text)
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                # Odd indices are the content INSIDE the delimiter (New Type)
                split_nodes.append(TextNode(sections[i], text_type))

        # Functional Pragmatism: extend modifies the list in-place,
        # avoiding nested lists.
        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    """
    Extracts markdown images returning a list of tuples (alt_text, url).
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """
    Extracts markdown links returning a list of tuples (anchor_text, url).
    Ignores images (which start with !).
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        # Optimization: If it's not text, we can't extract images from it.
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)

        # Base Case: If no images found, keep the node as is
        if len(images) == 0:
            new_nodes.append(node)
            continue

        for image_alt, image_link in images:
            # Construct the markdown pattern to split by
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)

            # Logic Gate: Ensure strict splitting
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")

            # Part 1: Text before the image
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            # Part 2: The Image itself
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            # Update the remaining text to be processed in the next iteration
            original_text = sections[1]

        # Part 3: Remaining text after the last image
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        for link_text, link_url in links:
            sections = original_text.split(f"[{link_text}]({link_url})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text: str) -> List[TextNode]:
    """
    Parses a raw string into a list of TextNodes by sequentially applying
    all splitting strategies (Images, Links, Code, Bold, Italic).
    """
    # Step 1: Start with a single text node
    nodes = [TextNode(text, TextType.TEXT)]

    # Step 2: Extract "Block-like" inline elements (Images and Links)
    # We do images first because they start with '!', so we don't want
    # the link splitter to accidentally catch an image as a link.
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    # Step 3: Extract "Delimiter-based" elements
    # We do code first, because code blocks might contain asterisks or underscores
    # that we don't want to parse as bold/italic.
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Step 4: Extract styling
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)  # Support underscores too

    return nodes
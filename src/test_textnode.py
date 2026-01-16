import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        """Test that two nodes with identical content are equal."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_type(self) -> None:
        """Test that nodes with different TextTypes are not equal."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self) -> None:
        """Test that nodes with different text content are not equal."""
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self) -> None:
        """Test that two nodes with the same URL are equal."""
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self) -> None:
        """Test that the string representation matches the expected format."""
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        expected = "TextNode(This is a text node, text, https://www.boot.dev)"
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
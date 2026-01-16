from textnode import TextNode, TextType

def main() -> None:
    # Create a dummy node to verify our implementation
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()

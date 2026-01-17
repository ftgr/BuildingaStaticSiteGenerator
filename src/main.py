import os
import shutil

from generate_page import generate_pages_recursive


def copy_files_recursive(source_dir_path: str, dest_dir_path: str) -> None:
    """
    Recursively copies the contents of the source directory to the destination directory.
    """
    # 1. Validation: Fail if source doesn't exist
    if not os.path.exists(source_dir_path):
        raise Exception(f"Source directory does not exist: {source_dir_path}")

    # 2. Preparation: Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    # 3. Traversal: List all items in the current source directory
    for filename in os.listdir(source_dir_path):
        # Construct full paths
        from_path = os.path.join(source_dir_path, filename)
        to_path = os.path.join(dest_dir_path, filename)

        # 4. Logic Gate: File vs Directory
        print(f"Processing: {from_path} -> {to_path}")

        if os.path.isfile(from_path):
            # Base Case: It's a file, just copy it
            shutil.copy(from_path, to_path)
        else:
            # Recursive Step: It's a directory, dive deeper!
            copy_files_recursive(from_path, to_path)


def main() -> None:
    # Define our source and destination
    # Senior Engineer Tip: Use absolute paths or reliable relative paths
    source = "static"
    destination = "public"
    content_source = "content"
    template_path = "template.html"

    print("Deleting public directory...")
    # Step 1: Clean Slate. Remove the entire directory tree if it exists.
    if os.path.exists(destination):
        shutil.rmtree(destination)

    print("Copying static files to public directory...")
    copy_files_recursive(source, destination)

    # NEW: Generate the page
    # generate_page("content/index.md", "template.html", "public/index.html")
    # print("Generating content...")
    # This one call handles the entire site now
    generate_pages_recursive(content_source, template_path, destination)

    print("Done!")

    # Create a dummy node to verify our implementation
    # node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(node)


if __name__ == "__main__":
    main()

import os

from markdown_blocks import markdown_to_html_node, extract_title


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath: str):
    """
    Crawls the content directory and generates HTML pages for every Markdown file found.
    Preserves the directory structure in the destination.
    """
    for entry in os.listdir(dir_path_content):
        # Construct full paths
        from_path = os.path.join(dir_path_content, entry)
        to_path = os.path.join(dest_dir_path, entry)

        # Logic Gate: File vs Directory
        if os.path.isfile(from_path):
            # We only care about markdown files
            if from_path.endswith(".md"):
                # Calculate the destination HTML path
                # e.g., content/blog/index.md -> public/blog/index.html
                dest_html_path = to_path.replace(".md", ".html")

                # Generate the page using our existing logic (refactored or called directly)
                #generate_page(from_path, template_path, dest_html_path)
                generate_page(from_path, template_path, dest_html_path, basepath)
        else:
            # Recursion Step: It's a directory
            # Ensure the destination directory exists
            os.makedirs(to_path, exist_ok=True)
            #generate_pages_recursive(from_path, template_path, to_path)
            generate_pages_recursive(from_path, template_path, to_path, basepath)


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # 1. Read the Markdown file
    with open(from_path, "r") as f:
        markdown_content = f.read()

    # 2. Read the Template file
    with open(template_path, "r") as f:
        template_content = f.read()

    # 3. Convert Markdown to HTML
    node = markdown_to_html_node(markdown_content)
    html_content = node.to_html()

    # 4. Extract the Title
    title = extract_title(markdown_content)

    # 5. Replace Placeholders
    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    # Logic to fix links for GitHub Pages deployment
    # We replace absolute paths like href="/..." with href="{basepath}..."
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    # 6. Ensure the destination directory exists
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    # 7. Write the final HTML file
    with open(dest_path, "w") as f:
        f.write(full_html)
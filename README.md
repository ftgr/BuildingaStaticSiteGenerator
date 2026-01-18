# 🐍 Python Static Site Generator

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-functional-success)

A robust, lightweight, and custom-built Static Site Generator (SSG) written entirely in Python. This project converts a directory of Markdown files into a fully functional, navigable static HTML website.

It was built from scratch to understand the fundamentals of parsing, recursion, and tree data structures, without relying on external libraries like Hugo or Jekyll.

## ✨ Features

* **Markdown Parsing**: Full support for standard Markdown syntax including:
    * Headings (H1-H6)
    * Paragraphs & Blockquotes
    * Unordered & Ordered Lists
    * Code Blocks (with raw text preservation)
    * **Bold**, *Italic*, `Inline Code`
    * Links & Images
* **Recursive Generation**: Crawls nested directories in `content/` to mirror the structure in the generated site (e.g., handles `/blog/posts/`).
* **Static Asset Management**: Automatically copies images and CSS from `static/` to the build folder.
* **Templating**: Injects generated HTML into a customizable `template.html`.
* **GitHub Pages Ready**: Supports configurable base paths for hosting on subdirectories (like GitHub Pages).
* **Zero Dependencies**: Built using only the Python Standard Library (`os`, `shutil`, `unittest`, `re`, `html`, `sys`).

## 📂 Project Structure

```text
.
├── content/             # Your raw Markdown files (The source of truth)
├── static/              # Static assets (CSS, Images)
├── src/                 # Source code
│   ├── main.py          # Entry point
│   ├── htmlnode.py      # HTML Node data structures
│   ├── textnode.py      # Intermediate Text representation
│   ├── markdown_blocks.py # Block-level parsing logic
│   ├── inline_markdown.py # Inline-level parsing logic
│   └── generate_page.py # File I/O and orchestration
├── docs/                # The generated site (Production build)
├── public/              # (Optional) Local development build location
├── template.html        # The HTML skeleton for all pages
├── main.sh              # Script for local development (Build + Serve)
├── build.sh             # Script for production build
└── test.sh              # Runs the unit test suite

```

## 🚀 Getting Started

### Prerequisites

* Python 3.x installed on your machine.

### Installation

1. Clone the repository:
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
```


2. Make the scripts executable (Linux/Mac):
```bash
chmod +x main.sh build.sh test.sh
```



## 💻 Usage

### 1. Local Development

To build the site and spin up a local server to view it:

```bash
./main.sh
```

This script will:

1. Clean the `public/` directory.
2. Generate the site from `content/`.
3. Serve the site at `http://localhost:8888`.

### 2. Adding Content

To add a new page:

1. Create a folder or file in `content/`.
2. Add a `.md` file.
3. Ensure the file has a single H1 (`# Title`) at the top (used for the page title).

**Example:**
Create `content/about.md`:

```markdown
# About Me

I am a developer building cool things.
```

### 3. Production Build (GitHub Pages)

GitHub Pages often serves sites from a subdirectory (e.g., `username.github.io/repo-name/`). To build for production:

1. Open `build.sh`.
2. Ensure the argument passed to `main.py` matches your repository name (surrounded by slashes).
```bash
# Example for [https://github.com/jdoe/my-blog](https://github.com/jdoe/my-blog)
python3 src/main.py "/my-blog/"
```


3. Run the build script:
```bash
./build.sh
```


4. Commit and push the changes (ensure the `docs/` folder is committed).

## ⚙️ Configuration

### Deployment Settings

This project is configured to deploy to **GitHub Pages** using the `/docs` folder method.

1. Go to your GitHub Repository Settings.
2. Navigate to **Pages**.
3. Under **Build and deployment**, select:
* Source: **Deploy from a branch**
* Branch: **main** (or master)
* Folder: **/docs**


4. Save. Your site will be live at the provided URL shortly.

## 🧪 Testing

The project utilizes Python's built-in `unittest` framework. The test suite covers data node integrity, regex pattern matching, and block parsing logic.

To run all tests:

```bash
./test.sh
```

## 🧠 Architecture Overview

The generator follows a **Pipeline Pattern**:

1. **Raw Markdown** is read from files.
2. **Block Splitting**: The text is split into "Blocks" (Paragraphs, Headings, Lists).
3. **Text Tokenization**: Text inside blocks is parsed into `TextNodes` (identifying bold, links, etc.).
4. **HTML Conversion**: `TextNodes` are converted to `LeafNodes`, and Blocks are converted to `ParentNodes` (HTML structure).
5. **Tree Assembly**: The nodes are assembled into a complete HTML tree.
6. **Injection**: The HTML tree is rendered to a string and injected into `template.html`.

## 📝 License

This project is open source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

---

*Built with ❤️ (and recursion) during the Boot.dev backend curriculum.*
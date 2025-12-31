import os
from pathlib import Path

from markdown_blocks import extract_title, markdown_to_html_node


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    dir_path = os.path.dirname(dest_path)
    if dir_path != "":
        os.makedirs(dir_path, exist_ok=True)
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_string)
    page = page.replace('href="/', f'href="{base_path}')
    page = page.replace('src="/', f'src="{base_path}')

    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(content_dir, template_path, dest_dir, base_path):
    content_dir = Path(content_dir)
    dest_dir = Path(dest_dir)
    for path in content_dir.iterdir():
        dest_path = dest_dir / path.name
        if path.is_dir():
            generate_pages_recursive(path, template_path, dest_path, base_path)
        elif path.is_file() and path.suffix == ".md":
            dest_htmlpath = dest_dir / (path.stem + ".html")
            generate_page(path, template_path, dest_htmlpath, base_path)

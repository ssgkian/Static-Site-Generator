import os
import shutil
import sys

from copystatic import copy_dir
from gencontent import generate_pages_recursive


def main():
    base_path = None
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"

    static_dir = "./static"
    docs_dir = "./docs"
    content_dir = "./content"
    template_path = "./template.html"
    if os.path.exists(docs_dir):
        print("DELETING PUBLIC DIRECTORY")
        shutil.rmtree(docs_dir)
    os.mkdir(docs_dir)
    copy_dir(static_dir, docs_dir)
    generate_pages_recursive(content_dir, template_path, docs_dir, base_path)


main()

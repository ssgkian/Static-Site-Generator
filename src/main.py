import os
import shutil

from copystatic import copy_dir
from gencontent import generate_pages_recursive


def main():
    static_dir = "./static"
    public_dir = "./public"
    content_dir = "./content"
    template_path = "./template.html"
    if os.path.exists(public_dir):
        print("DELETING PUBLIC DIRECTORY")
        shutil.rmtree(public_dir)
    os.mkdir(public_dir)
    copy_dir(static_dir, public_dir)
    generate_pages_recursive(content_dir, template_path, public_dir)


main()

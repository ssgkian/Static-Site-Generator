import os
import shutil


def copy_dir(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    items = os.listdir(source_dir)

    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            print("COPYING FILES TO STATIC DIRECTORY")
            copy_dir(source_path, dest_path)

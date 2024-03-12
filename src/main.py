import os
import shutil
from copystatic import copy_files_recursively
from gencontent import generate_page


def main():
    static_content_path = "./static"
    public_content_path = "./public"
    if os.path.exists(public_content_path):
        print("Deleting public directory...")
        shutil.rmtree(public_content_path)
        print("Creating public directory...")
        os.mkdir(public_content_path)
    else:
        print("Creating public directory...")
        os.mkdir(public_content_path)
    copy_files_recursively(static_content_path, public_content_path)
    generate_page("./content/index.md", "./template.html", "./public/index.html")


main()

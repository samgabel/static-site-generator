import os
import shutil
from copystatic import copy_files_recursively
from gencontent import (
    generate_page,
    generate_pages_recursive,
)

def main():
    static_content_path = "./static"
    content_path = "./content"
    template_path = "./template.html"
    public_content_path = "./public"
    # idempotent public dir
    if os.path.exists(public_content_path):
        print("Deleting public directory...")
        shutil.rmtree(public_content_path)
        print("Creating public directory...")
        os.mkdir(public_content_path)
    else:
        print("Creating public directory...")
        os.mkdir(public_content_path)
    # copy over static files to public dir
    copy_files_recursively(static_content_path, public_content_path)
    # generate_page("./content/index.md", "./template.html", "./public/index.html")
    # convert md into html, insert in html template, and create file structure in public dir
    generate_pages_recursive(content_path, template_path, public_content_path)


main()

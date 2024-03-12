import os
from markdown_blocks import markdown_to_html_node

def extract_title_markdown(markdown: str) -> str:
    lines = markdown.split("\n")
    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line[2:]
    return title


def generate_page(src_path: str, template_path: str, dst_path:str):
    print(f"Generating page from {src_path} to {dst_path} using {template_path}")
    with open(src_path, 'r') as f:
        md = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    # template with "{{ Content }}" replaced with src file converted html content
    template = template.replace("{{ Content }}", markdown_to_html_node(md).to_html())
    # completed template file with "{{ Title }}"
    template = template.replace("{{ Title }}", extract_title_markdown(md))
    # check if directory exists, if not create directory
    dst_dir_path = os.path.dirname(dst_path)
    if dst_dir_path != "":
        os.makedirs(dst_dir_path, exist_ok=True)
    # create file at dst_path and write template to it
    with open(dst_path, 'w') as f:
        f.write(template)


if __name__ == "__main__":
    generate_page("/Users/samgabel/Projects/Boot.Dev/static-site-generator/content/index.md", "/Users/samgabel/Projects/Boot.Dev/static-site-generator/template.html", "/Users/samgabel/Projects/Boot.Dev/static-site-generator/public")

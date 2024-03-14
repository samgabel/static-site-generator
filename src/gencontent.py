import os
from markdown_blocks import markdown_to_html_node


def generate_pages_recursive(src_path: str, template_path: str, dst_path: str):
    'Will convert md to html, insert title and content into an html template, and create and write content dir structure to public dir.'
    for file in os.listdir(src_path):
        extended_src = f"{src_path}/{file}"
        extended_dst = f"{dst_path}/{file}"
        if os.path.isfile(extended_src):
            extended_dst = f"{extended_dst[:-3]}.html"
            generate_page(extended_src, template_path, extended_dst)
        else:
            generate_pages_recursive(extended_src, template_path, extended_dst)


def generate_page(src_path: str, template_path: str, dst_path: str):
    'Used by `generate_pages_recursive` in order to convert md to html'
    print(f" * [{template_path}]: {src_path} -> {dst_path}")
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


def extract_title_markdown(markdown: str) -> str:
    'Used by generate page in order to extract the main h1 of the md'
    lines = markdown.split("\n")
    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line[2:]
    return title

import os
import shutil
import sys

from extract_markdown import extract_title
from markdown_blocks import markdown_to_html_node
from textnode import TextNode, TextType

def main():
    # test = TextNode("Hello there", TextType.LINK, "https://github.com/nickdellaquilo/")
    # print(test)

    transfer("static", "docs")

    basepath = '/'
    if sys.argv and len(sys.argv) > 1:
        basepath = sys.argv[1]
    generate_pages_recursive("content", "template.html", "docs", basepath)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path}  to {dest_path} using template {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    result = template_content.replace("{{ Title }}", title).replace("{{ Content }}", str(html_content)).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(result)

def generate_pages_recursive(dir_path_content, template_path, dir_path_dest, basepath):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                generate_page(
                    os.path.join(root, file),
                    template_path,
                    os.path.join(dir_path_dest, os.path.relpath(root, dir_path_content), file.replace(".md", ".html")),
                    basepath
                )

def transfer(src="static", dst="public"):
    if not os.path.exists(dst):
        os.makedirs(dst)
    shutil.rmtree(dst)
    shutil.copytree(src, dst)
    

if __name__ == "__main__":
    main()
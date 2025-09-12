import os
import shutil

from extract_markdown import extract_title
from markdown_blocks import markdown_to_html_node
from textnode import TextNode, TextType

def main():
    # test = TextNode("Hello there", TextType.LINK, "https://github.com/nickdellaquilo/")
    # print(test)

    transfer("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path}  to {dest_path} using template {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
    html_content = markdown_to_html_node(markdown_content)
    title = extract_title(markdown_content)
    result = template_content.replace("{{ Title }}", title).replace("{{ Content }}", str(html_content))
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(result)

def transfer(src="static", dst="public"):
    if not os.path.exists(dst):
        os.makedirs(dst)
    shutil.rmtree(dst)
    shutil.copytree(src, dst)
    

if __name__ == "__main__":
    main()
import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
    '''
    Extracts all markdown image links from the given text.
    Returns a list of tuples (alt text, url).
    '''
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    '''
    Extracts all markdown links from the given text.
    Returns a list of tuples (anchor text, url).
    '''
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("# "):
            return stripped_line[2:].strip()
    raise ValueError("No title found in markdown")
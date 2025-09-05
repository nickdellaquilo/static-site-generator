import re

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

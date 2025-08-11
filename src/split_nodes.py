from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: [TextNode], delimiter, text_type: TextType):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) == 1:
            result.append(node)
            continue

        if len(parts) % 2 == 0:
            raise Exception(
                f"Invalid Markdown syntax: unmatched delimiter '{delimiter}' in text '{node.text}'"
            )

        for i, part in enumerate(parts):
            if i % 2 == 0:
                result.append(TextNode(part, TextType.TEXT))
            else:
                result.append(TextNode(part, text_type))
    return result

def split_nodes_image(old_nodes: [TextNode]):
    # Placeholder for future implementation
    pass



def split_nodes_link(old_nodes: [TextNode]):
    # Placeholder for future implementation
    pass
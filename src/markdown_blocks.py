from enum import Enum
import re

BlockType = Enum('BlockType',
['PARAGRAPH', 'HEADING', 'CODE', 'QUOTE', 'UNORDERED_LIST', 'ORDERED_LIST']
    )

def block_to_block_type(block):
    """
    Takes a single block of markdown text as input and returns the BlockType representing the type of block it is. Assume all leading and trailing whitespace were already stripped.
    """
    lines = block.split('\n')
    # Heading
    if len(lines) == 1 and lines[0].startswith('#'):
        match = re.match(r'^(#{1,6})\s', lines[0])
        if match:
            return BlockType.HEADING
    # Code block
    if lines[0].startswith('```') and lines[-1].startswith('```') and len(lines) >= 2:
        return BlockType.CODE
    # Quote block
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    # Unordered list block
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    # Ordered list block
    if all(
        line.startswith(f"{i+1}. ")
        for i, line in enumerate(lines)
    ):
        return BlockType.ORDERED_LIST
    # Paragraph
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks
import unittest
from markdown_blocks import markdown_to_html_node, markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()

    def test_markdown_to_blocks_empty(self):
        md = """"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_newlines(self):
        md = """
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [""])
        
    def test_markdown_to_blocks_leading_trailing_newlines(self):
        md = """
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [""])

    def test_markdown_to_blocks_no_double_newline(self):
        md = """This is a paragraph with no double newlines.
This is still part of the same paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [md])

    def test_markdown_to_blocks_multiple_lists(self):
        md = """
- First list item
- Second list item

1. First numbered item
2. Second numbered item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- First list item\n- Second list item",
                "1. First numbered item\n2. Second numbered item",
            ],
        )

    def test_markdown_to_blocks_code_block(self):
        md = """
```
def hello_world():
    print("Hello, world!")
```
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ['```\ndef hello_world():\n    print("Hello, world!")\n```'])

    def test_block_to_block_type_paragraph(self):
        md = "This is a simple paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [md])
    
    def test_block_to_block_type_heading(self):
        md = "# Heading 1"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)
        md2 = "## Heading 2"
        self.assertEqual(block_to_block_type(md2), BlockType.HEADING)
        md3 = "###### Heading 6"
        self.assertEqual(block_to_block_type(md3), BlockType.HEADING)
        md4 = "#NoSpace"
        self.assertNotEqual(block_to_block_type(md4), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        md = "```\ncode block\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)
        md2 = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(md2), BlockType.CODE)
        md3 = "```\nnot closed"
        self.assertNotEqual(block_to_block_type(md3), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        md = "> This is a quote"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)
        md2 = "> Line 1\n> Line 2"
        self.assertEqual(block_to_block_type(md2), BlockType.QUOTE)
        md3 = "> Line 1\nNot a quote"
        self.assertNotEqual(block_to_block_type(md3), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        md = "- item 1\n- item 2"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)
        md2 = "- item 1\n* item 2"
        self.assertNotEqual(block_to_block_type(md2), BlockType.UNORDERED_LIST)
        md3 = "- item 1\nitem 2"
        self.assertNotEqual(block_to_block_type(md3), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        md = "1. item 1\n2. item 2"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)
        md2 = "1. item 1\n3. item 2"
        self.assertNotEqual(block_to_block_type(md2), BlockType.ORDERED_LIST)
        md3 = "1. item 1\n2 item 2"
        self.assertNotEqual(block_to_block_type(md3), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph_default(self):
        md = "Just a normal text block."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
        md2 = "Another\nmultiline\nparagraph."
        self.assertEqual(block_to_block_type(md2), BlockType.PARAGRAPH)





if __name__ == "__main__":
    unittest.main()

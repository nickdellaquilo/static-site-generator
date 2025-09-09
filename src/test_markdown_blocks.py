import unittest
from markdown_blocks import markdown_to_blocks


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

    




if __name__ == "__main__":
    unittest.main()

import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("This is a text node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_single_delimiter(self):
        node = TextNode("This is a `code block", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("unmatched delimiter", str(context.exception))

    def test_multiple_delimiters(self):
        node = TextNode("This is text with a `code block` and more text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and more text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_consecutive_delimiters(self):
        node = TextNode("Text with ``empty`` code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("", TextType.CODE),
            TextNode("empty", TextType.TEXT),
            TextNode("", TextType.CODE),
            TextNode(" code", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_non_text_node(self):
        node = TextNode("This is bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])



if __name__ == "__main__":
    unittest.main()
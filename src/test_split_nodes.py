import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

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
            TextNode("empty", TextType.TEXT),
            TextNode(" code", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_non_text_node(self):
        node = TextNode("This is bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_single(self):
        node = TextNode(
            "[link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        node = TextNode(
            "This is text without links.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is text without links.", TextType.TEXT)],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        # Test text_to_textnodes function
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected_nodes)

    def test_text_to_textnodes_no_formatting(self):
        text = "This is plain text without any formatting."
        nodes = text_to_textnodes(text)
        expected_nodes = [TextNode("This is plain text without any formatting.", TextType.TEXT)]
        self.assertEqual(nodes, expected_nodes)

    def test_text_to_textnodes_only_formatting(self):
        text = "**Bold** _Italic_ `Code` ![Image](https://example.com/image.png) [Link](https://example.com)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("Italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("Code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("Image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" ", TextType.TEXT),
            TextNode("Link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(nodes, expected_nodes)

    def test_text_to_textnodes_unmatched_delimiter(self):
        text = "This is **bold text with no closing delimiter"
        with self.assertRaises(Exception) as context:
            text_to_textnodes(text)
        self.assertIn("unmatched delimiter", str(context.exception))

    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        expected_nodes = [TextNode("", TextType.TEXT)]
        self.assertEqual(nodes, expected_nodes)

    def test_text_to_textnodes_adjacent_formatting(self):
        text = "**Bold**_Italic_`Code`"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("Bold", TextType.BOLD),
            TextNode("Italic", TextType.ITALIC),
            TextNode("Code", TextType.CODE),
        ]
        self.assertEqual(nodes, expected_nodes)

    def test_text_to_textnodes_nested_formatting(self):
        text = "This is **bold and _italic_** text"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold and _italic_", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected_nodes)

    

if __name__ == "__main__":
    unittest.main()
import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links, extract_title

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_images_none(self):
        text = "This is a sample text without images."
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_images_single(self):
        text = "Here is an image ![alt text](http://example.com/image.png)"
        self.assertEqual(extract_markdown_images(text), [("alt text", "http://example.com/image.png")])

    def test_extract_images_multiple(self):
        text = "First image ![first](http://example.com/first.png) and second image ![second](http://example.com/second.png)"
        self.assertEqual(extract_markdown_images(text), [("first", "http://example.com/first.png"), ("second", "http://example.com/second.png")])

    def test_extract_links_none(self):
        text = "This is a sample text without links."
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_links_single(self):
        text = "Here is a link [example](http://example.com)"
        self.assertEqual(extract_markdown_links(text), [("example", "http://example.com")])

    def test_extract_links_multiple(self):
        text = "First link [first](http://example.com/first) and second link [second](http://example.com/second)"
        self.assertEqual(extract_markdown_links(text), [("first", "http://example.com/first"), ("second", "http://example.com/second")])

    def test_extract_links_with_image(self):
        text = "Here is a link [example](http://example.com) and an image ![alt](http://example.com/image.png)"
        self.assertEqual(extract_markdown_links(text), [("example", "http://example.com")])
        self.assertEqual(extract_markdown_images(text), [("alt", "http://example.com/image.png")])

    def test_extract_title(self):
        text = "# This is the title\nThis is some content."
        self.assertEqual(extract_title(text), "This is the title")
    
    def test_extract_title_no_title(self):
        text = "This is some content without a title."
        with self.assertRaises(ValueError):
            extract_title(text)

    def test_extract_title_multiple_titles(self):
        text = "# First Title\nSome content.\n# Second Title"
        self.assertEqual(extract_title(text), "First Title")

    def test_extract_title_with_leading_spaces(self):
        text = "   # Title with leading spaces\nContent."
        self.assertEqual(extract_title(text), "Title with leading spaces")

    

if __name__ == "__main__":
    unittest.main()
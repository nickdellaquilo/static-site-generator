import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(tag="div", value="Test", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode(tag="div", value="Test", props={"class": "test-class"})
        self.assertEqual(node.props_to_html(), 'class="test-class"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(tag="div", value="Test", props={"class": "test-class", "id": "test-id"})
        self.assertEqual(node.props_to_html(), 'class="test-class" id="test-id"')

    def test_repr(self):
        node = HTMLNode(tag="div", value="Test", children=None, props={"class": "test-class"})
        self.assertEqual(repr(node), "HTMLNode(tag=div, value=Test, children=None, props={'class': 'test-class'})")

    def test_repr_no_props(self):
        node = HTMLNode(tag="div", value="Test", children=None, props=None)
        self.assertEqual(repr(node), "HTMLNode(tag=div, value=Test, children=None, props=None)")

    def test_repr_with_children(self):
        child_node = HTMLNode(tag="span", value="Child", props={"class": "child-class"})
        node = HTMLNode(tag="div", value="Test", children=[child_node], props={"class": "test-class"})
        self.assertEqual(repr(node), "HTMLNode(tag=div, value=Test, children=[HTMLNode(tag=span, value=Child, children=None, props={'class': 'child-class'})], props={'class': 'test-class'})")

    def test_repr_with_no_children(self):
        node = HTMLNode(tag="div", value="Test", children=[], props={"class": "test-class"})
        self.assertEqual(repr(node), "HTMLNode(tag=div, value=Test, children=[], props={'class': 'test-class'})")
    


if __name__ == "__main__":
    unittest.main()
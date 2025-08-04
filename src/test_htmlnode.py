import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("p", "Hello, world!", props={"class": "greeting"})
        self.assertEqual(node.to_html(), '<p class="greeting">Hello, world!</p>')

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child", props={"class": "child-class"})
        parent_node = ParentNode("div", [child_node], props={"id": "parent-id"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="parent-id"><span class="child-class">child</span></div>',
        )

    def test_parent_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_parent_to_html_multiple_children(self):
        child1 = LeafNode("span", "child1")
        child2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>")

    def test_nested_parent_nodes_three_levels(self):
        # <section><div><span>deep</span></div></section>
        deep_child = LeafNode("span", "deep")
        mid_parent = ParentNode("div", [deep_child])
        top_parent = ParentNode("section", [mid_parent])
        self.assertEqual(top_parent.to_html(), "<section><div><span>deep</span></div></section>")

    def test_nested_parent_nodes_with_props(self):
        # <section id="top"><div class="mid"><span style="color:red">deep</span></div></section>
        deep_child = LeafNode("span", "deep", props={"style": "color:red"})
        mid_parent = ParentNode("div", [deep_child], props={"class": "mid"})
        top_parent = ParentNode("section", [mid_parent], props={"id": "top"})
        self.assertEqual(
            top_parent.to_html(),
            '<section id="top"><div class="mid"><span style="color:red">deep</span></div></section>'
        )

    def test_nested_parent_nodes_mixed_leaf_and_parent(self):
        # <ul><li>one</li><li><b>two</b></li></ul>
        leaf1 = LeafNode("li", "one")
        leaf2 = LeafNode("b", "two")
        parent2 = ParentNode("li", [leaf2])
        ul_parent = ParentNode("ul", [leaf1, parent2])
        self.assertEqual(
            ul_parent.to_html(),
            "<ul><li>one</li><li><b>two</b></li></ul>"
        )

    def test_deeply_nested_parent_nodes(self):
        # <a><b><c><d>deepest</d></c></b></a>
        node = LeafNode("d", "deepest")
        for tag in ["c", "b", "a"]:
            node = ParentNode(tag, [node])
        self.assertEqual(node.to_html(), "<a><b><c><d>deepest</d></c></b></a>")

    def test_parent_node_with_mixed_children(self):
        # <div><span>text</span>plain</div>
        leaf1 = LeafNode("span", "text")
        leaf2 = LeafNode(None, "plain")
        parent = ParentNode("div", [leaf1, leaf2])
        self.assertEqual(parent.to_html(), "<div><span>text</span>plain</div>")
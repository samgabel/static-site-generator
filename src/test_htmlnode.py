import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
)


class TestHTMLNode(unittest.TestCase):

    def setUp(self):
        # HTMLNode objects to be used in tests
        self.base_node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.no_prop_node1 = HTMLNode()
        self.no_prop_node2 = HTMLNode("a", "https://google.com", None, None)
        # LeafNode objects to be used in tests
        self.leaf_node = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        self.no_children_node = LeafNode(tag="p", value="The quick brown fox jumps over the lazy dog")
        self.no_tag_node = LeafNode(None, value="The quick brown fox jumps over the lazy dog")
        self.no_tag_props_node = LeafNode(None, value="The quick brown fox jumps over the lazy dog", props={"href": "https://www.google.com"})
        # ParentNode objects to be used in tests
        self.parent_node = ParentNode(tag="p",
                                      children=[
                                          LeafNode("b", "Bold text"),
                                          LeafNode(None, "Normal text"),
                                          LeafNode("i", "italic text"),
                                          LeafNode(None, "Normal text")
                                      ])
        self.nested_parent_node_1 = ParentNode(tag="span", children=[self.parent_node])
        self.nested_parent_node_2 = ParentNode(tag="div", children=[self.nested_parent_node_1])
        self.parent_heading_node = ParentNode(tag="h3", children=[LeafNode(None, value="Heading Three")])


# TEST props_to_html --------------------------------------------------------------------

    def test_props_to_html(self):
        # Test that props_to_html() works to produce desired output
        node1 = self.base_node
        node2 = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node1.props_to_html(), node2)

    def test_no_props1_to_html(self):
        # Test that props_to_html() has the desired outcome when props=None
        node = self.no_prop_node1
        self.assertEqual(node.props_to_html(), "")

    def test_no_props2_to_html(self):
        # Test that props_to_html() has the desired outcome when props=None
        node = self.no_prop_node2
        self.assertEqual(node.props_to_html(), "")


# TEST LeafNode to_html ----------------------------------------------------------------

    def test_to_html(self):
        # Test that to_html() works to produce desired output
        node = self.leaf_node
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_no_children(self):
        # Test that to_html() has the desired output when children is omitted
        node = self.no_children_node
        self.assertEqual(node.to_html(), '<p>The quick brown fox jumps over the lazy dog</p>')

    def test_to_html_no_tag(self):
        # Test that to_html() has the desired output when tag is omitted
        node = self.no_tag_node
        self.assertEqual(node.to_html(), 'The quick brown fox jumps over the lazy dog')

    def test_to_html_no_tag_props(self):
        # Test that to_html() has the desired output when tag is omitted, but props is still included
        node = self.no_tag_props_node
        self.assertEqual(node.to_html(), 'The quick brown fox jumps over the lazy dog')


# TEST ParentNode to_html ---------------------------------------------------------------

    def test_to_html_parent(self):
        node = self.parent_node
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_to_html_parent_nested_1(self):
        node = self.nested_parent_node_1
        self.assertEqual(node.to_html(), '<span><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></span>')

    def test_to_html_parent_nested_2(self):
        node = self.nested_parent_node_2
        self.assertEqual(node.to_html(), '<div><span><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></span></div>')

    def test_to_html_parent_headings(self):
        node = self.parent_heading_node
        self.assertEqual(node.to_html(),  '<h3>Heading Three</h3>')


# TEST __repr__ -------------------------------------------------------------------------

    def test_repr(self):
        # Test __repr__ method to return the proper format
        node = self.base_node
        expected_repr = "HTMLNode(None, None, children: None, {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(repr(node), expected_repr)


# Allows you to have code in your module that is only run when the module is executed directly (not imported).
# If we import this test_htmlnode file into another file, we will import everything but...
# the code below won't execute since __name__ will not be "__main__".
if __name__ == "__main__":
    unittest.main()

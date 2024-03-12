import unittest

from textnode import (
    TextNode,
    # text_type_text,
    # text_type_bold,
    text_type_italic,
    # text_type_code,
    # text_type_image,
    text_type_link,
)


class TestTextNode(unittest.TestCase):

    def setUp(self):
        # Create common TextNode object to be used in multiple tests
        self.base_node = TextNode("This is a text node", text_type_link, "https://google.com")

        self.diff_text_node = TextNode("Different text node", text_type_link, "https://google.com")
        self.diff_type_node = TextNode("This is a text node", text_type_italic, "https://google.com")
        self.diff_url_node = TextNode("This is a text node", text_type_italic, "https://yahoo.com")
        self.no_text_node = TextNode("", "bold", "https://google.com")
        self.no_url_node = TextNode("This is a text node", text_type_link)
        self.invalid_url_node = TextNode("This is a text node", "bold", "invalid")


# TEST __eq__ ---------------------------------------------------------------------------

    def test_eq(self):
        # Test __eq__ method to works properly when objects are equal
        node1 = self.base_node
        node2 = self.base_node
        self.assertEqual(node1, node2)

    def test_eq_false_object(self):
        # Test __eq__ method to works properly when objects are NOT equal
        node1 = self.base_node
        node2 = ""
        self.assertNotEqual(node1, node2)

    def test_eq_false_text(self):
        # Test __eq__ method works properly when text is NOT equal
        node1 = self.base_node
        node2 = self.diff_text_node
        self.assertNotEqual(node1, node2)

    def test_eq_false_type(self):
        # Test __eq__ method works properly when text_type is NOT equal
        node1 = self.base_node
        node2 = self.diff_type_node
        self.assertNotEqual(node1, node2)

    def test_eq_false_url(self):
        # Test __eq__ method works properly when url is NOT equal
        node1 = self.base_node
        node2 = self.diff_url_node
        self.assertNotEqual(node1, node2)


# TEST __repr__ -------------------------------------------------------------------------

    def test_repr(self):
        # Test __repr__ method ato return the proper format
        node = self.base_node
        expected_repr = "TextNode(This is a text node, link, https://google.com)"
        self.assertEqual(repr(node), expected_repr)


# TEST instance variables ---------------------------------------------------------------

    def test_empty_txt(self):
        # Test behavior with empty text
        node = self.no_text_node
        self.assertEqual(node.text, "")

    def test_url_none(self):
        # Test if url parameter is None by default
        node = self.no_url_node
        self.assertIsNone(node.url)


    # TODO: feat: url format check
    # first implement URL format checking in TextNode class


# Allows you to have code in your module that is only run when the module is executed directly (not imported).
# If we import this test_textnode file into another file, we will import everything but..
# the code below won't execute since __name__ will not be "__main__".
if __name__ == "__main__":
    unittest.main()

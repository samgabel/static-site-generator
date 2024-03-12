import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)



class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_with_nonTextType(self):
        node = TextNode("`print('Hello world!')`", text_type_code)
        nonTextNode = "the quick brown fox"
        new_nodes = split_nodes_delimiter([node, nonTextNode], "**", text_type_bold) # pyright: ignore[reportArgumentType]
        self.assertListEqual(
            [
                TextNode("`print('Hello world!')`", text_type_code),
                "the quick brown fox",
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another", "https://i.imgur.com/dfsdkjfd.png"),
            ],
            extract_markdown_images(text)
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertListEqual(
            [
                ("link", "https://www.example.com"), 
                ("another", "https://www.example.com/another"),
            ],
            extract_markdown_links(text)
        )

    def test_split_nodes_image(self):
        node = TextNode( "This is text with an ![image](url1) and another ![second image](url2)", text_type_text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "url1"),
                TextNode(" and another ", text_type_text),
                TextNode( "second image", text_type_image, "url2"),
            ],
            split_nodes_image([node])
        )

    def test_split_nodes_image_single(self):
        node = TextNode( "![image](url1)", text_type_text)
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "url1"),
            ],
            split_nodes_image([node])
        )

    def test_split_nodes_link(self):
        node = TextNode( "This is text with an [link](url1) and another [second link](url2)", text_type_text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("link", text_type_link, "url1"),
                TextNode(" and another ", text_type_text),
                TextNode( "second link", text_type_link, "url2"),
            ],
            split_nodes_link([node])
        )

    def test_split_nodes_link_wrong_text_type(self):
        node = TextNode( "`print(Hello world!)`", text_type_code)
        self.assertListEqual(
            [
                TextNode("`print(Hello world!)`", text_type_code),
            ],
            split_nodes_link([node])
        )


# FINAL PRODUCT TESTS BELOW --------------------------------------------------------------------


    def test_1_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://image.png) and a [link](https://google.com)"
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://image.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://google.com"),
            ],
            text_to_textnodes(text)
        )

    def test_2_text_to_textnodes(self):
        text = "This is *text* with an **bold** word and a `code block` and an ![image](https://image.png) and a [link](https://google.com)"
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_italic),
                TextNode(" with an ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://image.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://google.com"),
            ],
            text_to_textnodes(text)
        )

    def test_3_text_to_textnodes(self):
        text = "This is `print(2 * 3)` and an ![image](https://image.png) and a [link](https://google.com)"
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("print(2 * 3)", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://image.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://google.com"),
            ],
            text_to_textnodes(text)
        )

    def test_4_text_to_textnodes(self):
        text = "This is `print(2 * 3)` and an ![*image](https://image.png) and a `[link](https://google.com)`"
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("print(2 * 3)", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("*image", text_type_image, "https://image.png"),
                TextNode(" and a ", text_type_text),
                TextNode("[link](https://google.com)", text_type_code),
            ],
            text_to_textnodes(text)
        )

    # NOTE: Allow for image links (image nested within a link)
    # def test_5_text_to_textnodes(self):
    #     text = "This is a image nested in a link (an image that when clicked goes to a link) [![*image](https://image.png)](https://google.com)"
    #     self.assertListEqual(
    #         [
    #             TextNode("This is a image nested in a link (an image that when clicked goes to a link) ", text_type_text),
    #             TextNode("![*image](https://image.png)", text_type_link, "https://google.com"),
    #         ],
    #         text_to_textnodes(text)
    #     )


if __name__ == "__main__":
    unittest.main()

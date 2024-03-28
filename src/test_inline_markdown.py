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


def test_delim_1():
    """
    `split_nodes_delimiter` tested with 1 inline bold words
    """
    node = TextNode("This is text with a **bolded** word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
    assert new_nodes == [
        TextNode("This is text with a ", text_type_text),
        TextNode("bolded", text_type_bold),
        TextNode(" word", text_type_text),
    ]


def test_delim_2():
    """
    `split_nodes_delimiter` tested with 2 inline bold words
    """
    node = TextNode(
        "This is text with a **bolded** word and **another**", text_type_text
    )
    new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
    assert new_nodes == [
        TextNode("This is text with a ", text_type_text),
        TextNode("bolded", text_type_bold),
        TextNode(" word and ", text_type_text),
        TextNode("another", text_type_bold),
    ]


def test_delim_3():
    """
    `split_nodes_delimiter` tested with 1 inline bold phrase and 1 inline bold word
    """
    node = TextNode(
        "This is text with a **bolded word** and **another**", text_type_text
    )
    new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
    assert new_nodes == [
        TextNode("This is text with a ", text_type_text),
        TextNode("bolded word", text_type_bold),
        TextNode(" and ", text_type_text),
        TextNode("another", text_type_bold),
    ]


def test_delim_4():
    """
    `split_nodes_delimiter` tested with 1 inline italic word
    """
    node = TextNode("This is text with an *italic* word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
    assert new_nodes == [
        TextNode("This is text with an ", text_type_text),
        TextNode("italic", text_type_italic),
        TextNode(" word", text_type_text),
    ]


def test_delim_5():
    """
    `split_nodes_delimiter` tested with 1 inline code phrase
    """
    node = TextNode("This is text with a `code block` word", text_type_text)
    new_nodes = split_nodes_delimiter([node], "`", text_type_code)
    assert new_nodes == [
        TextNode("This is text with a ", text_type_text),
        TextNode("code block", text_type_code),
        TextNode(" word", text_type_text),
    ]


def test_delim_6():
    """
    `split_nodes_delimiter` tested with 1 long inline code phrase
    """
    node = TextNode("`print('Hello world!')`", text_type_code)
    nonTextNode = "the quick brown fox"
    new_nodes = split_nodes_delimiter(
        [node, nonTextNode], "**", text_type_bold  # pyright: ignore[reportArgumentType]
    )
    assert new_nodes == [
        TextNode("`print('Hello world!')`", text_type_code),
        "the quick brown fox",
    ]


def test_extract_img():
    """
    `extract_markdown_images` tested with 1 inline image
    """
    text = (
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
        "and ![another](https://i.imgur.com/dfsdkjfd.png)"
    )
    assert extract_markdown_images(text) == [
        ("image", "https://i.imgur.com/zjjcJKZ.png"),
        ("another", "https://i.imgur.com/dfsdkjfd.png"),
    ]


def test_extract_link():
    """
    `extract_markdown_links` tested with 1 inline link
    """
    text = (
        "This is text with a [link](https://www.example.com) "
        "and [another](https://www.example.com/another)"
    )
    assert extract_markdown_links(text) == [
        ("link", "https://www.example.com"),
        ("another", "https://www.example.com/another"),
    ]


def test_split_img_1():
    """
    `split_nodes_image` tested with 2 inline images
    """
    node = TextNode(
        "This is text with an ![image](url1) and another ![second image](url2)",
        text_type_text,
    )
    assert split_nodes_image([node]) == [
        TextNode("This is text with an ", text_type_text),
        TextNode("image", text_type_image, "url1"),
        TextNode(" and another ", text_type_text),
        TextNode("second image", text_type_image, "url2"),
    ]


def test_split_img_2():
    """
    `split_nodes_image` tested with 1 inline image
    """
    node = TextNode("![image](url1)", text_type_text)
    assert split_nodes_image([node]) == [TextNode("image", text_type_image, "url1")]


def test_split_link_1():
    """
    `split_nodes_link` tested with 2 inline links
    """
    node = TextNode(
        "This is text with an [link](url1) and another [second link](url2)",
        text_type_text,
    )
    assert split_nodes_link([node]) == [
        TextNode("This is text with an ", text_type_text),
        TextNode("link", text_type_link, "url1"),
        TextNode(" and another ", text_type_text),
        TextNode("second link", text_type_link, "url2"),
    ]


def test_split_link_2():
    """
    `split_nodes_link` tested with 1 inline code phrase
    """
    node = TextNode("`print(Hello world!)`", text_type_code)
    assert split_nodes_link([node]) == [TextNode("`print(Hello world!)`", text_type_code)]


def test_text_to_textnodes_1():
    """
    `text_to_textnodes` tested with multi-line input wuth multiple inline syntax per line
    > testing ordering of function calls
    """
    text = (
        "This is **text** with an *italic* word and a `code block` "
        "and an ![image](https://image.png) and a [link](https://google.com)"
    )
    assert text_to_textnodes(text) == [
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
    ]


def test_text_to_textnodes_2():
    """
    `text_to_textnodes` tested with multi-line input wuth multiple inline syntax per line
    > testing ordering of function calls
    """
    text = (
        "This is *text* with an **bold** word and a `code block` "
        "and an ![image](https://image.png) and a [link](https://google.com)"
    )
    assert text_to_textnodes(text) == [
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
    ]


def test_text_to_textnodes_3():
    """
    `text_to_textnodes` tested with single-line input wuth multiple inline syntax per line
    > testing ordering of function calls
    """
    text = "This is `print(2 * 3)` and an ![image](https://image.png) and a [link](https://google.com)"
    assert text_to_textnodes(text) == [
        TextNode("This is ", text_type_text),
        TextNode("print(2 * 3)", text_type_code),
        TextNode(" and an ", text_type_text),
        TextNode("image", text_type_image, "https://image.png"),
        TextNode(" and a ", text_type_text),
        TextNode("link", text_type_link, "https://google.com"),
    ]


def test_text_to_textnodes_4():
    """
    `text_to_textnodes` tested with single-line input wuth multiple inline syntax per line
    > testing ordering of function calls
    """
    text = "This is `print(2 * 3)` and an ![*image](https://image.png) and a `[link](https://google.com)`"
    assert text_to_textnodes(text) == [
        TextNode("This is ", text_type_text),
        TextNode("print(2 * 3)", text_type_code),
        TextNode(" and an ", text_type_text),
        TextNode("*image", text_type_image, "https://image.png"),
        TextNode(" and a ", text_type_text),
        TextNode("[link](https://google.com)", text_type_code),
    ]

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

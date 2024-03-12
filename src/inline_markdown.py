import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


# sequencially parse through the md text line
def text_to_textnodes(text: str) -> list[TextNode]:
    'Sequencially parse though the md text line applying inline md syntax where needed and splitting md into TextNodes'
    nodes = [TextNode(text, text_type_text)]
    # we want this order specifically based on precedence in markdown syntax
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    return nodes



def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_types: str) -> list[TextNode]:
    'Will split up text nodes based on `text_types` and return a list of new text nodes'
    new_nodes = []
    for on in old_nodes:
        # only allow TextNode objects into the split process
        if not isinstance(on, TextNode):
            new_nodes.append(on)
            continue
        # only allow "text" type nodes into the split process
        if on.text_type != text_type_text:
            new_nodes.append(on)
            continue
        # split our object.text by our given delimiter argument
        split_text = on.text.split(delimiter)
        # if only 1 split occurs that means that we have an open ended delimiter
        if len(split_text) == 2:
            raise ValueError("Markdown Error: unclosed delimiter")
        for i in range(len(split_text)):
            # remove objects with empty text strings (if there is a delimiter at the begining/end, this will happen)
            if split_text[i] == "":
                continue
            # even indexed strings will always be non-delimited text
            if i % 2 == 0:
                new_nodes.append(TextNode(split_text[i], text_type_text))
            else:
                new_nodes.append(TextNode(split_text[i], text_types))
    return new_nodes



def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    'Similar to `split_nodes_delimiter()`, but will split out image details and return a list of text and image TextNode objects'
    new_nodes = []
    for on in old_nodes:
        # load in list of tuples with image details
        image_tup = extract_markdown_images(on.text)
        # if image details are present in any of the old_nodes
        # doubles as the base case for the recursive call
        if image_tup:
            # we will only split once per recursion in order to properly sequence nodes
            split_text = on.text.split(f"![{image_tup[0][0]}]({image_tup[0][1]})", 1)
            # the image details will always be at the second index of the split_text list
            processed_text = [ TextNode(split_text[0], text_type_text) , TextNode(image_tup[0][0], text_type_image, image_tup[0][1]) ]
            # if the image details are at the start of the node, then the split will create a blank list item before the image details
            if processed_text[0].text == "":
                new_nodes.append(processed_text[1])
            else:
                # we want to `extend` both items onto the new_nodes list, not append a list into the new_nodes list
                new_nodes.extend(processed_text)
            # RECURSION: extend each recursion layer's `new_nodes` where the second half of split_text (unprocessed half) is the argument
            new_nodes.extend(split_nodes_image([TextNode(split_text[1], text_type_text)]))
        else:
            # deepest layer of recursion, if TextNode().text is empty, then return empty string instead of TextNode object with empty string
            if on.text == "":
                return []
            # append TextNode object to new_nodes list without processing if there are no images present in the object
            else:
                new_nodes.append(on)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    'Similar to `split_nodes_delimiter()`, but will split out link details and return a list of text and link TextNode objects'
    # TODO: feat: image links
    # Allow for image links (image nested in a link)
    # see unittest (NOTE) for details
    new_nodes = []
    for on in old_nodes:
        # for instances when our old_node is not a text_type "text"
        if on.text_type != text_type_text:
            new_nodes.append(on)
            continue
        # load in list of tuples with link details
        link_tup = extract_markdown_links(on.text)
        # if link details are present in any of the old_nodes
        # doubles as the base case for the recursive call
        if link_tup:
            # we will only split once per recursion in order to properly sequence nodes
            split_text = on.text.split(f"[{link_tup[0][0]}]({link_tup[0][1]})", 1)
            # the link details will always be at the second index of the split_text list
            processed_text = [ TextNode(split_text[0], text_type_text) , TextNode(link_tup[0][0], text_type_link, link_tup[0][1]) ]
            # if the link details are at the start of the node, then the split will create a blank list item before the link details
            if processed_text[0].text == "":
                new_nodes.append(processed_text[1])
            else:
                # we want to `extend` both items onto the new_nodes list, not append a list into the new_nodes list
                new_nodes.extend(processed_text)
            # RECURSION: extend each recursion layer's `new_nodes` where the second half of split_text (unprocessed half) is the argument
            new_nodes.extend(split_nodes_link([TextNode(split_text[1], text_type_text)]))
        else:
            # deepest layer of recursion, if TextNode().text is empty, then return empty list instead of TextNode object with empty string
            if on.text == "":
                return []
            # append TextNode object to new_nodes list without processing if there are no links present in the object
            else:
                new_nodes.append(on)
    return new_nodes



# this will extract a list of tuples of alt text and urls
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    '''
    This will extract a list of tuples of alt text and urls. To be used by `split_nodes_image()`.

    `text = "This is text with an ![image](url) and ![another](url2)"`
    `extract_markdown_links(text)`
    `[ ("image", url), ("another", url2) ]``
    '''
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


# this will extract a list of tuples of anchor text and urls
def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    '''
    This will extract a list of tuples of anchor text and urls. `To be used by split_nodes_link()`.

    *See `extract_markdown_images()` for info on behavior*
    '''
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

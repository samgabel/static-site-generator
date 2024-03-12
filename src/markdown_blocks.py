import re
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ol = "ordered_list"
block_type_ul = "unordered_list"


def markdown_to_html_node(markdown: str) -> ParentNode:
    '''
    Main function that converts md string into a ParentNode of tag="div".
    This returns our Top Level ParentNode.
    We can use `markdown_to_html_node(markdown).to_html()` to turn the markdown file into pure HTML.
    '''
    blocks = markdown_to_blocks(markdown)
    children: list[ParentNode] = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children=children)


# TODO: refactor: "\n" & indents
# validate new blocks based on "\n" + different block type instead of... just "\n\n"
# also have to figure out how indents will play into block nesting

def markdown_to_blocks(markdown: str) -> list[str]:
    'Will be able to detect and append each new block when parsing through a md file'
    markdown_blocks: list[str] = []
    # split at blank newlines
    for block in markdown.split("\n\n"):
        if block != str(""):
            # gets rid of spaces (not tabs) before and after blocks
            block = block.strip()
            markdown_blocks.append(block)
    return markdown_blocks


def block_to_html_node(block):
    '''
    This gives us a way to return a second-level ParentNode and its children given a md block.
    All it is doing is pointing us to the right function based on `block_type`

    Used by: `markdown_to_html_node`
    '''
    block_type = block_to_block_type(block)
    if block_type is block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type is block_type_heading:
        return heading_to_html_node(block)
    if block_type is block_type_code:
        return code_to_html_node(block)
    if block_type is block_type_ol:
        return ol_to_html_node(block)
    if block_type is block_type_ul:
        return ul_to_html_node(block)
    if block_type is block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def block_to_block_type(block: str) -> str:
    '''
    The only goal with this function is to figure out what kind of block it is, not if each line belongs in the block it is in

    Used by: `block_to_html_node`
    '''
    block = block.strip("\n")
    block = block.strip("    ")
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return block_type_heading
    if block[:3] == "```" and block[-3:] == "```":
        return block_type_code
    if block[:2] == "> ":
        return block_type_quote
    if block[:2] == "- " or block[:2] == "* ":
        return block_type_ul
    if re.match(r'\d+', block[0]) and (block[1] == "." or block[1] == ")"):
        return block_type_ol
    return block_type_paragraph


# Object Conversion Function (string => TextNode => LeafNode)
def text_to_children(text: str) -> list[LeafNode]:
    '''
    Given a text string, it converts it to list of TextNodes which are converted to a list of LeafNodes.
    This list is to be used as the `children` argument for ParentNode objects
    '''
    # string => TextNode
    text_nodes = text_to_textnodes(text)
    children: list[LeafNode] = []
    for text_node in text_nodes:
        # TextNode => LeafNode
        leaf_node = text_node_to_html_node(text_node)
        children.append(leaf_node)
    return children


def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("\n```"):
        raise ValueError("Invalid code block")
    # we don't want the newline char so we go till "-4" instead of "-3"
    text = block[4:-4]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def ol_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ul_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        # if not line.startswith(">"):
        #     raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


if __name__ == "__main__":
    block = '''
# Heading

This is **bolded** paragraph

Another paragraph block,
this time with another *line*.

- Unordered list item 1
- second item

```
print("Hello world!")
```

> This is a quote
'''
    print(markdown_to_html_node(block).to_html())
    # <div><h1>Heading</h1><p>This is <b>bolded</b> paragraph</p><p>Another paragraph block, this time with another <i>line</i>.</p><ul><li>Unordered list item 1</li><li>second item</li></ul><pre><code>print("Hello world!")</code></pre></div>

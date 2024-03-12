from typing import Union

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        if not isinstance(tag, str) and tag is not None:
            raise TypeError("Tag must be a string")
        if not isinstance(value, str) and value is not None:
            raise TypeError("Value must be a string")
        if not isinstance(children, list) and children is not None:
            raise TypeError("Children must be a list")
        if not isinstance(props, dict) and props is not None:
            raise TypeError("Props must be a dictionary")
        # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.tag: Union[str, None] = tag
        # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.value: Union[str, None] = value
        # A list of HTMLNode objects representing the children of this node
        self.children: Union[list[HTMLNode], None] = children
        # A dictionary representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        self.props: Union[dict[str, str], None] = props

    def to_html(self):
        'To be overwritten by a childclass'
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        'Returns a stringified version of the props argument dictionary'
        if self.props is None:
            return ""
        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html

    def __repr__(self):
        # give myself a way to print out an HTMLNode object and see its arguments
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"



# It's a "leaf" in the tree of HTML nodes. It's a node with no children.
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        'Will render a leaf node as an HTML string'
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        # give myself a way to print out an LeafNode object and see its arguments
        return f"LeafNode({self.tag}, {self.value}, {self.props})"



# We need to be able to recurse through nested HTML nodes
class ParentNode(HTMLNode):
    def __init__(self, tag, children=None, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        'Will recurse through nested parent nodes and pass on leaf nodes to be rendered into html'
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid HTML: no children")
        branch_results = ""
        for child in self.children:
            # when child is of a ParentNode object it will recurse until it reaches a LeafNode object
            # the act of running the `.to_html` method on a LeafNode object is essentially the base case for the recursion
            branch_results += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{branch_results}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

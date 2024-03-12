import unittest
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,

    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_ul,
    block_type_ol,

)



class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = '''
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
    * with items
'''
        self.assertListEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n    * with items",
            ],
            markdown_to_blocks(markdown)
        )

    # NOTE: This test case will fail until we include functionality for keeping tabs and
    # separating blocks by "\n" + new block type instead of just "\n\n"

#     def test_markdown_to_blocks_extras(self):
#         markdown = '''
# # Heading
# This is **bolded** paragraph
#
#
# This is another paragraph with *italic* text and `code` here
# This is the same paragraph on a new line
#
# - this is a list item:
#     ```python
#     print(Hello world!)
#     # Hello world!
#     ```
#     > this prints Hello world!
#
# * This is a list
#     * with items
# '''
#         self.assertListEqual(
#             [
#                 "# Heading",
#                 "This is **bolded** paragraph",
#                 "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
#                 "- this is a list item:",
#                 "   ```python\n    print(Hello world!)\n    # Hello world!\n    ```",
#                 "   > this prints Hello world!",
#                 "* This is a list\n    * with items",
#             ],
#             markdown_to_blocks(markdown)
#         )


    def test_block_to_block_type_paragraph(self):
        block = '''
The quick brown fox jumps
over the lazy dog'''
        self.assertEqual(block_type_paragraph, block_to_block_type(block))

    def test_block_to_block_type_heading(self):
        block = '''
###### Heading
The quick brown fox jumps
over the lazy dog'''
        self.assertEqual(block_type_heading, block_to_block_type(block))

    def test_block_to_block_type_code(self):
        block = '''
```
print(Hello world!)
```'''
        self.assertEqual(block_type_code, block_to_block_type(block))

    def test_block_to_block_type_quote(self):
        block = '''
> The quick brown fox jumps
over the lazy dog'''
        self.assertEqual(block_type_quote, block_to_block_type(block))

    def test_block_to_block_type_ul(self):
        block = '''
- The quick brown fox jumps
    * over the lazy dog'''
        self.assertEqual(block_type_ul, block_to_block_type(block))

    def test_block_to_block_type_ol(self):
        block = '''
1) The quick brown fox jumps
2. over the lazy dog'''
        self.assertEqual(block_type_ol, block_to_block_type(block))

    def test_block_to_block_types(self):
            block = "# heading"
            self.assertEqual(block_to_block_type(block), block_type_heading)
            block = "```\ncode\n```"
            self.assertEqual(block_to_block_type(block), block_type_code)
            block = "> quote\n> more quote"
            self.assertEqual(block_to_block_type(block), block_type_quote)
            block = "* list\n* items"
            self.assertEqual(block_to_block_type(block), block_type_ul)
            block = "1. list\n2. items"
            self.assertEqual(block_to_block_type(block), block_type_ol)
            block = "paragraph"
            self.assertEqual(block_to_block_type(block), block_type_paragraph)


# FINAL PRODUCT ----------------------------------------------------------------------------------------------


    def test_markdown_to_html(self):
        block = '''
# Title




## First Heading

This is **bolded** paragraph

Another paragraph block,
this time with another *line*.

- Unordered list item 1
- second item

```
print("Hello world!")
```

> this prints "Hello world!"



## Second Heading

1) first
2) second

![Image](https:/google.com/image.png)

> This is a quote
and this should be on the same `line`
'''
        self.maxDiff = None
        self.assertEqual(
            '<div><h1>Title</h1><h2>First Heading</h2><p>This is <b>bolded</b> paragraph</p><p>Another paragraph block, this time with another <i>line</i>.</p><ul><li>Unordered list item 1</li><li>second item</li></ul><pre><code>print("Hello world!")</code></pre><blockquote>this prints "Hello world!"</blockquote><h2>Second Heading</h2><ol><li>first</li><li>second</li></ol><p><img src="https:/google.com/image.png" alt="Image"></img></p><blockquote>This is a quote and this should be on the same <code>line</code></blockquote></div>',
            markdown_to_html_node(block).to_html()
        )




if __name__ == "__main__":
    unittest.main()

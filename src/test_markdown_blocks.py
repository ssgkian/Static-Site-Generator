import unittest

from markdown_blocks import (
    BlockType,
    block_to_block_type,
    extract_title,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_empty(self):
        md = """
        """

        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    # test block_to_block_type

    def test_block_type(self):
        block = "# Text"  # headings
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "####### Text"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "```Text```"  # code
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = """```
        Text```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = """
    ```
    This is text that should remain
    the same even with inline stuff
    ```
    """
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = ">Text\n>Text"  # quote
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = ">Text\nText"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "- Text\n- Text"  # unordered_list
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "- Text\n Text"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "1. Text\n2. Text\n3. Text"  # ordered_list
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "1. Text\n. Text\n3. Text"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # test markdown_to_html_node
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with *italic* text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that *should* remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that *should* remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """### Heading with **bold** and *italic* text"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Heading with <b>bold</b> and <i>italic</i> text</h3></div>",
        )

    def test_quote(self):
        md = """
        > This is text
        > that is **bold**
        > and
        > *italic*
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is text\nthat is <b>bold</b>\nand\n<i>italic</i></blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
        - Test
        - *Test*
        - **Test**"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Test</li><li><i>Test</i></li><li><b>Test</b></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
        1. Test
        2. *Test*
        3. **Test**"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Test</li><li><i>Test</i></li><li><b>Test</b></li></ol></div>",
        )

    # extract title tests
    def test_extract_title(self):
        md = """Test,
        Bold
        Italic
        # Heading
        Check"""

        extracted = extract_title(md)
        self.assertEqual(extracted, "Heading")

import unittest
from markdown_blocks import *


class TestBlockMarkdown(unittest.TestCase):
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
    def test_preserves_inline_formatting(self):
        md = """
        This has _italic_ and **bold**

        `code` inline
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This has _italic_ and **bold**",
                "`code` inline"
            ]
        )
    def test_headings(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Invalid"), BlockType.PARAGRAPH)

    def test_code_blocks(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nmulti\nline\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("``invalid``"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```unclosed"), BlockType.PARAGRAPH)

    def test_quote_blocks(self):
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">Valid"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Valid\nInvalid"), BlockType.PARAGRAPH)

    def test_unordered_lists(self):
        self.assertEqual(block_to_block_type("- Item"), BlockType.ULIST)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.ULIST)
        self.assertEqual(block_to_block_type("* Item"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("-No space"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- Item\n\n- Another"), BlockType.PARAGRAPH)

    def test_ordered_lists(self):
        self.assertEqual(block_to_block_type("1. First"), BlockType.OLIST)
        self.assertEqual(block_to_block_type("1. First\n2. Second"), BlockType.OLIST)
        self.assertEqual(block_to_block_type("1.First"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("2. First"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. First\n3. Third"), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        self.assertEqual(block_to_block_type("Plain text"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Multi\nline\ntext"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1.Not list"), BlockType.PARAGRAPH)

    def test_edge_cases(self):
        self.assertEqual(block_to_block_type("   "), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("-"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(">"), BlockType.QUOTE)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

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
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_blockquote(self):
        md = """
        > This is a
        > blockquote block

        this is paragraph text

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
    
    def test_lists(self):
        md = """
        - This is a list
        - with items
        - and _more_ items

        1. This is an `ordered` list
        2. with items
        3. and more items

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )
    def test_code(self):
            md = """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )

    def test_basic_h1(self):
        md = "# Hello"
        title = extract_title(md)
        self.assertEqual(title, "Hello")

    def test_h1_with_whitespace(self):
        md = "   #    Hello World   "
        title = extract_title(md)
        self.assertEqual(title, "Hello World")

    def test_h1_not_first_line(self):
        md = """
        Some intro text here.

        # My Title

        More content below.
        """
        title = extract_title(md)
        self.assertEqual(title, "My Title")
    
    def test_no_headers(self):
        md = "This is just a plain paragraph with no headers."
        with self.assertRaises(Exception):
            extract_title(md)

    def test_only_h2_headers(self):
        md = """
        ## Header Two
        ### Header Three
        """
        with self.assertRaises(Exception):
            extract_title(md)

    def test_empty_string(self):
        md = ""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_empty_h1(self):
        md = "#     "
        with self.assertRaises(Exception):
            extract_title(md)


    
if __name__ == "__main__":
    unittest.main()

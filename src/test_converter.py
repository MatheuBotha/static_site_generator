import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)
from converter import text_node_to_html_node, split_nodes_delimiter


class TestConverter(unittest.TestCase):
    def test_text_node_to_html_node_text_type(self):
        text_node = TextNode('myval', 'text', None)
        html_node = text_node_to_html_node(text_node)
        expected = 'myval'
        self.assertEqual(html_node.to_html(), expected)

    def test_text_node_to_html_node_format_type(self):
        text_node = TextNode('myval', 'bold', None)
        html_node = text_node_to_html_node(text_node)
        expected = '<b>myval</b>'
        self.assertEqual(html_node.to_html(), expected)

    def test_text_node_to_html_node_link_type(self):
        text_node = TextNode('myval', 'link', 'http://my_url')
        html_node = text_node_to_html_node(text_node)
        expected = '<a href="http://my_url">myval</a>'
        self.assertEqual(html_node.to_html(), expected)

    def test_text_node_to_html_node_image_type(self):
        text_node = TextNode('myval', 'image', 'http://my_url')
        html_node = text_node_to_html_node(text_node)
        expected = '<img src="http://my_url" alt="myval"></img>'
        self.assertEqual(html_node.to_html(), expected)


    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_at_start(self):
        node = TextNode("`code block` This is text with a", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        expected = [
            TextNode("code block", text_type_code),
            TextNode(" This is text with a", text_type_text),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_at_end(self):
        node = TextNode("This is text with a `code block`", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_more_than_one(self):
        node = TextNode("This is text with a `code block` `code block` apples", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" apples", text_type_text),
        ]
        self.assertEqual(new_nodes, expected)

if __name__ == "__main__":
    unittest.main()
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
import converter


class TestConverter(unittest.TestCase):
    def test_text_node_to_html_node_text_type(self):
        text_node = TextNode('myval', 'text', None)
        html_node = converter.text_node_to_html_node(text_node)
        expected = 'myval'
        self.assertEqual(html_node.to_html(), expected)

    def test_text_node_to_html_node_format_type(self):
        text_node = TextNode('myval', 'bold', None)
        html_node = converter.text_node_to_html_node(text_node)
        expected = '<b>myval</b>'
        self.assertEqual(html_node.to_html(), expected)

    def test_text_node_to_html_node_link_type(self):
        text_node = TextNode('myval', 'link', 'http://my_url')
        html_node = converter.text_node_to_html_node(text_node)
        expected = '<a href="http://my_url">myval</a>'
        self.assertEqual(html_node.to_html(), expected)

    def test_text_node_to_html_node_image_type(self):
        text_node = TextNode('myval', 'image', 'http://my_url')
        html_node = converter.text_node_to_html_node(text_node)
        expected = '<img src="http://my_url" alt="myval"></img>'
        self.assertEqual(html_node.to_html(), expected)


    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = converter.split_nodes_delimiter([node], "`", text_type_code)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_at_start(self):
        node = TextNode("`code block` This is text with a", text_type_text)
        new_nodes = converter.split_nodes_delimiter([node], "`", text_type_code)
        expected = [
            TextNode("code block", text_type_code),
            TextNode(" This is text with a", text_type_text),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_at_end(self):
        node = TextNode("This is text with a `code block`", text_type_text)
        new_nodes = converter.split_nodes_delimiter([node], "`", text_type_code)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_more_than_one(self):
        node = TextNode("This is text with a `code block` `code block` apples", text_type_text)
        new_nodes = converter.split_nodes_delimiter([node], "`", text_type_code)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" apples", text_type_text),
        ]
        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        expected = [('image', 'https://i.imgur.com/zjjcJKZ.png'), ('another', 'https://i.imgur.com/dfsdkjfd.png')]
        self.assertEqual(expected, converter.extract_markdown_images(text))

    def test_extract_markdown_images_with_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected = []
        self.assertEqual(expected, converter.extract_markdown_images(text))

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertEqual(expected, converter.extract_markdown_links(text))

    def test_extract_markdown_links_with_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        expected = []
        self.assertEqual(expected, converter.extract_markdown_links(text))

    def test_extract_images_and_links_with_empty_str(self):
        text_empty = ''
        text_none = None
        self.assertEqual([], converter.extract_markdown_images(text_empty))
        self.assertEqual([], converter.extract_markdown_links(text_empty))
        self.assertEqual([], converter.extract_markdown_images(text_none))
        self.assertEqual([], converter.extract_markdown_links(text_none))

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = converter.split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_nodes_image_at_start_and_end(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) This is text with an and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = converter.split_nodes_image([node])
        expected = [
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" This is text with an and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertEqual(expected, new_nodes)
        
    def test_split_nodes_image_two_in_a_row(self):
        node = TextNode(
            "Start ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png) End",
            text_type_text,
        )
        new_nodes = converter.split_nodes_image([node])
        expected = [
            TextNode("Start ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(
                "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode(" End", text_type_text),
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = converter.split_nodes_link([node])
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("link", text_type_link, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second link", text_type_link, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertEqual(expected, new_nodes)
if __name__ == "__main__":
    unittest.main()
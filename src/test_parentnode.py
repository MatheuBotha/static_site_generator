import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestHtmlNode(unittest.TestCase):
    def test_parent_node_nesting_leaf_nodes(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        node.to_html()

        expected_html = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'

        self.assertEqual(node.to_html(), expected_html)

    def test_parent_node_nesting_parent_nodes(self):
        inner_parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        outer_parent = ParentNode(
            'div',
            [
                inner_parent,
                inner_parent
            ],
        )

        print(outer_parent.to_html())
        expected = '<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>'
        self.assertEqual(outer_parent.to_html(), expected)

    def test_parent_node_with_props(self):
        inner_parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text", {'style': 'font-size: 40px;'}),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {
                'style': 'background-color:red;'
            },
        )

        outer_parent = ParentNode(
            'div',
            [
                inner_parent,
                inner_parent
            ],
            {'style': 'text-align: center;'},
        )

        expected = '<div style="text-align: center;"><p style="background-color:red;"><b style="font-size: 40px;">Bold text</b>Normal text<i>italic text</i>Normal text</p><p style="background-color:red;"><b style="font-size: 40px;">Bold text</b>Normal text<i>italic text</i>Normal text</p></div>'
        self.assertEqual(outer_parent.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
import unittest

from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node_p = LeafNode("p", "This is a paragraph of text.")
        node_a = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node_none = LeafNode(None, 'val')

        node_p_expected = '<p>This is a paragraph of text.</p>'
        node_a_expected = '<a href="https://www.google.com">Click me!</a>'
        node_none_expected = 'val'

        self.assertEqual(node_p.to_html(), node_p_expected)
        self.assertEqual(node_a.to_html(), node_a_expected)
        self.assertEqual(node_none.to_html(), node_none_expected)


if __name__ == "__main__":
    unittest.main()
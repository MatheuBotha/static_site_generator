import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", "url")
        node2 = TextNode("This is a text node", "bold", "url")
        self.assertEqual(node, node2)

    def test_eq_with_none_vals(self):
        node = TextNode(None, None, None)
        node2 = TextNode(None, None, None)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold", "url")
        node2 = TextNode("This is not a text node", "bold", "url")
        self.assertNotEqual(node, node2)

    def test_not_eq_with_none_vals(self):
        node = TextNode("This is a text node", "bold", "url")
        node2 = TextNode(None, None, None)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
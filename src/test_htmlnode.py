import unittest

from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_print(self):
        node = HtmlNode('MyTag', 'MyValue', [], {})
        node_as_string = f'{node}'
        expected_result = f'''<HTML Node>
self.tag='MyTag'
self.value='MyValue'
self.children=[]
self.props={{}}
'''
        self.assertEqual(node_as_string, expected_result)

    def test_props_to_html(self):
        node = HtmlNode('', '', [], {'a': 'b', 'x': 'y'})
        props_as_html = node.props_to_html()
        expected_props_as_html = ' a="b" x="y"'
        self.assertEqual(props_as_html, expected_props_as_html)

    def test_props_to_html_none_props(self):
        node = HtmlNode()
        self.assertEqual('', node.props_to_html())

if __name__ == "__main__":
    unittest.main()
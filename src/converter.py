import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)
from leafnode import LeafNode

text_type_to_leaf_tag = {
    "text": None,
    "bold": "b",
    "italic": "i",
    "code": "code",
    "link": "a",
    "image": "img",
}

def text_node_to_html_node(text_node):
    if text_node.text_type not in text_type_to_leaf_tag:
        raise ValueError('No html tag for this text node type')
    tag = text_type_to_leaf_tag[text_node.text_type]
    value = text_node.text
    props = None
    if tag == 'a':
        props = {'href': text_node.url}
    if tag == 'img':
        value = ''
        props = {'src': text_node.url, 'alt': text_node.text}
    return LeafNode(tag, value, props)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        for idx, token in enumerate(old_node.text.split(delimiter)):
            if token:
                if (idx + 1) % 2 == 0:
                    new_nodes.append(TextNode(token, text_type))
                else:
                    new_nodes.append(TextNode(token, text_type_text))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
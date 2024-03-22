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
    if text:
        return re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return []

def extract_markdown_links(text):
    if text:
        return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return []

def split_nodes_image(old_nodes):
    result = []
    for old_node in old_nodes:
        old_node_text = old_node.text
        extracted_images = extract_markdown_images(old_node.text)
        for idx, extracted_image in enumerate(extracted_images):
            new_nodes = old_node_text.split(f"![{extracted_image[0]}]({extracted_image[1]})", 1)
            if new_nodes[0]:
                prefix_node = TextNode(new_nodes[0], text_type_text)
                result.append(prefix_node)
            image_node = TextNode(extracted_image[0], text_type_image, extracted_image[1])
            result.append(image_node)
            if idx+1 == len(extracted_images):
                if new_nodes[1]:
                    postfix_node = TextNode(new_nodes[1], text_type_text)
                    result.append(postfix_node)
            else:
                old_node_text = new_nodes[1]
    return result

def split_nodes_link(old_nodes):
    result = []
    for old_node in old_nodes:
        old_node_text = old_node.text
        extracted_links = extract_markdown_links(old_node.text)
        for idx, extracted_link in enumerate(extracted_links):
            new_nodes = old_node_text.split(f"[{extracted_link[0]}]({extracted_link[1]})", 1)
            if new_nodes[0]:
                prefix_node = TextNode(new_nodes[0], text_type_text)
                result.append(prefix_node)
            image_node = TextNode(extracted_link[0], text_type_link, extracted_link[1])
            result.append(image_node)
            if idx+1 == len(extracted_links):
                if new_nodes[1]:
                    postfix_node = TextNode(new_nodes[1], text_type_text)
                    result.append(postfix_node)
            else:
                old_node_text = new_nodes[1]
    return result
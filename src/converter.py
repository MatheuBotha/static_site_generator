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
from parentnode import ParentNode

text_type_to_leaf_tag = {
    "text": None,
    "bold": "b",
    "italic": "i",
    "code": "code",
    "link": "a",
    "image": "img",
}

block_types = {
    "paragraph": "",
    "heading": "#",
    "code": "```",
    "quote": ">",
    "unordered_list": "-",
    "ordered_list": "1.",
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
                    new_nodes.append(TextNode(token, old_node.text_type))
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
        if not extracted_images:
            result.append(old_node)
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
        if not extracted_links:
            result.append(old_node)
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

def text_to_textnodes(text):
    result = [TextNode(text, text_type_text)]
    text_types_delimiter_map = {
        text_type_bold: '**',
        text_type_italic: '*',
        text_type_code: '`',
    }
    for text_type, delimiter in text_types_delimiter_map.items():
        result = split_nodes_delimiter(result, delimiter, text_type)
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    return result

def markdown_to_blocks(markdown):
    if not markdown:
        return []
    result = []
    markdown_blocks = markdown.split('\n\n')
    for block in markdown_blocks:
        result.append(TextNode(block.strip(), None, None))
    return result

def block_to_block_type(block):
    for block_type in block_types.items():
        if block_type[1] != "":
            if block.text.startswith(block_type[1]):
                return block_type
    return ("paragraph", block_types["paragraph"])

def markdown_to_html_node(markdown):
    top_block = ParentNode(tag="div", children=[])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        top_block.children.append(html_node_from_text_node(block))
    return top_block

def html_node_from_text_node(block):
    block_type = block_to_block_type(block)
    if block_type[0] == "paragraph":
        return paragraph_from_text_node(block)
    if block_type[0] == "heading":
        return heading_from_text_node(block)
    if block_type[0] == "code":
        return code_from_text_node(block)
    if block_type[0] == "quote":
        return quote_from_text_node(block)
    if block_type[0] == "unordered_list":
        return unordered_list_from_text_node(block)
    if block_type[0] == "ordered_list":
        return ordered_list_from_text_node(block)
    return LeafNode('br')

def text_to_html_nodes(text):
    result = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        result.append(text_node_to_html_node(text_node))
    return result

def paragraph_from_text_node(block):
    para = ParentNode("p", [])
    para.children = text_to_html_nodes(block.text)
    return para

def heading_from_text_node(block):
    heading = None    
    if block.text.startswith("# "):
        heading = ParentNode("h1", [])
        block.text = block.text.lstrip("# ")
    if block.text.startswith("## "):
        heading = ParentNode("h2", [])
        block.text = block.text.lstrip("## ")
    if block.text.startswith("### "):
        heading = ParentNode("h3", [])
        block.text = block.text.lstrip("### ")
    if block.text.startswith("#### "):
        heading = ParentNode("h4", [])
        block.text = block.text.lstrip("#### ")
    if block.text.startswith("##### "):
        heading = ParentNode("h5", [])
        block.text = block.text.lstrip("##### ")
    if block.text.startswith("###### "):
        heading = ParentNode("h6", [])
        block.text = block.text.lstrip("###### ")
    heading.children = text_to_html_nodes(block.text)
    return heading

def code_from_text_node(block):
    code_html_node = ParentNode("code", [])
    code_html_node.children = text_to_html_nodes(block.text.replace("```", "").strip())
    return code_html_node

def quote_from_text_node(block):
    quote_html_node = ParentNode("blockquote", [])
    quote_html_node.children = text_to_html_nodes(block.text.replace("> ", "").strip())
    return quote_html_node

def unordered_list_from_text_node(block):
    unordered_list = ParentNode("ul", children=[])
    for item_text in block.text.split("- "):
        if item_text.strip():
            item_text = item_text.strip()
            item = ParentNode("li", children=[])
            item.children = text_to_html_nodes(item_text)
            unordered_list.children.append(item)
    return unordered_list

def ordered_list_from_text_node(block):
    ordered_list = ParentNode("ol", children=[])
    for item_text in block.text.split("\n"):
        item_text = item_text.split(".", 1)[1].strip()
        item = ParentNode("li", children=[])
        item.children = text_to_html_nodes(item_text)
        ordered_list.children.append(item)
    return ordered_list

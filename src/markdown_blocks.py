from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    splitted = markdown.split("\n\n")
    stripped = []
    for text in splitted:
        text = text.strip()
        if text:
            stripped.append(text)
    return stripped


def block_to_block_type(md_block):
    if md_block == "":
        return BlockType.PARAGRAPH
    lines = md_block.split("\n")
    lines = [line.lstrip() for line in lines]
    if (
        lines[0].startswith("# ")
        or lines[0].startswith("## ")
        or lines[0].startswith("### ")
        or lines[0].startswith("#### ")
        or lines[0].startswith("##### ")
        or lines[0].startswith("###### ")
    ):
        return BlockType.HEADING
    elif md_block.startswith("```") and md_block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    elif all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                children.append(heading_helper(block))
            case BlockType.CODE:
                children.append(code_helper(block))
            case BlockType.QUOTE:
                children.append(quote_helper(block))
            case BlockType.ULIST:
                children.append(unordered_list_helper(block))
            case BlockType.OLIST:
                children.append(ordered_list_helper(block))
            case _:
                paragraph_html_node = paragraph_helper(block)
                children.append(paragraph_html_node)

    return ParentNode("div", children)


def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_helper(block):
    lines = block.split("\n")
    clean_lines = [line.strip() for line in lines if line.strip() != ""]
    text = " ".join(clean_lines)
    paragraph_children = text_to_children(text)
    paragraph_html_node = ParentNode("p", paragraph_children)
    return paragraph_html_node


def heading_helper(block):
    prefix, text = block.split(" ", 1)
    heading_children = text_to_children(text)
    return ParentNode(f"h{len(prefix)}", heading_children)


def code_helper(block):
    lines = block.split("\n")
    inner_lines = lines[1:-1]
    clean_lines = [line.lstrip() for line in inner_lines]
    inner_text = "\n".join(clean_lines) + "\n"
    code_text_node = TextNode(inner_text, TextType.CODE)
    code_html_node = text_node_to_html_node(code_text_node)
    c_w_pre_html_node = ParentNode("pre", [code_html_node])  # code with "pre" tag
    return c_w_pre_html_node


def quote_helper(block):
    lines = block.split("\n")
    clean_lines = []
    for line in lines:
        line = line.lstrip()
        if line.startswith(">"):
            line = line[1:].lstrip()
        clean_lines.append(line)
    text = "\n".join(clean_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def unordered_list_helper(block):
    lines = block.split("\n")
    item_nodes = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        text = line[2:]
        ul_children = text_to_children(text)
        item_node = ParentNode("li", ul_children)
        item_nodes.append(item_node)
    return ParentNode("ul", item_nodes)


def ordered_list_helper(block):
    lines = block.split("\n")
    item_nodes = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        text = line.split(". ", 1)[1]
        ol_children = text_to_children(text)
        item_node = ParentNode("li", ol_children)
        item_nodes.append(item_node)
    return ParentNode("ol", item_nodes)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        line = line.lstrip()
        if line.startswith("# "):
            return line[1:].strip()
    raise Exception("no line starts with heading")

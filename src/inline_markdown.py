import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            if delimiter not in node.text:
                new_nodes.append(node)
                continue

            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("unmatched delimiter")
            for i, part in enumerate(parts):
                if part == "":
                    continue
                if i % 2 == 0:
                    text_node = TextNode(part, TextType.TEXT)
                    new_nodes.append(text_node)
                else:
                    text_node = TextNode(part, text_type)
                    new_nodes.append(text_node)

        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)
            current_text = node.text

            if not images:
                new_nodes.append(node)
                continue
            current_text = node.text
            for image_alt, image_url in images:
                markdown = f"![{image_alt}]({image_url})"
                sections = current_text.split(markdown, 1)
                before = sections[0]
                after = sections[1]

                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))

                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
                current_text = after

            if current_text:
                new_nodes.append(TextNode(current_text, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            urls = extract_markdown_links(node.text)
            current_text = node.text

            if not urls:
                new_nodes.append(node)
                continue
            current_text = node.text
            for url_text, url in urls:
                markdown = f"[{url_text}]({url})"
                sections = current_text.split(markdown, 1)
                before = sections[0]
                after = sections[1]

                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))

                new_nodes.append(TextNode(url_text, TextType.LINK, url))
                current_text = after

            if current_text:
                new_nodes.append(TextNode(current_text, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

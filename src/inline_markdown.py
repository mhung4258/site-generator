import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"There are not enough delimiters {delimiter}")
        
        for i in range(len(parts)):
            if not parts[i]:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], old_node.text_type))  # Preserve original type
            else: 
                new_nodes.append(TextNode(parts[i], text_type))  
    return new_nodes

#splits nodes that are images
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        images = extract_markdown_images(text)

        delimited_text = text
        for alt_text, url in images:
            #splits the text using the seperate text, url as the delimiter
            parts = delimited_text.split(f"![{alt_text}]({url})", 1)
            
            #if there exists a text before the delimiter add it before image
            if parts[0]:
                new_nodes.append(TextNode(parts[0], old_node.text_type))

            #add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            #change the text to the next section if there is more
            delimited_text = parts[1] if len(parts) > 1 else ""

        if delimited_text:
            new_nodes.append(TextNode(delimited_text, old_node.text_type))

    return new_nodes

#splits nodes that are links
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        link = extract_markdown_links(text)

        delimited_text = text
        for anchor, url in link:

            parts = delimited_text.split(f"[{anchor}]({url})", 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], old_node.text_type))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            delimited_text = parts[1] if len(parts) > 1 else ""
        
        if delimited_text:
            new_nodes.append(TextNode(delimited_text, old_node.text_type))
    
    return new_nodes
#Takes raw markdown texts and return a list of tuples
def extract_markdown_images(text):
    return re.findall((r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"),text)

def extract_markdown_links(text):
    return re.findall((r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"),text)


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes =  split_nodes_delimiter(nodes,"**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,'_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)

    return nodes

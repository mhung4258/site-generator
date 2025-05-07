from enum import Enum
from htmlnode import *
from textnode import *
from inline_markdown import *


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "ulist"
    OLIST = "olist"


def markdown_to_blocks(markdown):
    separated  = markdown.split("\n\n")
    text = []
    for line in separated:
        stripped_line = line.strip()
        if stripped_line:
            clean = [line.strip() for line in stripped_line.split("\n")]
            text.append('\n'.join(clean))
    
    return text

def block_to_block_type(block):
    lines = block.split("\n")
    
    #check Heading
    if len(lines) == 1 and re.match(r'^#{1,6}\s', block):
        return BlockType.HEADING
    
    #check Code
    if len(lines) >= 2 and lines[0] == '```' and lines[-1] == '```':
        return BlockType.CODE

    #check quote
    if lines and all(line.strip().startswith(">") for line in lines):
        return BlockType.QUOTE
    
    #check UL
    if lines and all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    
    #Check OL
    
    if lines:
        is_ordered = True
        for i, line in enumerate(lines, start=1):
            if not re.fullmatch(rf"^{i}\.\s.+", line):
                is_ordered = False
                break
        if is_ordered:
            return BlockType.OLIST
    
    return BlockType.PARAGRAPH
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    div_children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            #Headings <h1>to <h6>
            heading_hash = len(block.split(" ")[0])
            content = ' '.join(block.split(" ")[1:])
            children = text_to_children(content)
            p_node =  ParentNode(f'h{heading_hash}', children)
            div_children.append(p_node)

        elif block_type == BlockType.CODE:
            lines = block.split('\n')
            if len(lines) >= 3 and lines[0].strip() == '```' and lines[-1].strip() == '```':
                content = '\n'.join(lines[1:-1]) + '\n'
                code_node = LeafNode("code", content)
                pre_node = ParentNode("pre", [code_node])
                div_children.append(pre_node)
            else:
                children = text_to_children(block)
                p_node = ParentNode("p", children)
                div_children.append(p_node)

        elif block_type == BlockType.QUOTE:

            lines = [line.lstrip('>').strip() for line in block.split('\n')]
            content = " ".join(lines)
            children = text_to_children(content)
            quote_node = ParentNode("blockquote", children)
            div_children.append(quote_node)


        elif block_type == BlockType.ULIST:
            items = block.split("\n")
            html_items = []
            for item in items:
                text = item[2:]
                children = text_to_children(text)
                html_items.append(ParentNode("li", children))
            div_children.append(ParentNode("ul", html_items)) 

        elif block_type == BlockType.OLIST:
            items = block.split("\n")
            html_items = []
            for item in items:
                text = item[3:]
                children = text_to_children(text)
                html_items.append(ParentNode("li", children))
            div_children.append(ParentNode("ol", html_items)) 

        else: 
            #Paragraph <p>content</p>
            content = block.replace("\n", " ")
            children = text_to_children(content)
            p_node =  ParentNode('p', children)
            div_children.append(p_node)
        
    return ParentNode("div", div_children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def extract_title(markdown):
    title = ''
    # for block in markdown_to_blocks(markdown):
    #     if block.split(" ")[0] == '#':
    #         title = " ".join(block.split(" ")[1:]).lstrip()

    for block in markdown_to_blocks(markdown):
        if block_to_block_type(block) == BlockType.HEADING and block.split(" ")[0] == '#':
            title = (" ".join(block.split(" ")[1:])).lstrip()

    if title == '':
        raise Exception("Non-valid Title")
    return title

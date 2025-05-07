class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""   
        prop_string = ''
        for key, value in self.props.items():
            prop_string += f' {key}="{value}"'
        return prop_string  
        
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})'        


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value is missing")
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>" 


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag,None,children,props)
    
    def to_html(self):
        if self.tag is None: 
            return ValueError("html tag is missing")
        if self.children is None:
            return ValueError("children is missing")
    
        open_tag = f"<{self.tag}{self.props_to_html()}>"
        close_tag = f"</{self.tag}>"

        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        return f"{open_tag}{children_html}{close_tag}"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"




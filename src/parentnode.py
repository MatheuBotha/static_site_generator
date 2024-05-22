from htmlnode import HtmlNode

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None) -> None:
        if not tag:
            raise ValueError('A parent node must have a tag')
        if children == None:
            raise ValueError('A parent node must have children')
        super().__init__(tag, None, children, props)

    def to_html(self):
        html = f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
            html += child.to_html()
        html += f'</{self.tag}>'
        return html
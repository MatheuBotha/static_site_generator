class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ''
        result = ''
        for key, val in self.props.items():
            result += f' {key}="{val}"'
        return result
    
    def __repr__(self):
        return f'''<HTML Node>
{self.tag=}
{self.value=}
{self.children=}
{self.props=}
'''
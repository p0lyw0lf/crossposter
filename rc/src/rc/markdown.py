from mistletoe import block_token, span_token
from mistletoe.base_renderer import BaseRenderer

class DescriptionRenderer(BaseRenderer):
    limit = 140
    def render_document(self, token: block_token.Document) -> str:
        s = ""
        if token.children is None:
            return s
        for child in token.children:
            try:
                s += self.render(child)
            except:
                # error rendering child (hline?), just continue
                pass
            if len(s) >= self.limit:
                return s[:self.limit-3] + "..."
        return s

    def render_paragraph(self, token: block_token.Paragraph) -> str:
        return self.render_inner(token) + " "

    def render_image(self, token: span_token.Image) -> str:
        return token.title

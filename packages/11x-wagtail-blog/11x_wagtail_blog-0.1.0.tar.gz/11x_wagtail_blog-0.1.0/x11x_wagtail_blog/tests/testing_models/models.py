from wagtail.blocks import TextBlock
from wagtail.fields import StreamField

from x11x_wagtail_blog.models import ExtensibleArticlePage


class TestingArticlePage(ExtensibleArticlePage):
    body = StreamField([
        ("text", TextBlock())
    ], use_json_field=True)

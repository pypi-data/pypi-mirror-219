from django.conf import settings
from django.db import models
from django.utils import timezone
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField, RichTextField
from wagtail.models import Page
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.models import register_snippet

_RICH_TEXT_SUMMARY_FEATURES = getattr(settings, "X11X_WAGTAIL_BLOG_SUMMARY_FEATURES", ["bold", "italic", "code", "superscript", "subscript", "strikethrough"])


@register_snippet
class AboutTheAuthor(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        editable=True,
        blank=False,
        related_name="about_the_author_snippets",
    )
    body = RichTextField()

    panels = [
        FieldPanel("author"),
        FieldPanel("body"),
    ]

    def __str__(self):
        return str(self.author)


class RelatedArticles(models.Model):
    related_to = ParentalKey("ExtensibleArticlePage", verbose_name="Article", related_name="related_article_to")
    related_from = ParentalKey("ExtensibleArticlePage", verbose_name="Article", related_name="related_article_from")


class ExtensibleArticlePage(Page):
    date = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=True)
    summary = RichTextField(features=_RICH_TEXT_SUMMARY_FEATURES, default="", blank=True, null=False)
    title_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.RESTRICT,
        related_name="+",
        null=True,
        blank=True,
    )

    authors = StreamField(
        [
            ("about_the_authors", SnippetChooserBlock(AboutTheAuthor)),
        ],
        default=list,
        use_json_field=True,
        blank=True,
    )

    is_creatable = False

    settings_panels = Page.settings_panels + [
        FieldPanel("date"),
        FieldPanel("owner"),
    ]

    pre_body_content_panels = Page.content_panels + [
        FieldPanel("title_image"),
        FieldPanel("summary"),
    ]
    post_body_content_panels = [
        FieldPanel("authors"),
        InlinePanel(
            "related_article_from",
            label="Related Articles",
            panels=[FieldPanel("related_to")]
        )
    ]

    def has_authors(self):
        return len(self.authors) > 0

    @classmethod
    def with_body_panels(cls, panels):
        return cls.pre_body_content_panels + panels + cls.post_body_content_panels

    def get_template(self, request, *args, **kwargs):
        return getattr(settings, "X11X_WAGTAIL_BLOG_ARTICLE_TEMPLATE", "x11x_wagtail_blog/article_page.html")

    def has_related_articles(self):
        return self.related_article_from.all().count() > 0

    @property
    def related_articles(self):
        return [to.related_to for to in self.related_article_from.all()]

    @related_articles.setter
    def related_articles(self, value):
        """
        An iterable of all articles related to this one.
        """
        self.related_article_from = [
            RelatedArticles(
                related_from=self,
                related_to=v
            ) for v in value
        ]

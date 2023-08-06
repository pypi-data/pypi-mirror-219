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
    """
    A snippet holding the content of an 'About the Author' section for particular authors.

    These snippets are intended to be organized by the various authors of a website. Individual users
    may have several 'about' blurbs that they can choose depending on what a particular article calls
    for.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        editable=True,
        blank=False,
        related_name="about_the_author_snippets",
    )
    "A reference to the author this snippet is about."

    body = RichTextField()
    "A paragraph or two describing the associated author."

    panels = [
        FieldPanel("author"),
        FieldPanel("body"),
    ]

    def __str__(self):
        return str(self.author)


class RelatedArticles(models.Model):
    """
    You should never have to instantiate ``RelatedArticles`` directly. This is a
    model to implement the m2m relationship between articles.
    """
    related_to = ParentalKey("ExtensibleArticlePage", verbose_name="Article", related_name="related_article_to")
    related_from = ParentalKey("ExtensibleArticlePage", verbose_name="Article", related_name="related_article_from")


class ExtensibleArticlePage(Page):
    """
    `ExtensibleArticlePage` is the base class for blog articles. Inherit from `ExtensibleArticlePage` when
    and add your own ``body`` element. `ExtensibleArticlePage` are NOT creatable through the wagtail admin.
    """
    date = models.DateTimeField(default=timezone.now, null=False, blank=False, editable=True)
    "Date to appear in the article subheading."

    summary = RichTextField(features=_RICH_TEXT_SUMMARY_FEATURES, default="", blank=True, null=False)
    "The article's summary. `summary` will show up in index pages."

    title_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.RESTRICT,
        related_name="+",
        null=True,
        blank=True,
    )
    "The image to use in the title header or section of the article."

    authors = StreamField(
        [
            ("about_the_authors", SnippetChooserBlock(AboutTheAuthor)),
        ],
        default=list,
        use_json_field=True,
        blank=True,
    )
    "About the author sections to include with the article.."

    is_creatable = False

    settings_panels = Page.settings_panels + [
        FieldPanel("date"),
        FieldPanel("owner"),
    ]

    pre_body_content_panels = Page.content_panels + [
        FieldPanel("title_image"),
        FieldPanel("summary"),
    ]
    "Admin `FieldPanels` intended to be displayed BEFORE a ``body`` field."

    post_body_content_panels = [
        FieldPanel("authors"),
        InlinePanel(
            "related_article_from",
            label="Related Articles",
            panels=[FieldPanel("related_to")]
        )
    ]
    "Admin `FieldPanel` s intended to be displayed AFTER a ``body`` field."

    def has_authors(self):
        """
        Returns ``True`` if this article has one or more 'about the authors' snippet. ``False`` otherwise.
        """
        return len(self.authors) > 0

    @classmethod
    def with_body_panels(cls, panels):
        """
        A helper method that concatenates all the admin panels of this class with the admin panels intended to enter content
        of the main body.

        :param panels: Panels intended to show up under the "Title" and "Summary" sections, but before
            the 'trailing' sections.
        """
        return cls.pre_body_content_panels + panels + cls.post_body_content_panels

    def get_template(self, request, *args, **kwargs):
        """
        Returns the default template. This method will likely be removed in the (very) near future.

        This method may be overridden (like all wagtail pages) to return the intended template.

        :deprecated:
        """
        return getattr(settings, "X11X_WAGTAIL_BLOG_ARTICLE_TEMPLATE", "x11x_wagtail_blog/article_page.html")

    def has_related_articles(self):
        """
        Returns `True` if this page has related articles associated with it. Returns ``False`` otherwise.
        """
        return self.related_article_from.all().count() > 0

    @property
    def related_articles(self):
        """
        An iterable of related articles related to this one.
        """
        return [to.related_to for to in self.related_article_from.all()]

    @related_articles.setter
    def related_articles(self, value):
        """
        Sets the articles related to this one.

        :param list[ExtensibleArticlePage] value: A list of related articles.
        """
        self.related_article_from = [
            RelatedArticles(
                related_from=self,
                related_to=v
            ) for v in value
        ]

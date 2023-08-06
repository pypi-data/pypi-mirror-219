"""
11x Wagtail Blog
================

``11x-wagtail-blog`` is a wagtail app implementing basic blog features for a wagtail site. This project started as an
implementation of the blogging features of ``11x.engineering``, but since it is intended to be used as the first series
of articles, it has been open sourced and published here. It is intended to demonstrate how to develop a fully featured
package published to PyPI.


Quick Start
===========

To install::

    pip install 11x-wagtail-blog

Add ``x11x_wagtail_blog`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        ...,
        'x11x_wagtail_blog',
        ...,
    ]

Since this package only gives you the common features of every blogging application, you will need to define your own page
models and derive them from `ExtensibleArticlePage`::

>>> from x11x_wagtail_blog.models import ExtensibleArticlePage
>>> from wagtail.admin.panels import FieldPanel
>>> from wagtail.blocks import TextBlock
>>> from wagtail.fields import StreamField

>>> class MyArticlePage(ExtensibleArticlePage):
...     body = StreamField([
...         ("text", TextBlock()),
...     ], use_json_field=True)
...
...     content_panels = ExtensibleArticlePage.with_body_panels([
...         FieldPanel("body"),
...     ])

This can be done in any valid Wagtail app.

Next, generate your migrations as usual::

    python manage.py makemigrations
    python manage.py migrate

You will have to define a template. The default template used is ``x11x_wagtail_blog/article_page.html``, but you should
override the ``get_template()`` method to return your own template.

The fields available on every blog page can be found in :class:`x11x_wagtail_blog.models.ExtensibleArticlePage`.

.. code-block:: html

    <!DOCTYPE html>
    <html>
      <head>...</head>
      <body>
        <h1>{{ self.title }}</h1>

        {% include_block self.body %}

        <h2>About the authors</h2>
        {% for author in self.authors %}
        {% include "myblog/about_the_author_section.html" with author=author.value %}
        {% endfor %}

        <h2>Related Articles</h2>
        <ul>
        {% for article in self.related_articles %}
        <li><a href="{% pageurl article %}">{{ article.title }}</a></li>
        {% endfor %}
        </ul>
      </body>
    </html>
"""

__version__ = "0.2.0"

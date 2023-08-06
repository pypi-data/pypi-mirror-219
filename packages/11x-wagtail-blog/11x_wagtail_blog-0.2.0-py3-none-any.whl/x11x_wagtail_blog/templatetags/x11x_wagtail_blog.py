from django import template
from django.core.exceptions import ObjectDoesNotExist

from x11x_wagtail_blog.models import AboutTheAuthor

register = template.Library()


@register.inclusion_tag("x11x_wagtail_blog/about_the_author.html")
def about_the_author(snippet: AboutTheAuthor, *, heading="h4"):
    # Deprecated, do not use.
    try:
        avatar = snippet.author.wagtail_userprofile.avatar
    except ObjectDoesNotExist:
        avatar = None

    return {
        "author_full_name": snippet.author.first_name + " " + snippet.author.last_name,
        "body": snippet.body,
        "avatar": avatar,
        "heading": heading,
    }

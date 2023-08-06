11x Wagtail Blog
================

{% for badge in badges %}{{ badge.as_rst_declaration() }} {% endfor %}

{{ x11x_wagtail_blog.__doc__}}

{% for badge in badges -%}
{{ badge.as_rst_definition() }}
{% endfor %}

from django import template

register = template.Library()

@register.inclusion_tag("network/components/feed.html")
def feed(posts, pagination):
  return { "posts": posts, "pagination": pagination }
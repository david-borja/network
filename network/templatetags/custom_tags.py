from django import template

register = template.Library()

@register.inclusion_tag("network/components/feed.html")
def feed(posts):
  return { "posts": posts }
from django import template

from twitter.models import Comment

register = template.Library()


@register.filter(name='count_comments')
def count_comments(tweet):
    comments = Comment.objects.filter(tweet_id=tweet.id)
    return len(comments)

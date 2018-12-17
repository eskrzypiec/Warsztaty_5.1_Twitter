from django.contrib import admin
from .models import *


# Register your models here.

def short_content(text):
    return str(text.content)[0:50]


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ["id", short_content, "user", "creation_date"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "sent_date", "sent_from", "sent_to", short_content, "read"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "creation_date", "tweet", "user", short_content]



from django import forms

from twitter.models import *


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class SendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'sent_to']


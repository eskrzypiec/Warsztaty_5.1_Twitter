from django.contrib.auth.models import User
from django.db import models


class Tweet(models.Model):
    content = models.CharField(max_length=140)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}: {self.content[0:50]}"


class Message(models.Model):
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_to")
    sent_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_from")
    read = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"Do: {self.sent_to}, Od: {self.sent_from}, Treść: {self.content[0:30]}"


class Comment(models.Model):
    content = models.CharField(max_length=60)
    creation_date = models.DateTimeField(auto_now_add=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"Od: {self.user}, Treść: {self.content[0:30]}"

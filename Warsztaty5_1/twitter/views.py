from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth import views as auth_views

from twitter.forms import AddCommentForm, SendMessageForm
from twitter.models import *


class MainView(LoginRequiredMixin, View):
    def get(self, request):
        tweets = Tweet.objects.filter(blocked=False)
        return render(request, "twitter/content_page.html", locals())


class AddTweetView(LoginRequiredMixin, CreateView):
    model = Tweet
    fields = ['content']
    template_name = 'twitter/add.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        tweet = form.save(commit=False)
        tweet.user = self.request.user
        tweet.save()
        return super(AddTweetView, self).form_valid(form)


class UserTweetView(LoginRequiredMixin, View):
    def get(self, request):
        id_user = request.user.id
        tweets = Tweet.objects.filter(user_id=id_user, blocked=False)
        return render(request, "twitter/content_page.html", locals())


class ShowTweetView(LoginRequiredMixin, View):
    def get(self, request, id_tweet):
        tweet = get_object_or_404(Tweet, id=id_tweet, blocked=False)
        comments = Comment.objects.filter(tweet_id=tweet.id, blocked=False)
        form = AddCommentForm()
        return render(request, "twitter/tweet_details.html", locals())

    def post(self, request, id_tweet):
        tweet = get_object_or_404(Tweet, pk=id_tweet)
        form = AddCommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content')
            comment = Comment(content=content, tweet=tweet, user=request.user, blocked=False)
            comment.save()
            messages.success(request, "Komentarz został dodany poprawnie")
        return redirect("show-tweet", id_tweet=id_tweet)


class UserReceivedMessagesView(LoginRequiredMixin, View):
    def get(self, request):
        id_user = request.user.id
        user_messages = Message.objects.filter(sent_to_id=id_user, blocked=False)
        received = True
        return render(request, "twitter/user_messages.html", locals())


class UserSentMessagesView(LoginRequiredMixin, View):
    def get(self, request):
        id_user = request.user.id
        user_messages = Message.objects.filter(sent_from_id=id_user, blocked=False)
        return render(request, "twitter/user_messages.html", locals())


class MessageDetailView(LoginRequiredMixin, View):
    def get(self, request, id_message):
        message_detail = Message.objects.get(id=id_message)
        message_detail.read = True
        message_detail.save()
        return render(request, "twitter/message_details.html", locals())


class SendMessageView(LoginRequiredMixin, View):
    def get(self, request):
        form = SendMessageForm
        return render(request, "twitter/add.html", locals())

    def post(self, request):
        sent_from = request.user
        form = SendMessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content')
            sent_to = form.cleaned_data.get('sent_to')
            message_sent = Message(content=content, sent_from=sent_from, sent_to=sent_to, blocked=False)
            message_sent.save()
            messages.success(request, "Wiadomość wysłana")
        return redirect("messages-received")


class LoginUserView(auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = "twitter/login.html"


class LogoutUserView(auth_views.LogoutView):
    template_name = 'twitter/logout.html'
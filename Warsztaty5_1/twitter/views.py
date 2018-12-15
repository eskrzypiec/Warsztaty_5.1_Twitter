from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from twitter.models import Tweet


class MainView(View):
    def get(self, request):
        tweets = Tweet.objects.all()
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


class UserTweetView(View):
    def get(self, request, id_user):
        tweets = Tweet.objects.filter(user_id=id_user)
        return render(request, "twitter/content_page.html", locals())


class ShowTweetView(View):
    def get(self, request, id_tweet):
        tweet = get_object_or_404(Tweet, id=id_tweet)
        return render(request, "twitter/tweet_details.html", locals())

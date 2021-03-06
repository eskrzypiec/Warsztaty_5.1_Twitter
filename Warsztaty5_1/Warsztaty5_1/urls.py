"""Warsztaty5_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from twitter.views import *
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main'),
    path('add_tweet/', AddTweetView.as_view(), name='add-tweet'),
    path('user_tweet/', UserTweetView.as_view(), name='user-tweet'),
    path('user_tweets/<int:user_id>/', SingleUserTweetView.as_view(), name='user-tweets'),
    path('tweet/<int:id_tweet>/', ShowTweetView.as_view(), name='show-tweet'),
    path('user_messages_received/', UserReceivedMessagesView.as_view(), name='messages-received'),
    path('user_messages_sent/', UserSentMessagesView.as_view(), name='messages-sent'),
    path('message_detail/<int:id_message>/', MessageDetailView.as_view(), name='message-details'),
    path('send_message/', SendMessageView.as_view(), name='send-message'),
    path('send_message/<int:user_id>', SendMessageToUserView.as_view(), name='send-message-to-user'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('delete_account/<int:pk>', DeleteAccountView.as_view(), name='delete-account'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

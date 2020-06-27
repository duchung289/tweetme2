from django.urls import path

from .views import (
    tweet_detail_view, 
    tweet_list_view, 
    tweet_create_view,
    tweet_delete_view,
    tweet_action_view,
    tweet_feed_view
)
'''
CLIENT
Base ENDPOINT --> /api/tweets/
'''
urlpatterns = [
    path('', tweet_list_view),
    path('action/', tweet_action_view),
    path('feed/', tweet_feed_view),
    path('create/', tweet_create_view),
    path('<str:tweet_id>/', tweet_detail_view),
    path('<str:tweet_id>/delete/', tweet_delete_view)
]

from django.urls import path

from tweets.views import (
    home_view, 
    tweet_detail_view, 
    tweet_list_view, 
    tweet_create_view,
    tweet_delete_view,
    tweet_action_view
)

urlpatterns = [
    path('', tweet_list_view),
    path('action/', tweet_action_view),
    path('create/', tweet_create_view),
    path('<str:tweet_id>/', tweet_detail_view),
    path('<str:tweet_id>/delete/', tweet_delete_view)
]

import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Tweet
from ..forms import TweetForm
from ..serializers import (
    TweetSerializer, 
    TweetActionSerializer, 
    TweetCreateSerializer)
from django.db.migrations import serializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

@api_view(['POST']) #http method that the client send == POST
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        obj = serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status = 404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status = 200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status = 404) # not found
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({'message': 'You can not delete this tweet' }, status = 401) # unauthorized
    obj = qs.first()
    obj.delete()
    return Response({'message': 'Tweet is removed' }, status = 200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, retweet.
    '''
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status = 404) # not found
        obj = qs.first()

        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)

        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)

        elif action == "retweet":
            new_tweet = Tweet.objects.create(
                user=request.user, 
                parent=obj,
                content=content
                )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)

    return Response({}, status = 200)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    username = request.GET.get('username') #?username=hung
    if username != None:
        qs = qs.filter(user__username__iexact=username)
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data)    

def tweet_create_view_pure_django(request, *args, **kwargs):
    '''
    REST API CRUD (CREATE-REVIEW-UPDATE-DELETE) --> DRF Django Rest Framework
    '''
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status = 401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        # will do other form related logic
        obj.user = user
        obj.save()

        if request.is_ajax():
            return JsonResponse(obj.serialize(), status = 201) #201 == created items

        if next_url and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status = 400)

    return render(request, 'components/form.html', context={'form': form})

def tweet_list_view_pure_django(request, *args, **kwargs):
    """
    REST API REVIEW:
    Consume by JavaScript or Swipt/Java/iOS/Android
    return json data
    """
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    """
    REST API REVIEW:
    Consume by JavaScript or Swipt/Java/iOS/Android
    return json data
    """
    data = {
        "id": tweet_id
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found!"
        status = 404

    return JsonResponse(data, status=status) # json.dumps content_type = 'application/json'
    # return HttpResponse(f'<h1>Hello {tweet_id} - {obj.content}!</h1>')

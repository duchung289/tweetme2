import random
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render


from .models import Tweet
from .forms import TweetForm

# Create your views here.

def home_view(request,*args, **kwargs):
    # return HttpResponse('<h1>Hello World!</h1>')
    return render(request,'pages/home.html', context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    print('POST data is:', request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        # will do other form related logic
        obj.save()
    return render(request, 'components/form.html', context={'form': form})

def tweet_list_view(request, *args, **kwargs):
    """
    REST API REVIEW:
    Consume by JavaScript or Swipt/Java/iOS/Android
    return json data
    """
    qs = Tweet.objects.all()
    tweets_list = [{'id': x.id, 'content': x.content, 'likes': random.randint(0,99)} for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view(request, tweet_id, *args, **kwargs):
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


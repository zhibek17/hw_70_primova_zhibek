import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse

from webapp.models import Article


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed(['GET'])


def json_echo_view(request, *args, **kwargs):
    answer = {
        'message': 'Hello World!',
        'method': request.method
    }
    if request.body:
        answer['content'] = json.loads(request.body)
    return JsonResponse(answer)


def article_view(request):
    if request.method == 'GET':
        # articles = Article.objects.all()
        # articles_list = []
        # for article in articles:
        #     articles_list.append({'title': article.title, 'content': article.content})
        articles = Article.objects.values('id', 'title', 'content')
        articles_list = list(articles)
        return JsonResponse(articles_list, safe=False)
    elif request.method == 'POST':
        if request.body:
            data = json.loads(request.body)
            # article = Article.objects.create(title=data['title'], content=data['content'])
            article = Article.objects.create(**data)
            return JsonResponse({'id': article.id})
        else:
            return JsonResponse({'error': 'No data provided'}, status=400)
    return HttpResponseNotAllowed(['GET'])
import json

from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from webapp.models import Article
from api_v2.serializers import ArticleSerializer, ArticleModelSerializer


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


class ArticleView(APIView):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.order_by('-created_at')
        articles_list = ArticleModelSerializer(articles, many=True).data
        return Response(articles_list)

    def post(self, request, *args, **kwargs):
        serializer = ArticleModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ArticleDetailView(APIView):
    def get(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            serializer = ArticleModelSerializer(article)
            return Response(serializer.data)
        except Article.DoesNotExist:
            return Response({'error': 'Статья не найдена'}, status=404)


class ArticleUpdateView(APIView):
    def put(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            serializer = ArticleModelSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(status=400)
        except Article.DoesNotExist:
            return Response({'error': 'Статья не найдена'}, status=404)


class ArticleDeleteView(APIView):
    def delete(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            article.delete()
            return Response({'message': 'Статья удалена'}, status=200)
        except Article.DoesNotExist:
            return Response({'error': 'Статья не найдена'}, status=404)

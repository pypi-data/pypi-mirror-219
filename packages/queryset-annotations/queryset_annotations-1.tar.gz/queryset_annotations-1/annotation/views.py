from django.shortcuts import render

from queryset_annotations.proxy.model import BaseProxyModel
from django.db import models

from annotation.models import Author, Book
from queryset_annotations.base import BaseAnnotation
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet


class BookCountAnnotation(BaseAnnotation):
    name = "book_count"
    output_field = models.IntegerField()

    def get_expression(self):
        return models.Count("books", distinct=True)


class AuthorProxyModel(BaseProxyModel):
    book_count = BookCountAnnotation()

    class Meta:
        model = Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorProxyModel
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class AuthorViewSet(ModelViewSet):
    queryset = AuthorProxyModel.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

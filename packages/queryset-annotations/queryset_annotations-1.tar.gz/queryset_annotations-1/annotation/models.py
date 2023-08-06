from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="books")


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

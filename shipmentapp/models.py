from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="articles")
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    featured_starting = models.DateTimeField()
    featured_ending = models.DateTimeField()

    def __str__(self):
        return self.title
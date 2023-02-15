from django.db import models


class BlogPost(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    public = models.BooleanField(default=True)

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Character(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    race = models.CharField(max_length=100)
    abilities = models.TextField()

    def __str__(self):
        return self.name

class Village(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    leader = models.ForeignKey(Character, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Technique(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name


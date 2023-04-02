from django.db import models

class Studio(models.Model):
    name = models.CharField(max_length=128, unique=True)
    
    def __str__(self):
        return self.name

class Producer(models.Model):
    name = models.CharField(max_length=128, unique=True)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=128, unique=True)
    year = models.IntegerField()
    studios = models.ManyToManyField(Studio)
    producers = models.ManyToManyField(Producer)
    winner = models.BooleanField(default=False)

    def __str__(self):
        return self.title


from django.db import models

class Studio(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name

class Producer(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=128)
    year = models.IntegerField()
    studios = models.ManyToManyField(Studio)
    producers = models.ManyToManyField(Producer)

    def __str__(self):
        return self.title


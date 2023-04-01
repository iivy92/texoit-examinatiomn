from django.contrib import admin
from movie_award.models import Movie, Studio, Producer

class Movies(admin.ModelAdmin):
    list_display = ('id', 'title', 'year')
    list_display_links = ('id', 'title', 'year')
    search_fields = ('id', 'title', 'year')

admin.site.register(Movie, Movies)

class Studios(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')

admin.site.register(Studio, Studios)

class Producers(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')

admin.site.register(Producer, Producers)

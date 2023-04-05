from django.contrib import admin
from movies.models import Movie, Studio, Producer

class Movies(admin.ModelAdmin):
    list_display = ('id', 'title', 'year', 'winner')
    list_display_links = ('id', 'title', 'year', 'winner')
    search_fields = ('id', 'title', 'year', 'winner')

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

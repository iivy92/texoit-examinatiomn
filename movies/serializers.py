from rest_framework import serializers
from .models import Movie, Studio, Producer

class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['id', 'name']

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    studios = StudioSerializer(many=True)
    producers = ProducerSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'studios', 'producers', 'winner']

    def create(self, validated_data):
        studios_data = validated_data.pop('studios')
        producers_data = validated_data.pop('producers')
        movie = Movie.objects.create(**validated_data)
        for studio_data in studios_data:
            studio, _ = Studio.objects.get_or_create(name=studio_data['name'])
            movie.studios.add(studio)
        for producer_data in producers_data:
            producer, _ = Producer.objects.get_or_create(name=producer_data['name'])
            movie.producers.add(producer)
        return movie

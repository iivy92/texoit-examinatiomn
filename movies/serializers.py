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

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.year = validated_data.get('year', instance.year)
        instance.winner = validated_data.get('winner', instance.winner)

        # Update the many-to-many relationships
        updated_studios_data = validated_data.get('studios', [])
        updated_producers_data = validated_data.get('producers', [])

        # Get a list of existing studios/producers IDs
        existing_studio_ids = [studio.id for studio in instance.studios.all()]
        existing_producer_ids = [producer.id for producer in instance.producers.all()]

        # Update existing studios
        for studio_data in updated_studios_data:
            studio_id = studio_data.get('id')
            if studio_id in existing_studio_ids:
                studio = Studio.objects.get(id=studio_id)
                studio.name = studio_data.get('name', studio.name)
                studio.save()
                existing_studio_ids.remove(studio_id)
            else:
                studio = Studio.objects.create(name=studio_data['name'])
                instance.studios.add(studio)

        # Delete studios that were not updated or added
        instance.studios.filter(id__in=existing_studio_ids).delete()

        # Update existing producers
        for producer_data in updated_producers_data:
            producer_id = producer_data.get('id')
            if producer_id in existing_producer_ids:
                producer = Producer.objects.get(id=producer_id)
                producer.name = producer_data.get('name', producer.name)
                producer.save()
                existing_producer_ids.remove(producer_id)
            else:
                producer = Producer.objects.create(name=producer_data['name'])
                instance.producers.add(producer)

        # Delete producers that were not updated or added
        instance.producers.filter(id__in=existing_producer_ids).delete()

        instance.save()

        return instance

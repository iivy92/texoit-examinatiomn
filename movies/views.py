from django.http import JsonResponse
from rest_framework import viewsets, views
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from setup.swagger import producer_prize_response
from .models import Movie, Studio, Producer
from .serializers import MovieSerializer, StudioSerializer, ProducerSerializer

class StudioViewSet(viewsets.ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer

class ProducerViewSet(viewsets.ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ProducerPrizesView(views.APIView):
    
    @swagger_auto_schema(operation_description='Return max and min interval between prizes', responses=producer_prize_response)
    def get(self, request, *args, **kwargs):
        producers = Producer.objects.filter(movie__winner=True).distinct()
        min_interval = 999
        max_interval = 0
        min_winner = []
        max_winner = []
        for producer in producers:
            prizes = producer.movie_set.filter(winner=True).order_by('year')
            previous_win = None
            for prize in prizes:
                if previous_win is not None:
                    interval = prize.year - previous_win.year
                    if interval != 0 and  interval < min_interval:
                        min_interval = interval
                        min_winner = [{
                            "producer": producer.name,
                            "interval": min_interval,
                            "previousWin": previous_win.year,
                            "followingWin": previous_win.year + interval
                        }]
                    elif interval == min_interval:
                        min_winner.append({
                            "producer": producer.name,
                            "interval": interval,
                            "previousWin": previous_win.year,
                            "followingWin": previous_win.year + interval
                        })
                    elif interval > max_interval:
                        max_interval = interval
                        max_winner = [{
                            "producer": producer.name,
                            "interval": max_interval,
                            "previousWin": previous_win.year,
                            "followingWin": previous_win.year + interval
                        }]
                    elif interval == max_interval:
                        max_winner.append({
                            "producer": producer.name,
                            "interval": interval,
                            "previousWin": previous_win.year,
                            "followingWin": previous_win.year + interval
                        })
                previous_win = prize

        response_data = dict(
            min=min_winner,
            max=max_winner
        )
        return JsonResponse(response_data)

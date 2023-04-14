from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework import status


schema_view = get_schema_view(
    openapi.Info(
        title="Python Django API",
        default_version='v1.0.1',
        description="API Python, desenvolvida usando Django REST Framework, tem como objetivo fornecer informações dos indicados e vendedores da categoria Pior Filme do Golden Raspberry Awards.",
        contact=openapi.Contact(email="33p.peu@gmail.com"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

prize_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'producer': openapi.Schema(type=openapi.TYPE_STRING),
        'interval': openapi.Schema(type=openapi.TYPE_INTEGER),
        'previousWin': openapi.Schema(type=openapi.TYPE_INTEGER),
        'followingWin': openapi.Schema(type=openapi.TYPE_INTEGER),
    },
    required=['producer', 'interval', 'previousWin', 'followingWin']
)

producer_prize_response = {
    status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'min': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=prize_schema
            ),
            'max': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=prize_schema
            ),
        },
        required=['min', 'max']
    )
}

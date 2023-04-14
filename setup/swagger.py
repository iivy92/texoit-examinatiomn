from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Python Django API",
        default_version='v1',
        description="API Python, desenvolvida usando Django REST Framework, tem como objetivo fornecer informações dos indicados e vendedores da categoria Pior Filme do Golden Raspberry Awards.",
        contact=openapi.Contact(email="33p.peu@gmail.com"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

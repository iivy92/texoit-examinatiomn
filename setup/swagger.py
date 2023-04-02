from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="API de Filmes",
        default_version='v1',
        description="API para gerenciar filmes",
        contact=openapi.Contact(email="contato@exemplo.com"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

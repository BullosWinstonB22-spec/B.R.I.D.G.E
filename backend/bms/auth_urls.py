from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)

urlpatterns = [
    path("login/", obtain_auth_token, name="api-login"),  # POST {username, password} -> {token}
    path("me/", me, name="api-me"),
]

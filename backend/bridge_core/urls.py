from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def health(request):
    return JsonResponse({"status": "ok", "project": "B.R.I.D.G.E"})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health, name="health"),
    path("api/auth/", include("rest_framework.authtoken.urls") if False else include("bms.auth_urls")),
    path("api/", include("bms.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenRefreshView
from django.views.generic import TemplateView
from django.http import JsonResponse

def api_status(request):
    return JsonResponse({"status": "success", "message": "API is running in the backend!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_status, name='api_root'),
    path('api/status/', api_status, name='api_status'),
    path('auth/', include('accounts.urls')),  # This should be correct
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', api_status, name='home'),
]
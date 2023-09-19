from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from items.consumers import NotificationConsumer

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")), 
    path('items/', include('items.urls')),

]

websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi())
]

# Add this to serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
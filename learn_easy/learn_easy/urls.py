from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from usersApp.views import login_request, login_view
from cards.consumers import UserNotificationConsumer

urlpatterns = [ 
    path("accounts/login/", login_request, name='account_login'),
    path("accounts/signup/", login_request, name='account_signup'),
    path("accounts/login/link/", login_view, name='login_link'),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")), 
    path('cards/', include('cards.urls')),
    path('decks/', include('decks.urls')),
]

websocket_urlpatterns = [
    path("ws/user_card_notifications/", UserNotificationConsumer.as_asgi()),
]

# Add this to serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
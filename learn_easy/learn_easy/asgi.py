import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learn_easy.settings")

django_application = get_asgi_application()
from channels.auth import AuthMiddlewareStack

from . import urls # noqa isort:skip

# ProtocolTypeRouter is routing `"http"` connections to the Django application instantiated by get_asgi and
# "websocket" connections to a URLRouter that uses 
# urls.websocket_urlpatterns to route WebSocket connections to the appropriate consumer.
# `URLRouter` is an application that routes incoming HTTP requests
# to the appropriate consumer based on the URL of the request.
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(urls.websocket_urlpatterns))
    }
)



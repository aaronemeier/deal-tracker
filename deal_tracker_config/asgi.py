import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "deal_tracker"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deal_tracker_config.settings.production")
django_application = get_asgi_application()


async def websocket_application(receive, send):
    while True:
        event = await receive()

        if event["type"] == "websocket.connect":
            await send({"type": "websocket.accept"})

        if event["type"] == "websocket.disconnect":
            break

        if event["type"] == "websocket.receive" and event["text"] == "ping":
            await send({"type": "websocket.send", "text": "pong!"})


async def application(scope, receive, send):
    if scope["type"] == "http":
        await django_application(scope, receive, send)
    elif scope["type"] == "websocket":
        await websocket_application(receive, send)
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")

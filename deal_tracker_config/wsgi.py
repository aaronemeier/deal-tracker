import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "deal_tracker"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deal_tracker_config.settings.production")

application = get_wsgi_application()
application = WhiteNoise(application, root=str(ROOT_DIR / "deal_tracker/static"))

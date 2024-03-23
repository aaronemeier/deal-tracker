import logging

from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

from .models import UserPreference

LOG = logging.getLogger(__name__)


class ThemeMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return response

        profile = getattr(user, "profile", None)
        if profile is None:
            return response

        preference = UserPreference.objects.get(user=user)
        if preference.theme == "DARK":
            request.dark_theme = True
        else:
            request.dark_theme = False

        return self.get_response(request)


class UserLanguageMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return response

        profile = getattr(user, "profile", None)
        if profile is None:
            return response

        preference = UserPreference.objects.get(user=user)
        language: str = preference.language
        translation.activate(language)

        return self.get_response(request)

import threading

_thread_locals = threading.local()

__all__ = ["get_current_language"]


def get_current_language():
    """Get current language usage by interface."""
    return getattr(_thread_locals, "language", "en")


class LanguageMiddleware:
    """Middleware for handling user language usage."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.language = getattr(request, "LANGUAGE_CODE", "en")
        return self.get_response(request)

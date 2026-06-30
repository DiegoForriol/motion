"""Traduce errores de la API de Google Ads a mensajes claros para el usuario."""

from __future__ import annotations

import sys


def print_friendly_error(exc: Exception) -> None:
    """Imprime un mensaje legible para errores comunes de la API de Google
    Ads (GoogleAdsException) sin volcar un traceback completo al usuario."""
    try:
        from google.ads.googleads.errors import GoogleAdsException
    except ImportError:  # pragma: no cover - solo si la librería no está instalada
        print(f"Error: {exc}", file=sys.stderr)
        return

    if isinstance(exc, GoogleAdsException):
        print(
            f"Error de la API de Google Ads (request id: {exc.request_id}):",
            file=sys.stderr,
        )
        for error in exc.failure.errors:
            print(f"  - {error.message}", file=sys.stderr)
            if error.error_code:
                print(f"    Código: {error.error_code}", file=sys.stderr)
        return

    print(f"Error inesperado: {exc}", file=sys.stderr)

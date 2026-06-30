"""Construcción del cliente de la API de Google Ads."""

from __future__ import annotations

from google.ads.googleads.client import GoogleAdsClient

from adstool.config import ConfigError, Settings, fail, load_settings


def get_client_and_customer_id(
    config_file_path: str | None = None,
    customer_id: str | None = None,
) -> tuple[GoogleAdsClient, str]:
    """Carga la configuración y construye un GoogleAdsClient listo para usar.

    Termina el programa con un mensaje claro si falta configuración, en vez
    de dejar que falle con un traceback de autenticación.
    """
    try:
        settings: Settings = load_settings(
            config_file_path=config_file_path, customer_id=customer_id
        )
    except ConfigError as exc:
        fail(str(exc))
        raise  # pragma: no cover - fail() termina el proceso

    client = GoogleAdsClient.load_from_storage(str(settings.config_file_path))
    return client, settings.customer_id

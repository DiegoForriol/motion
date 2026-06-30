"""Carga y validación de configuración (google-ads.yaml + .env)."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml
from dotenv import load_dotenv

REQUIRED_GOOGLE_ADS_FIELDS = (
    "developer_token",
    "client_id",
    "client_secret",
    "refresh_token",
)

SETUP_HELP_URL_SECTION = "la sección 'Configuración' del README.md"


class ConfigError(Exception):
    """Error de configuración con un mensaje pensado para el usuario final."""


@dataclass
class Settings:
    config_file_path: Path
    customer_id: str | None


def load_settings(
    config_file_path: str | None = None,
    customer_id: str | None = None,
    env_file: str | Path = ".env",
) -> Settings:
    """Carga la configuración desde .env y valida que google-ads.yaml exista
    y tenga los campos obligatorios, sin intentar autenticar contra la API."""
    load_dotenv(dotenv_path=env_file, override=False)

    resolved_path = Path(
        config_file_path
        or os.environ.get("GOOGLE_ADS_CONFIGURATION_FILE_PATH", "./google-ads.yaml")
    )
    resolved_customer_id = customer_id or os.environ.get("GOOGLE_ADS_CUSTOMER_ID")

    if not resolved_path.exists():
        raise ConfigError(
            f"No se ha encontrado el archivo de configuración '{resolved_path}'.\n"
            f"Copia 'google-ads.yaml.example' a '{resolved_path}' y rellena tus "
            f"credenciales. Consulta {SETUP_HELP_URL_SECTION} para instrucciones "
            "detalladas sobre cómo obtener el developer token, las credenciales "
            "OAuth2 y el refresh token."
        )

    with resolved_path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    missing = [
        field
        for field in REQUIRED_GOOGLE_ADS_FIELDS
        if not raw.get(field) or str(raw.get(field)).startswith("INSERT_")
    ]
    if missing:
        raise ConfigError(
            f"Faltan campos obligatorios en '{resolved_path}': {', '.join(missing)}.\n"
            f"Consulta {SETUP_HELP_URL_SECTION} para saber cómo obtener cada uno."
        )

    if not resolved_customer_id or resolved_customer_id.startswith("1234567890"):
        raise ConfigError(
            "No se ha indicado el Customer ID de la cuenta de Google Ads.\n"
            "Pásalo con --customer-id o defínelo en .env como "
            "GOOGLE_ADS_CUSTOMER_ID (sin guiones)."
        )

    return Settings(config_file_path=resolved_path, customer_id=resolved_customer_id)


def fail(message: str) -> None:
    """Imprime un error de configuración legible y termina el programa."""
    print(f"Error de configuración: {message}", file=sys.stderr)
    sys.exit(1)

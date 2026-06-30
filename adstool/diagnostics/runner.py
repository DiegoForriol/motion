"""Ejecuta consultas GAQL contra la API de Google Ads."""

from __future__ import annotations

from typing import Any, Iterator

from google.ads.googleads.client import GoogleAdsClient


def run_query(
    client: GoogleAdsClient, customer_id: str, query: str
) -> Iterator[Any]:
    """Ejecuta una consulta GAQL y devuelve un iterador de filas (GoogleAdsRow)."""
    ga_service = client.get_service("GoogleAdsService")
    stream = ga_service.search_stream(customer_id=customer_id, query=query)
    for batch in stream:
        for row in batch.results:
            yield row

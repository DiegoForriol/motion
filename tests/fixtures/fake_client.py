"""Cliente de Google Ads simulado para probar `fixes/*` sin llamar a la API."""

from __future__ import annotations

from types import SimpleNamespace


class AutoNamespace:
    """Objeto que auto-crea atributos anidados al accederlos, imitando la
    ergonomía de los mensajes proto-plus (`operation.create.keyword.text = x`)
    sin necesitar las clases reales generadas por gRPC."""

    def __init__(self):
        object.__setattr__(self, "_data", {})

    def __getattr__(self, name):
        data = object.__getattribute__(self, "_data")
        if name not in data:
            data[name] = AutoNamespace()
        return data[name]

    def __setattr__(self, name, value):
        object.__getattribute__(self, "_data")[name] = value

    def __call__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self


class FakeService:
    def __init__(self):
        self.calls: list[tuple] = []

    def ad_group_path(self, customer_id, ad_group_id):
        return f"customers/{customer_id}/adGroups/{ad_group_id}"

    def ad_group_criterion_path(self, customer_id, ad_group_id, criterion_id):
        return f"customers/{customer_id}/adGroupCriteria/{ad_group_id}~{criterion_id}"

    def mutate_ad_group_criteria(self, customer_id, operations):
        self.calls.append(("mutate_ad_group_criteria", customer_id, operations))
        return SimpleNamespace(results=[SimpleNamespace(resource_name="fake/criterion/1")])

    def mutate_campaign_budgets(self, customer_id, operations):
        self.calls.append(("mutate_campaign_budgets", customer_id, operations))
        return SimpleNamespace(results=[SimpleNamespace(resource_name="fake/budget/1")])

    def mutate_campaigns(self, customer_id, operations):
        self.calls.append(("mutate_campaigns", customer_id, operations))
        return SimpleNamespace(results=[SimpleNamespace(resource_name="fake/campaign/1")])

    def mutate_conversion_actions(self, customer_id, operations):
        self.calls.append(("mutate_conversion_actions", customer_id, operations))
        return SimpleNamespace(results=[SimpleNamespace(resource_name="fake/conversion/1")])


class FakeClient:
    """Sustituto mínimo de GoogleAdsClient para tests de dry-run/apply."""

    def __init__(self):
        self._services: dict[str, FakeService] = {}
        self.enums = AutoNamespace()

    def get_service(self, name: str) -> FakeService:
        if name not in self._services:
            self._services[name] = FakeService()
        return self._services[name]

    def get_type(self, name: str) -> AutoNamespace:
        return AutoNamespace()

    def copy_from(self, dest, src) -> None:
        pass

    @property
    def all_calls(self) -> list[tuple]:
        return [call for service in self._services.values() for call in service.calls]

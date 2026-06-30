# adstool — Diagnóstico y corrección de Google Ads para lockercuenca.es

Herramienta de línea de comandos para diagnosticar por qué una campaña de
Google Ads no genera impresiones, y para aplicar correcciones (palabras
clave, presupuesto, pujas, acciones de conversión) usando la API oficial de
Google Ads.

**Por seguridad, ningún comando modifica la cuenta real a menos que se pase
`--apply` explícitamente, y se pedirá confirmación antes de aplicar cualquier
cambio.**

## 1. Requisitos previos

- Una cuenta de Google Ads con acceso de administrador.
- Un proyecto en Google Cloud Console.
- Python 3.10+.

## 2. Obtener un developer token

1. En la interfaz de Google Ads: **Herramientas y configuración → Centro de API**.
2. Solicita un developer token. Empezará con nivel de acceso **Test** (solo
   funciona contra cuentas de prueba). Para operar contra la cuenta real de
   lockercuenca.es necesitas que Google apruebe el nivel **Basic**, lo cual
   puede tardar varios días — solicítalo cuanto antes.

## 3. Crear credenciales OAuth2 (tipo Desktop App)

1. En Google Cloud Console: **APIs y servicios → Credenciales → Crear
   credenciales → ID de cliente de OAuth**.
2. Tipo de aplicación: **Aplicación de escritorio**.
3. Descarga el `client_id` y `client_secret`.

## 4. Generar un refresh token

Usa el script oficial `generate_user_credentials.py` del repositorio
[`google-ads-python`](https://github.com/googleads/google-ads-python) (carpeta
`examples/authentication/`). Ejecútalo localmente con tu `client_id` y
`client_secret`; abrirá el navegador para el consentimiento OAuth y
imprimirá un `refresh_token`.

## 5. Localizar el Customer ID

Aparece arriba a la derecha en la interfaz de Google Ads, con formato
`123-456-7890`. Quita los guiones para usarlo en la configuración. Si accedes
a la cuenta a través de una cuenta de gestor (MCC), añade también el
`login_customer_id` del gestor.

## 6. Configurar el proyecto

```bash
cp google-ads.yaml.example google-ads.yaml
cp .env.example .env
```

Edita `google-ads.yaml` con `developer_token`, `client_id`, `client_secret`,
`refresh_token` (y `login_customer_id` si aplica). Edita `.env` con
`GOOGLE_ADS_CUSTOMER_ID`.

**Nunca subas `google-ads.yaml` ni `.env` a un repositorio ni los pegues en
chats o tickets** — ya están excluidos en `.gitignore`.

## 7. Instalar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# para desarrollo/tests:
pip install -r requirements-dev.txt
```

## 8. Uso

Diagnosticar todas las campañas activas:

```bash
python -m adstool.cli diagnose
```

Diagnosticar una campaña concreta y guardar el informe en Markdown:

```bash
python -m adstool.cli diagnose --campaign-id 1234567890 --output both
```

Añadir palabras clave (primero en dry-run, luego aplicando):

```bash
python -m adstool.cli add-keywords --ad-group-id 111 --use-seed-list
python -m adstool.cli add-keywords --ad-group-id 111 --use-seed-list --apply
```

Subir el presupuesto diario:

```bash
python -m adstool.cli update-budget --campaign-id 1234567890 --daily-budget 10 --apply
```

Subir la puja de una palabra clave o el Target CPA de una campaña con Smart Bidding:

```bash
python -m adstool.cli update-bid --ad-group-id 111 --criterion-id 222 --cpc-bid 0.80 --apply
python -m adstool.cli update-bid --campaign-id 1234567890 --target-cpa 15 --apply
```

Crear una acción de conversión:

```bash
python -m adstool.cli create-conversion-action --name "Llamada telefónica" --category PHONE_CALL_LEAD --type CLICK_TO_CALL --apply
```

Diagnóstico + corrección automática de problemas seguros y aditivos (subir
presupuesto dentro de un límite de seguridad, añadir keywords semilla si un
grupo de anuncios no tiene ninguna activa, crear una acción de conversión si
no existe ninguna):

```bash
python -m adstool.cli fix --campaign-id 1234567890
python -m adstool.cli fix --campaign-id 1234567890 --apply
```

`fix --apply` nunca reactiva automáticamente campañas, anuncios o palabras
clave pausados/rechazados por motivos de política — eso requiere revisión
humana y solo aparece como sugerencia en el informe.

> Nota: crear una acción de conversión vía API solo registra el recurso en la
> cuenta. Para que las conversiones se cuenten de verdad hace falta instalar
> el Google Tag en la web (o configurar el desvío de llamadas para
> `PHONE_CALL_LEAD`) — eso es un paso manual aparte.

## 9. Tests

```bash
pytest
```

Los tests usan filas y un cliente de Google Ads simulados (`tests/fixtures/`)
y no hacen ninguna llamada real a la API.

## Seguridad

- Todo comando que muta la cuenta es **dry-run por defecto**; hace falta
  `--apply` explícito, y se pide confirmación interactiva salvo que se pase
  `--yes-i-am-sure`.
- Las subidas de presupuesto están limitadas a 5x el valor actual salvo que
  se pase `--force`.
- Cada ejecución con `--apply` añade una sección "Cambios aplicados" al
  informe Markdown en `reports/`, como registro de auditoría (no hay
  rollback automático).

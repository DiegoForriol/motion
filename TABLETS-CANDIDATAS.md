# Tablets candidatas para el nivel con dispositivo dedicado

> Generado el 2026-11-15 desde el directorio oficial **Android Enterprise Recommended**
> (`androidenterprisepartners.withgoogle.com/devices`), API `/api/search/products`.

## Cómo se ha filtrado

De **126** tablets listadas para Europa quedan **38** tras aplicar:

- Pantalla de **10 pulgadas o más** (botón grande).
- **Con SIM** (`Telephony support: Yes`). Muchas casas de personas mayores no tienen wifi fiable; una SIM de datos elimina la dependencia del router (§6.4).
- **Descartada la categoría industrial** (*Rugged*): son terminales de almacén y logística, cuestan el triple y no aportan nada en una cocina.

## Conclusiones

1. **Estar en este directorio ya garantiza el modo kiosco.** El directorio solo distingue entre *Knowledge Worker* e industrial; no hay una categoría de kiosco separada, porque el modo dispositivo dedicado es parte de Android Enterprise y lo soportan todos los listados.
2. **Las 38 soportan *zero-touch***, es decir, aprovisionamiento en bloque sin tocar cada aparato. Esto deja de ser una ventaja exclusiva de Samsung y de su Knox Mobile Enrollment.
3. **El criterio que de verdad separa a las candidatas son los años de parches de seguridad**, porque marcan el ciclo de reemplazo del parque. La horquilla va de 2026 a 2032: seis años de diferencia.
4. **El directorio no incluye precios.** Consultados aparte el 2026-11-15, ver §Precios. Caducan rápido.

## Las tres que importan

| | Por qué |
|---|---|
| **Samsung Galaxy Tab A11+ 5G** | Gama barata de Samsung y **parches hasta noviembre de 2032**: siete años. La apuesta segura. |
| **Redmi Pad 2 4G** | Parches hasta julio de 2032 con actualizaciones trimestrales. Marca económica, así que probablemente la mejor relación precio/soporte de la lista. |
| **TCL TAB 10L LTE Gen 4** | 10,1", parches hasta febrero de 2028. Candidata si el precio es muy inferior a las dos de arriba. |

**Corrección respecto a la recomendación anterior:** la **Galaxy Tab A9+ 5G** solo tiene parches hasta **octubre de 2027**, menos de dos años desde hoy. Queda descartada frente a la A11+.

## Precios

Consultados el 2026-11-15 en tiendas españolas. **Caducan rápido**; verificar el día de comprar.

| Modelo (versión con SIM) | Precio | Parches restantes | **€ / año de soporte** |
|---|---|---|---|
| **Samsung Galaxy Tab A11+ 5G** 128/6 GB | **274 €** (MediaMarkt, oferta; ref. 379 €, Vodafone 360 €) | ~6,0 años | **~46 €** |
| **Redmi Pad 2 4G** 128/4 GB | **229 €** (MediaMarkt, El Corte Inglés) | ~5,7 años | **~40 €** |
| **TCL TAB 10L LTE Gen 4** | [Suposición] ~140-150 € (confirmados 107-119 € solo en la versión **wifi**) | ~1,3 años | **~115 €** |

**La más barata es la más cara.** El TCL cuesta la mitad y sale al triple por año de soporte, porque sus parches acaban en febrero de 2028.

### La versión wifi baja el precio a 208 €

La **misma A11+ sin SIM** (también con parches hasta noviembre de 2032) está a **208 €** en MediaMarkt (PVP 329 €), y hay reacondicionada a 206,90 €. Son **~35 €/año de soporte**, el suelo real de la lista para seis años de parches.

| Variante A11+ 128/6 GB | Precio | €/año |
|---|---|---|
| Wifi | **208 €** | **~35 €** |
| 5G (con SIM) | 274 € | ~46 € |

**Lo que se paga por ahorrar los 66 € + los ~5 €/mes de SIM:** dependencia del wifi de la casa. Aceptable porque el latido (§6.3) delata la caída del router al día siguiente: es un riesgo visible, no silencioso. La variante 5G queda como opción para casas sin wifi fiable.

### Decisión: Samsung A11+, pagando ~20 € más que la Redmi

La diferencia de precio con la Redmi Pad 2 wifi (180-199 €) está dentro del ruido de las ofertas. La decisión se toma por otro motivo:

**Redmi es Xiaomi.** Y Xiaomi es el fabricante más agresivo cerrando procesos en segundo plano — exactamente el problema que este producto tiene que vencer (§6.1 del análisis). Pagar 45 € más por no pelearse con HyperOS en cada dispositivo del parque es barato.

### Trampas al comprar

- **La Redmi Pad 2 a 199 € es la versión SIN 4G.** El anuncio tiene que decir "4G" explícitamente.
- **Las fichas del TCL a 107-119 € son la versión wifi.** La LTE es otro producto, con otras cámaras y ranura nano-SIM.
- La A11+ a 274 € es **precio de oferta**; el de referencia es 379 €.

### Lo que esto hace al modelo de negocio

Amortizar la tablet en la suscripción sale caro: 208 € a 6 años son ~2,90 €/mes (la de 5G, ~3,80 € más ~5 €/mes de SIM). Sobre una cuota de 20-25 €, la variante con SIM se come en torno al 40 % del margen bruto.

**Conclusión:** refuerza la opción de §6.4.4 — **que la tablet la compre la familia** (pago único de ~208 €, o la ponen ellos), y la suscripción cubra solo el servicio.

**Y el problema real no es el precio, es el momento en que se pide.** Nadie paga 208 € por una hipótesis. De ahí el orden del §6.4.1: entran gratis con el móvil que ya tienen, se topan con la fricción, y entonces el aparato es algo que quieren. Comparado con la teleasistencia (25-35 €/mes indefinidamente), 208 € de una vez se amortizan en unos ocho meses.

## Descartado: placas tipo Raspberry Pi con Android

1. [Seguro] No hay Android oficial para Raspberry; solo ports de la comunidad.
2. [Seguro] Sin Google Play Services no hay push ni Play Store — el mismo defecto que descarta la Amazon Fire. Existen licencias GMS empresariales, pero se pagan por dispositivo.
3. [Probable] No sale más barato: con pantalla táctil (~60-80 €), caja, fuente y altavoz se llega a 150-200 € por algo más grande, sin batería, sin garantía y **de montaje manual unidad por unidad**.
4. [Probable] **Y la decisiva:** vender un aparato ensamblado convierte al vendedor en **fabricante** — marcado CE, declaración de conformidad y responsabilidad de producto. Es el negocio descartado en §6.4.3.

Vale como prototipo sobre la mesa. No para instalar en casas.

## Lista completa

| Modelo | Pulgadas | OS validado | Zero-touch | Parches hasta | Frecuencia |
|---|---|---|---|---|---|
| Samsung Galaxy Tab A11+ 5G | 11.0" | Android 16 | Yes | 2032-11-29 | - |
| Samsung Galaxy Tab S11 5G | 11.0" | Android 16 | Yes | 2032-09-29 | - |
| Samsung Galaxy Tab S11 Ultra 5G | 14.6" | Android 16 | Yes | 2032-09-29 | - |
| Samsung Galaxy Tab S10 Lite 5G | 10.9" | Android 16 | Yes | 2032-08-30 | - |
| Redmi Pad 2 4G | 11.0" | Android 16 | Yes | 2032-07-30 | quarterly |
| Redmi Pad 2 Pro 5G | 12.1" | Android 16 | Yes | 2032-06-29 | quarterly |
| Samsung Galaxy Tab S10 FE 5G | 10.9" | Android 16 | Yes | 2032-04-29 | - |
| Samsung Galaxy Tab S10 FE+ 5G | 13.1" | Android 16 | Yes | 2032-04-29 | - |
| OnePlus Pad Go 2 | 12.1" | Android 16 | Yes | 2031-12-30 | - |
| Samsung Galaxy Tab S10 Ultra 5G | 14.6" | Android 16 | Yes | 2031-10-30 | - |
| Samsung Galaxy Tab S10+ 5G | 12.4" | Android 16 | Yes | 2031-10-30 | - |
| Deutsche Telekom - T Tablet 2 | 10.1" | Android 16 | Yes | 2031-07-30 | everyTwoMonths |
| Bluebird T10 | 10.9" | Android 14 | Yes | 2030-12-31 | quarterly |
| HONOR Pad 20 | 12.1" | Android 16 | Yes | 2029-08-20 | quarterly |
| unitech RT112 | 10.1" | Android 16 | Yes | 2028-09-29 | quarterly |
| Samsung Galaxy Tab S9 FE 5G | 10.9" | Android 16 | Yes | 2028-07-30 | - |
| Samsung Galaxy Tab S9 FE+ 5G | 12.4" | Android 16 | Yes | 2028-07-30 | - |
| Samsung Galaxy Tab S9 5G | 11.0" | Android 16 | Yes | 2028-06-29 | - |
| Samsung Galaxy Tab S9 Ultra 5G | 14.6" | Android 16 | Yes | 2028-06-29 | - |
| Samsung Galaxy Tab S9+ 5G | 12.4" | Android 16 | Yes | 2028-06-29 | - |
| Lenovo Tab K11 | 10.9" | Android 15 | Yes | 2028-04-29 | - |
| TCL TAB 10L LTE Gen 4 | 10.1" | Android 16 | Yes | 2028-02-28 | quarterly |
| TCL TAB 10 LTE Gen4 | 10.1" | Android 15 | Yes | 2028-02-28 | everyTwoMonths |
| Lenovo Tab M11 | 11.0" | Android 15 | Yes | 2028-02-28 | - |
| Lenovo Tab M11 | 10.9" | Android 15 | Yes | 2028-02-28 | - |
| RHINO T105 | 10.9" | Android 14 | Yes | 2027-12-30 | quarterly |
| Inventus CT7 | 10.1" | Android 15 | Yes | 2027-10-30 | quarterly |
| Samsung Galaxy Tab A9+ 5G | 11.0" | Android 15 | Yes | 2027-10-30 | - |
| Redmi Pad Pro 5G | 12.1" | Android 16 | Yes | 2027-08-30 | - |
| HMD T21 | 10.4" | Android 14 | Yes | 2027-08-30 | monthly |
| HONOR Pad 10 | 12.1" | Android 16 | Yes | 2027-06-29 | quarterly |
| HONOR Pad X9a | 11.4" | Android 16 | Yes | 2027-04-29 | - |
| Lenovo Tab Extreme | 14.5" | Android 16 | Yes | 2027-03-30 | quarterly |
| Samsung Galaxy Tab S8 5G | 11.0" | Android 15 | Yes | 2027-02-27 | - |
| Samsung Galaxy Tab S8 Ultra 5G | 14.6" | Android 15 | Yes | 2027-02-27 | - |
| Samsung Galaxy Tab S8+ 5G | 12.4" | Android 15 | Yes | 2027-02-27 | - |
| Lenovo Tab M10 5G | 10.6" | Android 14 | Yes | 2027-02-27 | - |
| TCL TAB 11 FE LTE | 10.9" | Android 16 | Yes | 2026-12-30 | quarterly |

> Dos entradas distintas comparten el nombre *Lenovo Tab M11* (11,0" y 10,9"): son variantes de hardware diferentes bajo el mismo nombre comercial. Conviene confirmar cuál se compra.


# Guía Completa SEO — lockercuenca.es con RankMath
**Versión:** 1.0 · Junio 2026  
**Objetivo:** Posicionar lockercuenca.es para ~295.000 búsquedas/mes en Cuenca, España  
**Plugin:** RankMath SEO (WordPress)

---

## ÍNDICE

1. [Fix urgente — Desbloquear Google](#1-fix-urgente)
2. [Configuración inicial de RankMath](#2-configuración-inicial-rankmath)
3. [Robots.txt y Sitemap](#3-robotstxt-y-sitemap)
4. [SEO Local — Schema del negocio](#4-seo-local--schema)
5. [Página a página — Títulos, Meta y Keywords](#5-página-a-página)
6. [Plan de contenidos — 14 páginas a crear](#6-plan-de-contenidos)
7. [Checklist por página nueva](#7-checklist-por-página-nueva)
8. [Google Business Profile](#8-google-business-profile)
9. [Google Search Console](#9-google-search-console)
10. [Hoja de ruta 6 meses](#10-hoja-de-ruta-6-meses)

---

## 1. Fix Urgente

> ⚠️ **El sitio tiene 0 páginas indexadas en Google. Esto va primero.**

### 1.1 Desactivar Bot Fight Mode en Cloudflare (vía Raiola)

1. Entra en `https://clientes.raiolanetworks.es`
2. Selecciona el dominio `lockercuenca.es`
3. Busca la sección **Cloudflare** o **CDN**
4. Dentro del panel Cloudflare: **Security → Bots → Bot Fight Mode → OFF**
5. Guarda

### 1.2 Desactivar Noindex global en RankMath

1. WordPress → **RankMath → Titles & Meta → Global Meta**
2. Busca **"No Index Entire Site"** → debe estar **DESACTIVADO** (toggle gris)
3. Si está activo (azul), desactívalo → Guardar cambios

### 1.3 WordPress no bloquea buscadores

1. WordPress → **Ajustes → Lectura**
2. Comprueba que **"Disuadir a los motores de búsqueda de indexar este sitio"** está **DESMARCADO**
3. Guardar cambios

---

## 2. Configuración Inicial RankMath

### 2.1 Asistente de configuración

**RankMath → Dashboard → Setup Wizard** (si no lo has completado)

- Tipo de sitio: **Business Website**
- Nombre del negocio: `Locker Cuenca`
- Logo: subir logo del negocio
- Buscar consola: conectar Google Search Console (ver sección 9)

---

### 2.2 General Settings

**RankMath → General Settings**

| Opción | Valor |
|--------|-------|
| Separator | `–` (guión largo) |
| Breadcrumbs | **Activado** |
| Noindex empty category/tag archives | **Activado** |
| Noindex paginated pages | **Desactivado** |
| Strip Category Base | **Activado** |
| Capitalize titles | Según preferencia |

---

### 2.3 Títulos y Meta globales

**RankMath → Titles & Meta → Global Meta**

| Campo | Valor |
|-------|-------|
| Homepage Title | `Locker Cuenca – Consigna de Equipaje en Cuenca` |
| Homepage Description | `Guarda tu equipaje en nuestras taquillas automáticas en el centro de Cuenca. Sin esperas. Abierto todos los días. Desde X€/día.` |
| Robots Meta | **Index, Follow** |
| Max Snippet | `-1` (sin límite) |
| Max Image Preview | `large` |
| Max Video Preview | `-1` |

---

### 2.4 Activar módulos necesarios

**RankMath → Dashboard → Modules**

Activar:
- ✅ **Local SEO** — imprescindible para negocio físico
- ✅ **Schema (Structured Data)** — rich snippets
- ✅ **Sitemap** — rastreabilidad
- ✅ **SEO Analysis** — diagnóstico
- ✅ **404 Monitor** — detectar páginas rotas
- ✅ **Redirections** — gestionar redirecciones
- ✅ **Rich Snippets** — FAQs, estrellas
- ✅ **Google Search Console** — datos reales

Desactivar (si no los usas):
- ❌ WooCommerce SEO (si no tienes tienda)
- ❌ News Sitemap (si no es periódico)

---

## 3. Robots.txt y Sitemap

### 3.1 Editar robots.txt

**RankMath → General Settings → Edit robots.txt**

Contenido completo:
```
User-agent: *
Allow: /

Disallow: /wp-admin/
Disallow: /wp-login.php
Disallow: /wp-json/
Disallow: /cart/
Disallow: /checkout/
Disallow: /?s=
Disallow: /search/

Sitemap: https://lockercuenca.es/sitemap_index.xml
```

Guardar.

---

### 3.2 Configurar Sitemap

**RankMath → Sitemap Settings**

| Sección | Activar |
|---------|---------|
| Posts Sitemap | ✅ Sí |
| Pages Sitemap | ✅ Sí |
| Categories Sitemap | ✅ Sí |
| Author Sitemap | ❌ No (desactivar, oculta datos de usuario) |
| Media/Attachments | ❌ No |

**Images in Sitemap** → ✅ Activado  
**Include Featured Images** → ✅ Activado

Tras guardar: copiar la URL `https://lockercuenca.es/sitemap_index.xml` para enviarla a Google Search Console.

---

## 4. SEO Local — Schema

### 4.1 Configurar Local SEO

**RankMath → Titles & Meta → Local SEO**

| Campo | Valor |
|-------|-------|
| Business Type | `LocalBusiness` → subcategoría: `LuggageStorage` |
| Business Name | `Locker Cuenca` |
| Street Address | [Tu dirección] |
| City | `Cuenca` |
| State/Province | `Castilla-La Mancha` |
| Postal Code | `160XX` |
| Country | `Spain` |
| Phone | `+34 XXX XXX XXX` |
| Email | [Tu email de contacto] |
| URL | `https://lockercuenca.es` |
| Price Range | `€€` |
| Latitude | [Latitud de tu local] |
| Longitude | [Longitud de tu local] |
| Opening Hours | Todos los días X:00 – X:00 |

**Social Profiles** (añadir todos):
- Facebook: `https://www.facebook.com/lockercuenca/`
- Instagram: `https://www.instagram.com/lockerscuenca/`

Guardar.

---

### 4.2 Schema en la Homepage

**Editar la Homepage → RankMath (panel lateral) → Schema**

- Tipo: **Local Business**
- Confirma que hereda los datos del paso 4.1
- Añadir también: **FAQ Schema** con estas preguntas (modifica los datos con los tuyos):

```
Pregunta 1: ¿Cuánto cuesta guardar una maleta en Locker Cuenca?
Respuesta:  El precio es de X€ por día o X€ por hora. Sin comisiones ocultas.

Pregunta 2: ¿Dónde están las taquillas de Locker Cuenca?
Respuesta:  Estamos en [dirección], a X minutos a pie de las Casas Colgadas y la Catedral.

Pregunta 3: ¿En qué horario podéis guardar el equipaje?
Respuesta:  Abrimos todos los días de X:00 a X:00, incluidos festivos.

Pregunta 4: ¿Puedo reservar online?
Respuesta:  Sí, puedes reservar tu taquilla desde nuestra web y pagar al llegar.

Pregunta 5: ¿Qué tamaños de taquilla tenéis disponibles?
Respuesta:  Disponemos de taquillas para maleta de mano, maleta mediana y maleta grande.
```

---

## 5. Página a Página

> Para cada página: editar en WordPress → panel RankMath lateral → rellenar los campos indicados.

---

### HOMEPAGE — lockercuenca.es

| Campo RankMath | Valor |
|----------------|-------|
| **Focus Keyword** | `consigna equipaje Cuenca` |
| **SEO Title** | `Locker Cuenca – Consigna de Equipaje en Cuenca \| Taquillas para Turistas` |
| **Meta Description** | `Guarda tu equipaje en nuestras taquillas automáticas en el centro de Cuenca. Seguro, fácil y económico. Desde X€/día. A 5 min de las Casas Colgadas.` |
| **Robots** | Index, Follow |
| **Schema** | LocalBusiness + FAQ |
| **Canonical** | `https://lockercuenca.es/` |

**Keywords secundarias a incluir en el contenido:**  
`taquillas Cuenca`, `locker Cuenca`, `guardar maletas Cuenca`, `taquillas turistas`, `consigna turistas Cuenca`

**H1 recomendado:**  
`Consigna de Equipaje en Cuenca — Tus Taquillas en el Centro Histórico`

**H2s recomendados:**
- `¿Cómo funciona?`
- `Nuestras taquillas`
- `¿Dónde estamos?`
- `Precios`
- `Preguntas frecuentes`

---

### PÁGINA: Consigna de Equipaje
**URL:** `/consigna-equipaje-cuenca/`

| Campo RankMath | Valor |
|----------------|-------|
| **Focus Keyword** | `consigna equipaje Cuenca` |
| **SEO Title** | `Consigna Equipaje Cuenca – Taquillas 24h para Turistas \| Locker Cuenca` |
| **Meta Description** | `Consigna de equipaje en Cuenca desde X€/día. Taquillas automáticas en el centro histórico. Sin reserva previa. Abierto todos los días. ✓ Seguro y económico.` |
| **Schema** | LocalBusiness + FAQ + AggregateRating |
| **Robots** | Index, Follow |

**Keywords secundarias:** `taquillas Cuenca`, `locker Cuenca`, `guardar equipaje Cuenca`, `alquiler taquillas Cuenca`, `consigna Cuenca turistas`

**H1:** `Consigna de Equipaje en Cuenca: Deja la Maleta y Disfruta la Ciudad`

**H2s:**
- `¿Por qué guardar tu equipaje con nosotros?`
- `Cómo funciona nuestra consigna`
- `Tarifas y precios`
- `Nuestra ubicación en Cuenca`
- `Preguntas frecuentes`

---

### PÁGINA: Taquillas y Lockers — Precios
**URL:** `/taquillas-cuenca/`

| Campo RankMath | Valor |
|----------------|-------|
| **Focus Keyword** | `taquillas Cuenca` |
| **SEO Title** | `Taquillas en Cuenca – Precios y Ubicaciones \| Locker Cuenca` |
| **Meta Description** | `Alquila una taquilla en Cuenca desde X€. Lockers para maleta pequeña, mediana y grande. Reserva online. Centro histórico de Cuenca, España.` |
| **Schema** | Product + FAQ |
| **Robots** | Index, Follow |

**Keywords secundarias:** `alquiler taquillas Cuenca`, `locker Cuenca precio`, `taquillas baratas Cuenca`, `guardar maleta Cuenca precio`, `consigna barata Cuenca`

**H1:** `Taquillas y Lockers en Cuenca: Tarifas, Tamaños y Reserva`

---

### PÁGINA: Dónde Guardar las Maletas sin Hotel
**URL:** `/guardar-maletas-cuenca-sin-hotel/`

| Campo RankMath | Valor |
|----------------|-------|
| **Focus Keyword** | `guardar maletas Cuenca sin hotel` |
| **SEO Title** | `Dónde Guardar las Maletas en Cuenca sin Hotel – Guía 2026` |
| **Meta Description** | `¿De excursión a Cuenca sin hotel? Guarda tus maletas en nuestras taquillas desde X€. 5 opciones comparadas. La mejor solución para turistas de día.` |
| **Schema** | Article + FAQ |
| **Robots** | Index, Follow |

**Keywords secundarias:** `donde guardar maletas Cuenca`, `consigna Cuenca turistas día`, `taquillas turistas Cuenca`, `guardar equipaje Cuenca excursión`

---

### PÁGINA: Consigna Estación de Tren
**URL:** `/consigna-estacion-tren-cuenca/`

| Campo RankMath | Valor |
|----------------|-------|
| **Focus Keyword** | `consigna estación tren Cuenca` |
| **SEO Title** | `Consigna en la Estación de Tren de Cuenca – Opciones para Turistas` |
| **Meta Description** | `¿Llegas en tren a Cuenca? Guarda tu maleta en nuestras taquillas. A X minutos de la estación Fernando Zóbel. Desde X€. Sin comisiones.` |
| **Schema** | Article + FAQ |
| **Robots** | Index, Follow |

**Keywords secundarias:** `consigna Cuenca 24 horas`, `guardar maletas estación Cuenca`, `equipaje estación Fernando Zóbel`, `guarda maletas por horas Cuenca`

---

### PÁGINA: Excursión a Cuenca desde Madrid
**URL:** `/excursion-cuenca-desde-madrid/`

| Campo RankMath | Valor |
|----------------|-------|
| **Focus Keyword** | `excursión Cuenca desde Madrid` |
| **SEO Title** | `Excursión a Cuenca desde Madrid en un Día – Guía Completa 2026` |
| **Meta Description** | `Cómo hacer la excursión a Cuenca desde Madrid: tren, horarios, qué ver y dónde comer. Guía paso a paso para aprovechar el día sin cargar maletas.` |
| **Schema** | Article + HowTo |
| **Robots** | Index, Follow |

**Keywords secundarias:** `Cuenca en un día desde Madrid`, `viaje Cuenca día`, `qué ver en Cuenca excursión`, `tren Madrid Cuenca horario precio`

**H1:** `Excursión a Cuenca desde Madrid en un Día: Todo lo que Necesitas Saber`

**H2s:**
- `Cómo llegar a Cuenca desde Madrid`
- `Qué ver en Cuenca en un día`
- `Dónde comer en Cuenca`
- `Consejo: deja las maletas al llegar`
- `Horarios y precios del tren`

**CTA en el artículo:** *"Al llegar a la estación de Cuenca, deja tus maletas en nuestras taquillas y disfruta el día con las manos libres."*

---

### PÁGINA: Cuenca en un Fin de Semana
**URL:** `/cuenca-fin-de-semana/`

| Campo RankMath | Valor |
|----------------|-------|
| **Focus Keyword** | `fin de semana Cuenca` |
| **SEO Title** | `Cuenca en un Fin de Semana: Itinerario Perfecto 2026` |
| **Meta Description** | `El itinerario de fin de semana definitivo en Cuenca. Día 1 y Día 2 detallados: qué ver, dónde comer, dónde dormir y cómo moverte sin cargar maletas.` |
| **Schema** | Article |
| **Robots** | Index, Follow |

**Keywords secundarias:** `escapada Cuenca`, `qué hacer en Cuenca fin de semana`, `Cuenca 2 días`, `viaje fin de semana Cuenca`

---

### PÁGINA: Qué Ver en Cuenca en 2 Días
**URL:** `/que-ver-cuenca-2-dias/`

| Campo RankMath | Valor |
|----------------|-------|
| **Focus Keyword** | `qué ver en Cuenca en 2 días` |
| **SEO Title** | `Qué Ver en Cuenca en 2 Días: Ruta Completa con Mapa (2026)` |
| **Meta Description** | `Ruta de 2 días en Cuenca: Casas Colgadas, Catedral, Ciudad Encantada y mucho más. Mapa descargable + consejos de transporte y alojamiento.` |
| **Schema** | Article |
| **Robots** | Index, Follow |

**Keywords secundarias:** `itinerario Cuenca 2 días`, `itinerario Cuenca 1 día`, `Cuenca 48 horas`, `ruta Cuenca mapa`

---

### PÁGINA: Casas Colgadas de Cuenca
**URL:** `/casas-colgadas-cuenca/`

| Campo RankMath | Valor |
|----------------|-------|
| **Focus Keyword** | `casas colgadas Cuenca` |
| **SEO Title** | `Casas Colgadas de Cuenca: Horario, Precio y Cómo Visitarlas (2026)` |
| **Meta Description** | `Todo sobre las Casas Colgadas de Cuenca: horario de apertura, precio de entrada, cómo llegar andando y los mejores miradores. Guía actualizada 2026.` |
| **Schema** | Article + TouristAttraction |
| **Robots** | Index, Follow |

**Keywords secundarias:** `casas colgantes Cuenca`, `museo arte abstracto Cuenca`, `Puente San Pablo Cuenca`, `Hoz del Huécar Cuenca`, `fotos casas colgadas Cuenca`

**H1:** `Casas Colgadas de Cuenca: La Guía Definitiva para Visitarlas`

**H2s:**
- `Qué son las Casas Colgadas`
- `Horario y precio de entrada`
- `Cómo llegar a las Casas Colgadas`
- `El Museo de Arte Abstracto`
- `Los mejores miradores`
- `Consejo práctico: deja la maleta antes de subir`

---

### PÁGINA: Ciudad Encantada de Cuenca
**URL:** `/ciudad-encantada-cuenca/`

| Campo RankMath | Valor |
|----------------|-------|
| **Focus Keyword** | `Ciudad Encantada Cuenca` |
| **SEO Title** | `Ciudad Encantada de Cuenca: Horario, Precio y Cómo Llegar (2026)` |
| **Meta Description** | `Guía completa de la Ciudad Encantada de Cuenca: horario, precio de entrada, cómo llegar sin coche y qué ver. A 36 km de Cuenca capital.` |
| **Schema** | Article + TouristAttraction |
| **Robots** | Index, Follow |

**Keywords secundarias:** `Ciudad Encantada Cuenca cómo llegar`, `Ciudad Encantada horario precio`, `excursión Ciudad Encantada desde Cuenca`, `Serranía de Cuenca`

---

### PÁGINA: Catedral de Cuenca
**URL:** `/catedral-cuenca/`

| Campo RankMath | Valor |
|----------------|-------|
| **Focus Keyword** | `catedral de Cuenca` |
| **SEO Title** | `Catedral de Cuenca: Horario, Precio de Entrada y Qué Ver` |
| **Meta Description** | `Visita la Catedral de Cuenca, primera catedral gótica de Castilla. Horario actualizado, precio de entrada y los imprescindibles de su interior.` |
| **Schema** | Article + LandmarksOrHistoricalBuildings |
| **Robots** | Index, Follow |

**Keywords secundarias:** `catedral Cuenca entrada precio`, `catedral gótica Cuenca`, `visitar catedral Cuenca`, `Cuenca Patrimonio UNESCO`, `museos de Cuenca`

---

### PÁGINA PILAR: Guía Qué Ver en Cuenca
**URL:** `/guia-que-ver-en-cuenca/`  
*(Página más importante del sitio — publicar primero)*

| Campo RankMath | Valor |
|----------------|-------|
| **Focus Keyword** | `que ver en Cuenca` |
| **SEO Title** | `Qué Ver en Cuenca: Guía Completa 2026 (Con Mapa e Itinerarios)` |
| **Meta Description** | `La guía definitiva de Cuenca: Casas Colgadas, Catedral, Ciudad Encantada, itinerarios de 1 y 2 días, dónde comer y cómo moverte. Todo en un lugar.` |
| **Schema** | Article + BreadcrumbList + ItemList |
| **Robots** | Index, Follow |

**Keywords secundarias:** `visitar Cuenca`, `turismo Cuenca`, `qué ver en Cuenca en un día`, `Cuenca España`, `Cuenca Patrimonio UNESCO`

**H1:** `Qué Ver en Cuenca: La Guía Definitiva para Tu Visita`

**H2s:**
- `Por qué visitar Cuenca (Patrimonio de la Humanidad UNESCO)`
- `Las Casas Colgadas` → enlace interno a `/casas-colgadas-cuenca/`
- `La Catedral de Cuenca` → enlace interno a `/catedral-cuenca/`
- `Ciudad Encantada` → enlace interno a `/ciudad-encantada-cuenca/`
- `Cómo llegar a Cuenca desde Madrid` → enlace interno a `/como-llegar-cuenca-desde-madrid/`
- `Itinerarios: 1 día, 2 días, fin de semana` → enlace interno a rutas
- `Dónde comer en Cuenca`
- `💼 Viaja sin peso: deja tus maletas` → enlace interno a `/consigna-equipaje-cuenca/`

> Esta página debe enlazar a TODAS las demás. Es el hub de toda la arquitectura.

---

### PÁGINA: Cómo Llegar a Cuenca desde Madrid
**URL:** `/como-llegar-cuenca-desde-madrid/`

| Campo RankMath | Valor |
|----------------|-------|
| **Focus Keyword** | `cómo ir a Cuenca desde Madrid` |
| **SEO Title** | `Cómo Llegar a Cuenca desde Madrid: Tren, Bus y Coche (2026)` |
| **Meta Description** | `Todas las opciones para llegar a Cuenca desde Madrid: AVE, autobús y coche. Tiempos, precios y comparativa. + Consejo: guarda el equipaje al llegar.` |
| **Schema** | Article + HowTo |
| **Robots** | Index, Follow |

**Keywords secundarias:** `tren Cuenca Madrid precio`, `bus Cuenca Madrid horario`, `cómo llegar a Cuenca en tren`, `AVE Cuenca`, `estación tren Cuenca centro`

---

### PÁGINA: Aparcar en Cuenca
**URL:** `/aparcar-cuenca-casco-historico/`

| Campo RankMath | Valor |
|----------------|-------|
| **Focus Keyword** | `aparcar en Cuenca casco histórico` |
| **SEO Title** | `Aparcar en Cuenca: Guía de Parkings en el Casco Histórico 2026` |
| **Meta Description** | `Dónde aparcar en Cuenca sin complicaciones: parkings gratuitos, de pago y consejos para el casco histórico. Alternativa: deja el coche y guarda el equipaje.` |
| **Schema** | Article |
| **Robots** | Index, Follow |

**Keywords secundarias:** `parking Cuenca casco antiguo`, `dónde aparcar Cuenca`, `parking gratuito Cuenca`, `transporte en Cuenca`

---

### PÁGINA: Maletas para el Fin de Semana
**URL:** `/maletas-fin-de-semana-cuenca/`

| Campo RankMath | Valor |
|----------------|-------|
| **Focus Keyword** | `maletas fin de semana Cuenca` |
| **SEO Title** | `Maletas para Cuenca: Qué Llevar en el Equipaje (y Cómo Ir Ligero)` |
| **Meta Description** | `Lista de equipaje para un fin de semana en Cuenca. Qué llevar, qué no llevar y cómo disfrutar la ciudad sin cargar peso. Ideal para escapadas desde Madrid.` |
| **Schema** | Article |
| **Robots** | Index, Follow |

**Keywords secundarias:** `equipaje fin de semana Cuenca`, `qué llevar a Cuenca`, `maleta escapada Cuenca`

---

## 6. Plan de Contenidos

> 14 páginas ordenadas por prioridad. Publica en este orden exacto.

### Mes 1 — Julio 2026 (Fundación)

| Prioridad | Página | Keyword principal | Vol/mes | KD | Palabras |
|-----------|--------|-------------------|---------|-----|---------|
| 🔴 **#1** | Guía Qué Ver en Cuenca (PILAR) | `que ver en Cuenca` | 40.500 | 52 | 3.500 |
| 🔴 **#2** | Consigna de Equipaje en Cuenca | `consigna equipaje Cuenca` | 1.000 | 35 | 1.400 |
| 🔴 **#3** | Excursión desde Madrid | `excursión Cuenca desde Madrid` | 14.800 | 45 | 1.600 |

**Por qué este orden:** La página pilar (#1) activa todos los enlaces internos del sitio. La página de consigna (#2) genera conversiones desde el primer día. La excursión desde Madrid (#3) captura el mayor volumen de tráfico de verano.

---

### Mes 2 — Agosto 2026 (Temporada alta)

| Prioridad | Página | Keyword principal | Vol/mes | KD | Palabras |
|-----------|--------|-------------------|---------|-----|---------|
| 🟠 **#4** | Casas Colgadas de Cuenca | `casas colgadas Cuenca` | 22.200 | 48 | 1.500 |
| 🟠 **#5** | Guardar maletas sin hotel | `guardar maletas Cuenca sin hotel` | 450 | 18 | 1.300 |
| 🟠 **#6** | Taquillas y lockers — precios | `taquillas Cuenca` | 800 | 30 | 1.400 |

---

### Mes 3 — Septiembre 2026 (Escapadas otoño)

| Prioridad | Página | Keyword principal | Vol/mes | KD | Palabras |
|-----------|--------|-------------------|---------|-----|---------|
| 🟡 **#7** | Cuenca en un fin de semana | `fin de semana Cuenca` | 12.100 | 42 | 1.700 |
| 🟡 **#8** | Qué ver en Cuenca en 2 días | `qué ver en Cuenca en 2 días` | 9.900 | 40 | 1.700 |

---

### Mes 4 — Octubre 2026

| Prioridad | Página | Keyword principal | Vol/mes | KD | Palabras |
|-----------|--------|-------------------|---------|-----|---------|
| 🟢 **#9** | Ciudad Encantada de Cuenca | `Ciudad Encantada Cuenca` | 18.100 | 38 | 1.800 |
| 🟢 **#10** | Catedral de Cuenca | `catedral de Cuenca` | 9.900 | 35 | 1.300 |

---

### Mes 5 — Noviembre 2026

| Prioridad | Página | Keyword principal | Vol/mes | KD | Palabras |
|-----------|--------|-------------------|---------|-----|---------|
| 🔵 **#11** | Consigna estación de tren | `consigna estación tren Cuenca` | 250 | 20 | 1.200 |
| 🔵 **#12** | Cómo llegar a Cuenca | `cómo ir a Cuenca desde Madrid` | 6.600 | 35 | 1.400 |

---

### Mes 6 — Diciembre 2026

| Prioridad | Página | Keyword principal | Vol/mes | KD | Palabras |
|-----------|--------|-------------------|---------|-----|---------|
| ⚪ **#13** | Aparcar en Cuenca | `aparcar en Cuenca casco histórico` | 2.400 | 28 | 1.200 |
| ⚪ **#14** | Maletas fin de semana | `maletas fin de semana Cuenca` | 300 | 12 | 1.200 |

---

## 7. Checklist por Página Nueva

> Usar para cada página antes de publicarla.

### En RankMath (panel lateral al editar la página)

- [ ] **Focus Keyword** → rellenado con la keyword principal
- [ ] **SEO Title** → entre 50-60 caracteres, incluye keyword + marca
- [ ] **Meta Description** → entre 150-160 caracteres, incluye keyword + CTA
- [ ] **Puntuación RankMath** → mínimo 80/100 (verde)
- [ ] **Schema** → tipo correcto seleccionado (Article, FAQ, LocalBusiness...)
- [ ] **Canonical URL** → apunta a sí misma (sin parámetros)
- [ ] **Robots** → Index, Follow

### En el contenido (editor de WordPress)

- [ ] **H1** → contiene la keyword principal (solo 1 H1 por página)
- [ ] **H2s** → al menos 3, contienen variantes de keyword
- [ ] **Keyword en primer párrafo** → aparece en los primeros 100 caracteres
- [ ] **Keyword density** → entre 1-2% (RankMath lo indica)
- [ ] **Imágenes** → todas con `alt text` que describe la imagen (incluir keyword cuando sea natural)
- [ ] **Enlace al pilar** → cada spoke enlaza a `/guia-que-ver-en-cuenca/`
- [ ] **Enlace a consigna** → cada artículo de turismo enlaza a `/consigna-equipaje-cuenca/`
- [ ] **2-3 enlaces internos** → a páginas relacionadas del mismo cluster
- [ ] **Longitud mínima** → la indicada en el plan (1.200 - 3.500 palabras)
- [ ] **Permalink** → URL corta, en minúsculas, con guiones, sin acentos

### Tras publicar

- [ ] Google Search Console → Inspeccionar URL → Solicitar indexación
- [ ] Comprobar que aparece en el sitemap: `https://lockercuenca.es/sitemap_index.xml`
- [ ] Añadir enlace desde la página pilar hacia la nueva página

---

## 8. Google Business Profile

> Imprescindible. Apareces en Google Maps sin depender del posicionamiento web.

### Crear / reclamar la ficha

1. Ve a `https://business.google.com`
2. Busca "Locker Cuenca" — si ya existe, reclamar. Si no, crear desde cero.
3. Verificar el negocio (te envían una tarjeta postal o verificación por teléfono)

### Rellenar al 100%

| Campo | Qué poner |
|-------|-----------|
| Nombre | `Locker Cuenca` |
| Categoría principal | `Luggage storage facility` |
| Categorías secundarias | `Locker rental service` |
| Dirección | Dirección física completa |
| Teléfono | +34 XXX XXX XXX |
| Web | https://lockercuenca.es |
| Horario | Cada día con apertura y cierre real |
| Descripción (750 car.) | *"Locker Cuenca ofrece consigna de equipaje y taquillas automáticas en el centro histórico de Cuenca. Guarda tus maletas de forma segura mientras visitas las Casas Colgadas, la Catedral y el resto de la ciudad. Abiertos todos los días."* |
| Fotos | Mínimo 10: exterior, interior, taquillas, zona histórica cercana |

### Conseguir las primeras reseñas

- Pide a cada cliente satisfecho que deje reseña
- Objetivo: **10 reseñas con ≥ 4,0 estrellas** en los primeros 30 días
- Crea un enlace corto de reseña desde GBP → compártelo por WhatsApp

---

## 9. Google Search Console

### Configurar

1. Ve a `https://search.google.com/search-console`
2. Crear propiedad → "Prefijo de URL" → `https://lockercuenca.es`
3. Método de verificación: **Etiqueta HTML** → copiar el meta tag
4. En WordPress: **RankMath → General Settings → Webmaster Tools → Google Search Console** → pegar el código de verificación
5. Guardar → volver a GSC → verificar

### Enviar el sitemap

1. GSC → panel izquierdo → **Sitemaps**
2. Añadir: `sitemap_index.xml`
3. Enviar
4. Estado debe cambiar a "Correcto" en 24-48h

### Solicitar indexación de páginas prioritarias

Tras publicar cada página:
1. GSC → **Inspección de URLs**
2. Pegar la URL de la página
3. Clic en **"Solicitar indexación"**

---

## 10. Hoja de Ruta 6 Meses

```
JUL 2026 — Fundación
━━━━━━━━━━━━━━━━━━━━
☐ Desbloquear WAF en Raiola/Cloudflare
☐ Verificar noindex desactivado (RankMath + WordPress)
☐ Configurar RankMath completo (secciones 2-4)
☐ Configurar robots.txt y sitemap
☐ Google Search Console conectado
☐ Google Business Profile creado y verificado
☐ Publicar página pilar: "Qué ver en Cuenca" (#1)
☐ Publicar landing consigna: "Consigna equipaje Cuenca" (#2)
☐ Publicar: "Excursión desde Madrid" (#3)
☐ Solicitar indexación de las 3 páginas en GSC

AGO 2026 — Temporada Alta
━━━━━━━━━━━━━━━━━━━━━━━━━
☐ Publicar: "Casas Colgadas Cuenca" (#4) — 22.200 búsquedas/mes
☐ Publicar: "Guardar maletas sin hotel" (#5)
☐ Publicar: "Taquillas y lockers — precios" (#6)
☐ Conseguir 10 reseñas en Google Business Profile
☐ Registrar negocio en TripAdvisor
☐ Registrar en Bing Places
☐ Instalar plugin de caché (WP Rocket / LiteSpeed)

SEP 2026 — Escapadas Otoño
━━━━━━━━━━━━━━━━━━━━━━━━━━
☐ Publicar: "Cuenca en un fin de semana" (#7)
☐ Publicar: "Qué ver en Cuenca en 2 días" (#8)
☐ Revisar posiciones en GSC — ajustar titles si CTR < 3%
☐ Empezar outreach a 5 blogs de viajes sobre Cuenca

OCT 2026 — Atracciones
━━━━━━━━━━━━━━━━━━━━━━
☐ Publicar: "Ciudad Encantada de Cuenca" (#9)
☐ Publicar: "Catedral de Cuenca" (#10)
☐ Registrar en Civitatis como servicio/actividad
☐ Revisar Core Web Vitals en GSC → corregir si LCP > 2.5s

NOV 2026 — Logística
━━━━━━━━━━━━━━━━━━━━
☐ Publicar: "Consigna estación de tren" (#11)
☐ Publicar: "Cómo llegar a Cuenca desde Madrid" (#12)
☐ Añadir página en inglés: /en/luggage-storage-cuenca/
☐ Revisar páginas con posición 11-20 → optimizar

DIC 2026 — Long-Tail
━━━━━━━━━━━━━━━━━━━━
☐ Publicar: "Aparcar en Cuenca" (#13)
☐ Publicar: "Maletas para el fin de semana" (#14)
☐ Crear llms.txt para citabilidad en ChatGPT/Perplexity
☐ Balance: revisar posiciones, tráfico y conversiones
☐ Planificar contenidos 2027
```

---

## KPIs — Qué medir cada mes en GSC

| Métrica | Mes 1 | Mes 3 | Mes 6 |
|---------|-------|-------|-------|
| Páginas indexadas | 3+ | 10+ | 14 |
| Clics orgánicos/mes | ~10 | ~200 | ~2.000 |
| Posición media | — | Top 50 | Top 20 |
| "consigna Cuenca" posición | — | Top 30 | Top 5 |
| "que ver en Cuenca" posición | — | Top 100 | Top 30 |
| Reseñas Google | 3 | 15 | 30+ |

---

## Resumen de los 50 Keywords por Cluster

### Cluster 0 — Consigna & Taquillas (intención transaccional)
| Keyword | Vol/mes | KD | Página |
|---------|---------|-----|--------|
| consigna equipaje Cuenca | 1.000 | 35 | /consigna-equipaje-cuenca/ |
| taquillas Cuenca | 800 | 30 | /taquillas-cuenca/ |
| guardar maletas Cuenca | 600 | 28 | /guardar-maletas-cuenca-sin-hotel/ |
| locker Cuenca | 500 | 25 | /consigna-equipaje-cuenca/ |
| alquiler taquillas Cuenca | 400 | 22 | /taquillas-cuenca/ |
| consigna Cuenca turistas | 300 | 20 | /guardar-maletas-cuenca-sin-hotel/ |
| guardar maletas Cuenca sin hotel | 250 | 18 | /guardar-maletas-cuenca-sin-hotel/ |
| consigna estación tren Cuenca | 250 | 20 | /consigna-estacion-tren-cuenca/ |
| taquillas turistas Cuenca | 200 | 18 | /guardar-maletas-cuenca-sin-hotel/ |
| consigna Cuenca 24 horas | 120 | 18 | /consigna-estacion-tren-cuenca/ |
| precio consigna equipaje Cuenca | 120 | 20 | /taquillas-cuenca/ |
| guarda maletas por horas Cuenca | 100 | 15 | /consigna-estacion-tren-cuenca/ |
| consigna barata Cuenca | 90 | 15 | /taquillas-cuenca/ |
| guardar maletas fin de semana Cuenca | 150 | 15 | /maletas-fin-de-semana-cuenca/ |

### Cluster 1 — Excursiones e Itinerarios
| Keyword | Vol/mes | KD | Página |
|---------|---------|-----|--------|
| excursión Cuenca desde Madrid | 14.800 | 45 | /excursion-cuenca-desde-madrid/ |
| Cuenca en un día desde Madrid | 9.900 | 42 | /excursion-cuenca-desde-madrid/ |
| fin de semana Cuenca | 12.100 | 42 | /cuenca-fin-de-semana/ |
| escapada Cuenca | 8.100 | 40 | /cuenca-fin-de-semana/ |
| qué ver en Cuenca en 2 días | 9.900 | 40 | /que-ver-cuenca-2-dias/ |
| itinerario Cuenca 1 día | 4.400 | 35 | /que-ver-cuenca-2-dias/ |
| itinerario Cuenca 2 días | 3.600 | 32 | /que-ver-cuenca-2-dias/ |
| viaje Cuenca | 6.600 | 38 | /excursion-cuenca-desde-madrid/ |

### Cluster 2 — Atracciones Icónicas
| Keyword | Vol/mes | KD | Página |
|---------|---------|-----|--------|
| casas colgadas Cuenca | 22.200 | 48 | /casas-colgadas-cuenca/ |
| casas colgantes Cuenca | 3.600 | 35 | /casas-colgadas-cuenca/ |
| museo arte abstracto Cuenca | 2.400 | 30 | /casas-colgadas-cuenca/ |
| Puente San Pablo Cuenca | 4.400 | 32 | /casas-colgadas-cuenca/ |
| Hoz del Huécar Cuenca | 2.400 | 28 | /casas-colgadas-cuenca/ |
| Ciudad Encantada Cuenca | 18.100 | 38 | /ciudad-encantada-cuenca/ |
| Ciudad Encantada Cuenca cómo llegar | 4.400 | 30 | /ciudad-encantada-cuenca/ |
| excursión Ciudad Encantada desde Cuenca | 2.900 | 28 | /ciudad-encantada-cuenca/ |
| Serranía de Cuenca | 5.400 | 38 | /ciudad-encantada-cuenca/ |
| catedral de Cuenca | 9.900 | 35 | /catedral-cuenca/ |
| catedral Cuenca entrada precio | 2.400 | 28 | /catedral-cuenca/ |
| Cuenca Patrimonio UNESCO | 3.600 | 35 | /catedral-cuenca/ |
| museos de Cuenca | 3.600 | 30 | /catedral-cuenca/ |

### Cluster 3 — Logística del Viajero
| Keyword | Vol/mes | KD | Página |
|---------|---------|-----|--------|
| cómo ir a Cuenca desde Madrid | 6.600 | 35 | /como-llegar-cuenca-desde-madrid/ |
| tren Cuenca Madrid precio | 3.600 | 30 | /como-llegar-cuenca-desde-madrid/ |
| bus Cuenca Madrid horario | 2.400 | 28 | /como-llegar-cuenca-desde-madrid/ |
| cómo llegar a Cuenca en tren | 4.400 | 30 | /como-llegar-cuenca-desde-madrid/ |
| estación tren Cuenca centro | 1.900 | 25 | /como-llegar-cuenca-desde-madrid/ |
| aparcar en Cuenca casco histórico | 2.400 | 28 | /aparcar-cuenca-casco-historico/ |
| parking Cuenca casco antiguo | 1.600 | 25 | /aparcar-cuenca-casco-historico/ |
| transporte en Cuenca | 1.900 | 25 | /aparcar-cuenca-casco-historico/ |
| maletas fin de semana Cuenca | 300 | 12 | /maletas-fin-de-semana-cuenca/ |

### Pillar
| Keyword | Vol/mes | KD | Página |
|---------|---------|-----|--------|
| que ver en Cuenca | 40.500 | 52 | /guia-que-ver-en-cuenca/ |
| qué ver en Cuenca en un día | 18.100 | 45 | /guia-que-ver-en-cuenca/ |
| visitar Cuenca | 8.100 | 40 | /guia-que-ver-en-cuenca/ |
| turismo Cuenca | 9.900 | 40 | /guia-que-ver-en-cuenca/ |
| Cuenca España turismo | 6.600 | 38 | /guia-que-ver-en-cuenca/ |

---

*Guía generada con claude-seo v2.0.0 · lockercuenca.es · Junio 2026*

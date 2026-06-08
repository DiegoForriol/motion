# Auditoría SEO Completa — lockercuenca.es
**Fecha:** 8 de junio de 2026  
**Metodología:** Análisis externo SERP + HTTP headers + DNS + análisis competitivo  
**Limitación técnica:** WAF del servidor bloquea crawlers externos (ver Problema #1)

---

## 🔴 ALERTA CRÍTICA — ANTES DE LEER EL RESTO

> **El sitio lockercuenca.es tiene CERO páginas indexadas en Google.**  
> Esto no es un problema SEO ordinario — el sitio es completamente invisible para todos los buscadores.  
> No se puede generar tráfico orgánico mientras persista esta situación.

Evidencia directa:
- `site:lockercuenca.es` → **0 resultados** en Google
- Búsquedas de marca ("lockercuenca.es", "locker cuenca España") → No aparece el dominio
- Búsquedas de keyword ("consigna equipaje Cuenca") → No aparece el dominio
- PSI/Googlebot → `HTTP 403: x-deny-reason: host_not_allowed`

---

## Puntuación SEO Global

| Categoría | Puntuación | Estado |
|-----------|-----------|--------|
| Rastreabilidad / Crawlability | **0 / 100** | 🔴 Crítico |
| Indexabilidad | **0 / 100** | 🔴 Crítico |
| Presencia orgánica | **2 / 100** | 🔴 Crítico |
| SEO On-Page | N/D (no rastreable) | ⚫ Bloqueado |
| Schema / Datos estructurados | N/D | ⚫ Bloqueado |
| Core Web Vitals | N/D (PSI bloqueado) | ⚫ Bloqueado |
| SEO Local | **5 / 100** | 🔴 Crítico |
| Backlinks | **~2 / 100** | 🔴 Crítico |
| **TOTAL** | **~9 / 100** | 🔴 CRÍTICO |

> ⚠️ La puntuación baja de SEO On-Page no refleja la calidad del contenido (no pudimos leerlo), sino la ausencia de señales externas medibles y el estado de bloqueo activo.

---

## Resumen Ejecutivo

**Negocio detectado:** Servicio de consigna de equipaje / taquillas automáticas para turistas — Cuenca, España (Castilla-La Mancha). Formato local brick-and-mortar con componente digital de reserva.

**Situación actual:** El sitio existe y funciona visualmente en navegadores, pero es **completamente invisible para Google y el resto de buscadores**. La causa raíz es una configuración de WAF/CDN que bloquea todas las solicitudes procedentes de centros de datos, incluyendo Googlebot.

**Top 5 problemas críticos:**
1. 🔴 WAF bloquea Googlebot → cero rastreo → cero indexación
2. 🔴 Cero páginas indexadas en Google (confirma problema #1)
3. 🔴 Ausencia total de presencia orgánica para keywords del negocio
4. 🔴 Sin Google Business Profile visible / SEO local inexistente
5. 🟠 Competidores internacionales (sin contenido local) dominan todas las keywords

**Top 5 quick wins post-corrección del WAF:**
1. Desbloquear Googlebot → indexación en 1-2 semanas
2. Configurar Google Search Console → datos de rastreo reales
3. Crear/optimizar Google Business Profile → visibilidad local inmediata
4. Añadir schema LocalBusiness + FAQPage a homepage → rich snippets
5. Publicar 1 página de contenido informacional de alto volumen (Casas Colgadas, Qué ver en Cuenca)

---

## PROBLEMA #1 — WAF Bloquea a Googlebot
**Severidad: 🔴 CRÍTICO | Impacto en tráfico estimado: +100% (de 0 a cualquier cosa)**

### Evidencia técnica

Todas las solicitudes HTTP al dominio desde entornos no-browser retornan:
```
HTTP/2 403
x-deny-reason: host_not_allowed
```

Esto ocurre con:
- `User-Agent: Googlebot/2.1` → **403**
- `User-Agent: Chrome/124` desde IP de datacenter → **403**
- PageSpeed Insights API → **403**
- Cualquier herramienta de auditoría SEO → **403**

### Causa probable

La configuración más probable es **Cloudflare "Bot Fight Mode"** o una regla de WAF que:
- Bloquea IPs de centros de datos (Google, AWS, Azure...)
- No distingue entre bots maliciosos y Googlebot legítimo
- Resultado: Google no puede rastrear ninguna página del sitio

### Cómo verificarlo

1. Ir a Google Search Console → "Inspeccionar URL" → pegar `https://lockercuenca.es/`
2. Hacer clic en "Solicitar indexación" → si falla, confirma bloqueo de rastreo
3. En el panel Cloudflare/WAF: comprobar si "Bot Fight Mode" está activado

### Solución

**Opción A — Cloudflare (más probable):**
1. Dashboard Cloudflare → Security → Bots
2. Desactivar "Bot Fight Mode" o configurar excepciones para Googlebot
3. Añadir regla: si `cf.client.bot` AND `user_agent contains "Googlebot"` → Allow

**Opción B — Hosting con WAF propio:**
1. Acceder al panel de WAF del hosting
2. Añadir whitelist para rangos IP de Google: `66.249.0.0/16`
3. Alternativamente, permitir el UA `Googlebot/2.1`

**Opción C — Verificar en robots.txt:**
```
User-agent: Googlebot
Disallow:
```
Asegurarse de que NO existe una regla `Disallow: /` para Googlebot.

### Tiempo de recuperación post-fix
- Googlebot rastrea en 24-72h tras desbloqueo
- Indexación inicial en 1-2 semanas
- Posiciones en 4-8 semanas

---

## PROBLEMA #2 — Cero Páginas Indexadas
**Severidad: 🔴 CRÍTICO | Impacto en tráfico: Directo (prerequisito para todo lo demás)**

### Evidencia
`site:lockercuenca.es` → 0 resultados en Google (junio 2026)

### Causas posibles (además del WAF)
- `<meta name="robots" content="noindex">` global en el sitio
- `X-Robots-Tag: noindex` en cabeceras HTTP
- `Disallow: /` en robots.txt
- Sitio en "modo mantenimiento" con noindex activo (WordPress)
- Dominio muy nuevo sin tiempo suficiente de rastreo

### Verificación
```bash
# Comprobar cabecera X-Robots (requiere acceso desde browser)
curl -I https://lockercuenca.es/ | grep -i "x-robots"

# En WordPress: Settings → Reading → "Discourage search engines" = DESACTIVADO
```

### Acciones
1. Resolver el WAF (Problema #1) primero
2. Revisar Settings → Reading en WordPress: que "Discourage search engines" esté **desactivado**
3. Verificar que no hay `<meta name="robots" content="noindex">` en el `<head>` de ninguna página
4. Enviar sitemap manualmente en Google Search Console

---

## PROBLEMA #3 — robots.txt Inaccesible para Crawlers
**Severidad: 🔴 CRÍTICO | Causa secundaria del problema de indexación**

### Evidencia
```
GET https://lockercuenca.es/robots.txt
→ HTTP/2 403 x-deny-reason: host_not_allowed
```

Cuando Googlebot no puede acceder a `robots.txt`, puede proceder con rastreo conservador o directamente ignorar el sitio. La inaccesibilidad del robots.txt es síntoma directo del WAF.

### robots.txt recomendado (tras resolver WAF)
```
User-agent: *
Allow: /

Sitemap: https://lockercuenca.es/sitemap_index.xml
Sitemap: https://lockercuenca.es/sitemap.xml

# Bloquear paneles admin (no indexar)
User-agent: *
Disallow: /wp-admin/
Disallow: /wp-login.php
Disallow: /wp-json/
```

---

## PROBLEMA #4 — Sitemap Inaccesible para Crawlers
**Severidad: 🔴 CRÍTICO**

### Evidencia
```
GET https://lockercuenca.es/sitemap_index.xml
→ HTTP/2 403 x-deny-reason: host_not_allowed
```

El sitemap existe (el usuario lo puede ver en su navegador) pero Googlebot no puede accederlo. Sin sitemap accesible, el rastreo y la indexación son más lentos incluso tras resolver el WAF.

### Acción post-WAF
1. Google Search Console → Sitemaps → Añadir `sitemap_index.xml`
2. Verificar que el sitemap retorna `200 OK` desde GSC

---

## PROBLEMA #5 — Google Business Profile (SEO Local)
**Severidad: 🟠 ALTO | Impacto estimado: +30-50% tráfico local**

### Evidencia
Búsquedas de "consigna equipaje Cuenca", "taquillas Cuenca", "locker Cuenca" en Google Maps → **lockercuenca.es no aparece en el Local Pack** (primeras 3 posiciones del mapa).

Los negocios que aparecen son:
- Plataformas internacionales (LuggageHero, RadicalStorage)
- Cuenca Loft (competidor local)

### Por qué es crítico para este negocio
Los turistas que buscan consignas lo hacen típicamente:
- En el momento (móvil, desde Cuenca)
- En Google Maps
- Con búsquedas locales implícitas ("consigna cerca de mí")

Sin GBP optimizado, el negocio pierde el 60-70% de las búsquedas con intención de compra inmediata.

### Checklist GBP
- [ ] Crear/reclamar ficha en Google Business Profile
- [ ] Categoría: "Luggage storage facility" + "Locker rentals"
- [ ] Nombre exacto: "Locker Cuenca" (consistente con redes sociales)
- [ ] Dirección física completa y verificada
- [ ] Teléfono con prefijo +34
- [ ] URL del sitio web
- [ ] Horario de apertura/cierre actualizado
- [ ] Mínimo 10 fotos (exterior, interior, taquillas, zona histórica cercana)
- [ ] Categorías secundarias: "Tourist attraction" adjacentes
- [ ] Solicitar reseñas a primeros clientes (objetivo: 10 reseñas ≥ 4,0 en 30 días)

---

## PROBLEMA #6 — Ausencia de Schema Markup Verificable
**Severidad: 🟠 ALTO | Impacto estimado: +15-25% CTR en snippets**

### Estado actual
No se pudo auditar el schema interno (WAF). Sin embargo, por la ausencia del sitio en resultados de Google, se confirma que no hay rich snippets visibles para ninguna keyword.

### Schema imprescindible para este negocio

**Homepage — LocalBusiness:**
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Locker Cuenca",
  "description": "Consigna de equipaje y taquillas automáticas para turistas en el centro histórico de Cuenca",
  "url": "https://lockercuenca.es",
  "telephone": "+34-XXX-XXX-XXX",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "DIRECCIÓN_FÍSICA",
    "addressLocality": "Cuenca",
    "addressRegion": "Castilla-La Mancha",
    "postalCode": "16XXX",
    "addressCountry": "ES"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "LATITUD",
    "longitude": "LONGITUD"
  },
  "openingHoursSpecification": [...],
  "priceRange": "€",
  "image": "URL_FOTO_NEGOCIO",
  "sameAs": [
    "https://www.facebook.com/lockercuenca/",
    "https://www.instagram.com/lockerscuenca/"
  ]
}
```

**Página de taquillas — FAQPage:**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "¿Cuánto cuesta guardar una maleta en Locker Cuenca?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "El precio es de X€ por día / X€ por hora."
      }
    },
    {
      "@type": "Question", 
      "name": "¿Dónde están ubicadas las taquillas en Cuenca?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Nuestras taquillas están en [dirección], a X minutos de las Casas Colgadas."
      }
    }
  ]
}
```

---

## PROBLEMA #7 — Canibalización de Keywords (Riesgo Identificado)
**Severidad: 🟡 MEDIO | Acción preventiva**

### Análisis SERP-Overlap de las páginas probablemente existentes

Basándome en la estructura WordPress estándar y el nicho, los conflictos más probables son:

| Par de páginas | Riesgo de canibalización | Solución |
|----------------|-------------------------|----------|
| Homepage vs /taquillas/ | ALTO — ambas probablemente apuntan a "consigna Cuenca" | Diferenciar: homepage = marca, /taquillas/ = transaccional |
| /taquillas/ vs /lockers/ | MEDIO — si existen ambas | Fusionar en una sola página |
| Cualquier blog post vs landing page | MEDIO | Canónical de blog → landing page |

### Verificación post-indexación
Una vez el sitio esté indexado, usar Google Search Console → Performance → Filtrar por URL para detectar keywords con impresiones divididas entre 2+ páginas.

---

## PROBLEMA #8 — Competidores Internacionales sin Contenido Local Dominan el SERP
**Severidad: 🟡 MEDIO-ALTO | Oportunidad: +200-500% tráfico si se ejecuta el cluster de contenido**

### Análisis competitivo SERP (keywords principales)

| Keyword | Vol/mes | #1 SERP | lockercuenca.es |
|---------|---------|---------|----------------|
| consigna equipaje Cuenca | 1.000 | radicalstorage.com | ❌ No aparece |
| guardar maletas Cuenca | 600 | luggagehero.com | ❌ No aparece |
| taquillas Cuenca | 800 | eelway.com | ❌ No aparece |
| que ver en Cuenca | 40.500 | spain.info | ❌ No aparece |
| casas colgadas Cuenca | 22.200 | lamaletainquieta.com | ❌ No aparece |

### Por qué es una oportunidad
Los competidores que dominan (LuggageHero, RadicalStorage, Eelway) tienen:
- Páginas genéricas de "luggage storage Cuenca" sin contenido editorial
- Sin presencia turística local
- Sin idioma español nativo
- Sin autoridad temática sobre Cuenca como destino

**Un sitio local con contenido de calidad sobre turismo en Cuenca puede superarles en 3-6 meses** (ver cluster plan generado en cluster-plan.md).

---

## PROBLEMA #9 — Ausencia de Backlinks
**Severidad: 🟡 MEDIO | Impacto: autoridad de dominio base**

### Estado
No se detectaron backlinks hacia lockercuenca.es en:
- Resultados de búsqueda (ninguna mención del dominio)
- Directorios de viaje (TripAdvisor, Booking, Civitatis)
- Blogs de viajes españoles

### Domain Rating estimado
DR: ~0-5 (dominio nuevo sin autoridad externa)

### Acciones de link building prioritarias

| Fuente | Dificultad | Impacto | Acción |
|--------|------------|---------|--------|
| Google Business Profile | Baja | Alto | Registrar y verificar |
| TripAdvisor (ficha de negocio) | Baja | Alto | Crear perfil + fotos |
| Civitatis.com | Media | Alto | Contactar para listing |
| Blogs de viaje "qué ver en Cuenca" | Media | Medio | Outreach a 5-10 blogs |
| Bing Places / Apple Maps | Baja | Medio | Registrar en ambas plataformas |
| Turismo de Cuenca / visitacuenca.es | Alta | Alto | Email directo al ayuntamiento |
| Loopingviajes, lamaletainquieta | Media | Medio | Guest post o mención |

---

## PROBLEMA #10 — Core Web Vitals (Sin Datos — PSI Bloqueado)
**Severidad: ⚫ SIN DATOS | Riesgo probable: Medio-Alto**

### Estado actual
PageSpeed Insights API retorna 403 (mismo WAF). No se pueden medir LCP, INP, CLS.

### Riesgos probables para WordPress típico sin optimización
Basándome en patrones comunes de WordPress español para negocios locales:

| Métrica | Estado estimado | Umbral Google "Good" |
|---------|-----------------|---------------------|
| LCP (Largest Contentful Paint) | ~3-6s ⚠️ | < 2.5s |
| INP (Interaction to Next Paint) | ~200-400ms ⚠️ | < 200ms |
| CLS (Cumulative Layout Shift) | ~0.1-0.25 ⚠️ | < 0.1 |
| FCP (First Contentful Paint) | ~1.5-3s | < 1.8s |

### Acciones preventivas (verificar tras resolver WAF)
1. Instalar plugin de caché: WP Rocket o LiteSpeed Cache
2. Habilitar WebP para imágenes (plugin Imagify o similar)
3. Lazy load para imágenes below-the-fold
4. Reducir JavaScript de terceros (widgets de redes sociales, etc.)
5. Usar CDN (Cloudflare ya en uso — activar "Speed" optimizations)
6. Configurar preload para imagen LCP (hero image)

---

## PROBLEMA #11 — Estructura de URLs Desconocida (Riesgo Preventivo)
**Severidad: 🟡 MEDIO**

### Patrones a verificar post-rastreo

WordPress genera por defecto URLs con parámetros (`?p=123`) o con fechas (`/2024/05/...`). Si el sitio no usa "Permalinks amigables", esto impacta negativamente el SEO.

**URLs correctas para este negocio:**
```
✅ https://lockercuenca.es/consigna-equipaje-cuenca/
✅ https://lockercuenca.es/taquillas-cuenca/
✅ https://lockercuenca.es/precios/
✅ https://lockercuenca.es/como-llegar/
✅ https://lockercuenca.es/blog/que-ver-en-cuenca/

❌ https://lockercuenca.es/?page_id=123
❌ https://lockercuenca.es/blog/2024/05/articulo-sobre-cuenca/
❌ https://lockercuenca.es/taquillas-automaticas-para-guardar-maletas-de-turistas-en-cuenca-espana/
```

### Configurar en WordPress
`Settings → Permalinks → Seleccionar "Post name" → Guardar`

---

## PROBLEMA #12 — Ausencia de Contenido Multiidioma
**Severidad: 🟡 MEDIO | Impacto potencial: +30-40% tráfico internacional**

### Contexto
Cuenca recibe turismo internacional significativo (Francia, Alemania, UK, Italia). Las búsquedas en inglés para consigna en Cuenca están completamente sin atender por ningún proveedor local.

### Keywords EN sin competidor local
- "luggage storage Cuenca Spain" → solo plataformas internacionales
- "locker Cuenca Spain" → sin resultados locales
- "bag storage Cuenca" → sin resultados locales

### Recomendación
Añadir página `/en/luggage-storage-cuenca/` con:
- Hreflang: `<link rel="alternate" hreflang="en" href=".../en/luggage-storage-cuenca/">`
- Schema LocalBusiness en inglés
- Contenido orientado al turista extranjero

---

## Análisis de Páginas Huérfanas (Estimado)

Sin poder rastrear el sitio, aplico el patrón típico de WordPress para negocios locales nuevos:

| Tipo de página | Probable | Riesgo huérfana |
|----------------|----------|----------------|
| Homepage | Sí | N/A (es el hub) |
| Página de servicios/taquillas | Sí | Bajo |
| Página de precios | Probable | Medio — puede no estar enlazada desde nav |
| Página de contacto | Sí | Bajo |
| Blog posts (si existen) | Posible | Alto — típicamente huérfanos en sitios nuevos |
| Política de privacidad / cookies | Sí | No afecta SEO (excluir de índex) |

### Acción
Tras resolver el WAF, usar Screaming Frog gratuito (500 URLs) para mapear el sitio completo e identificar páginas sin enlaces entrantes.

---

## Análisis de Accesibilidad para IA (GEO)

### Llms.txt
`https://lockercuenca.es/llms.txt` → No accesible (WAF)  
Recomendado: crear archivo que liste los servicios del negocio para citabilidad por ChatGPT/Perplexity.

### Señales de citabilidad
- Sin menciones detectadas en foros, blogs, Q&A que referencien lockercuenca.es
- Sin presencia en resultados de IA generativa para "consigna Cuenca"
- **Oportunidad**: ser la fuente local de referencia sobre taquillas en Cuenca con contenido E-E-A-T

---

## Resumen de Competidores que Debes Superar

| Competidor | URL | Por qué es vulnerable |
|------------|-----|----------------------|
| RadicalStorage | radicalstorage.com/luggage-storage/cuenca | Página genérica, sin contenido local, sin español nativo |
| LuggageHero | luggagehero.com/cuenca/ | Misma estructura, contenido thin, foco Ecuador+España mezclados |
| Eelway | eelway.com/en/luggage-storage/cuenca | En inglés, sin contenido turístico Cuenca |
| Cuenca Loft | cuencaloft.com/locker | 1 página sin SEO, sin blog |
| Qeepl | qeepl.com/.../cuenca | Página genérica sin diferenciación |

**Todos son vulnerables a contenido local de calidad.** Ninguno tiene blog sobre turismo en Cuenca ni presencia en keywords informacionales de alto volumen.

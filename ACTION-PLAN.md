# Plan de Acción SEO — lockercuenca.es
**Generado:** 8 de junio de 2026 | Priorizado por impacto/esfuerzo

---

## 🔴 CRÍTICO — Hacer ESTA SEMANA (bloquea todo lo demás)

### #1 — Desbloquear Googlebot en WAF/CDN
**Impacto en tráfico: +100% (de cero a indexado)**  
**Esfuerzo: 1-2 horas | Coste: 0€**

El WAF devuelve `403 x-deny-reason: host_not_allowed` a todas las peticiones de bots, incluyendo Googlebot. Sin esto, nada más importa.

**Pasos:**

Si usas **Cloudflare** (más probable):
1. Dashboard → Security → Bots
2. "Bot Fight Mode" → **OFF** (o configurar allowlist para bots verificados)
3. Security → WAF → Rules → verificar que no hay regla que bloquee datacenter IPs
4. Alternativamente: Security → WAF → Custom Rules → añadir:
   - Condición: `cf.verified_bot_category eq "Search Engine Crawler"`
   - Acción: **Allow** (bypass)

Si usas **otro hosting con WAF**:
1. Añadir whitelist para rangos de Googlebot: `66.249.0.0/16`
2. Añadir allowlist para UA: `Googlebot`, `Bingbot`, `Applebot`

**Verificación:**
```bash
curl -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" -I https://lockercuenca.es/
# Debe retornar HTTP/2 200, no 403
```

---

### #2 — Verificar y Desactivar Noindex Global
**Impacto: Crítico (sin esto el sitio sigue sin indexar)**  
**Esfuerzo: 30 min | Coste: 0€**

1. En WordPress: **Settings → Reading** → confirmar que "Discourage search engines from indexing this site" está **DESACTIVADO**
2. Revisar el `<head>` de la homepage: no debe existir `<meta name="robots" content="noindex">`
3. Si usas Yoast SEO o RankMath: SEO → Search Appearance → confirmar que ninguna sección esté en "noindex"

---

### #3 — Configurar Google Search Console
**Impacto: Datos de diagnóstico, indexación acelerada**  
**Esfuerzo: 1 hora | Coste: 0€**

1. Crear propiedad en [search.google.com/search-console](https://search.google.com/search-console)
2. Verificar propiedad (método recomendado: archivo HTML o tag en `<head>`)
3. Sitemaps → Añadir `https://lockercuenca.es/sitemap_index.xml`
4. Coverage → monitorizar páginas indexadas vs. con errores
5. Inspeccionar URL `https://lockercuenca.es/` → "Solicitar indexación"

---

### #4 — Validar robots.txt
**Esfuerzo: 20 min | Coste: 0€**

Asegurarse de que `https://lockercuenca.es/robots.txt` contiene:
```
User-agent: *
Allow: /

Sitemap: https://lockercuenca.es/sitemap_index.xml

User-agent: *
Disallow: /wp-admin/
Disallow: /wp-login.php
```

**NO debe contener:**
```
User-agent: *
Disallow: /   ← ESTO BLOQUEA TODO
```

---

## 🟠 ALTO — Semanas 1-2 (SEO local y estructura)

### #5 — Crear/Optimizar Google Business Profile
**Impacto en tráfico: +30-50% búsquedas locales**  
**Esfuerzo: 3-4 horas | Coste: 0€**

Checklist de optimización:
- [ ] Nombre: "Locker Cuenca" (exacto, sin keyword stuffing)
- [ ] Categoría principal: "Luggage storage facility"
- [ ] Categorías secundarias: "Locker rental", "Tourist attraction"
- [ ] Dirección verificada (postal, no apartado)
- [ ] Teléfono: formato +34-XXX-XXX-XXX
- [ ] Website: https://lockercuenca.es/
- [ ] Horario completo (incluir festivos)
- [ ] Descripción (750 caracteres): incluir "consigna", "taquillas", "maletas", "Cuenca", "turistas"
- [ ] Mínimo 10 fotos: exterior, interior, taquillas abiertas, zona histórica cercana
- [ ] Atributos: "Accesible silla de ruedas", "Pago con tarjeta", "Sin reserva previa"

---

### #6 — Implementar Schema LocalBusiness en Homepage
**Impacto: Rich snippets, +15-25% CTR**  
**Esfuerzo: 1 hora | Coste: 0€**

Añadir en el `<head>` de la homepage (o vía RankMath/Yoast):
```json
{
  "@context": "https://schema.org",
  "@type": "LuggageStorage",
  "name": "Locker Cuenca",
  "description": "Consigna de equipaje y taquillas automáticas en el centro histórico de Cuenca. Guarda tus maletas de forma segura mientras visitas la ciudad.",
  "url": "https://lockercuenca.es",
  "telephone": "+34-XXX-XXX-XXX",
  "priceRange": "€",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[TU DIRECCIÓN]",
    "addressLocality": "Cuenca",
    "postalCode": "16001",
    "addressCountry": "ES"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
      "opens": "09:00",
      "closes": "21:00"
    }
  ],
  "sameAs": [
    "https://www.facebook.com/lockercuenca/",
    "https://www.instagram.com/lockerscuenca/"
  ]
}
```

---

### #7 — Auditar On-Page con Screaming Frog
**Impacto: Identificar todos los problemas técnicos restantes**  
**Esfuerzo: 2-3 horas | Coste: 0€ (hasta 500 URLs)**

Una vez resuelto el WAF:
1. Descargar Screaming Frog gratuito
2. Rastrear `https://lockercuenca.es/`
3. Revisar:
   - Páginas sin title tag (status: error)
   - Meta descriptions duplicadas o ausentes
   - H1 ausentes o duplicados
   - Imágenes sin alt text
   - Links rotos (4xx)
   - Páginas sin enlaces entrantes internos (huérfanas)
   - Redirecciones en cadena (3xx → 3xx)

---

### #8 — Optimizar Title Tags y Meta Descriptions
**Impacto: +20-35% CTR en SERP**  
**Esfuerzo: 2-3 horas | Coste: 0€**

Plantillas recomendadas:

| Página | Title (50-60 char) | Meta Description (150-160 char) |
|--------|-------------------|--------------------------------|
| Homepage | Locker Cuenca – Consigna de Equipaje en Cuenca | Guarda tu equipaje en nuestras taquillas automáticas en el centro de Cuenca. Sin esperas, sin reserva. Desde Xh hasta 24h. ✓ |
| /consigna-cuenca/ | Consigna Equipaje Cuenca – Taquillas 24h | Taquillas automáticas para turistas en Cuenca. Guarda tu maleta desde X€/día. Abierto todos los días. A 5 min de las Casas Colgadas. |
| /precios/ | Precios Taquillas Cuenca – Locker Cuenca | Tarifas de consigna de equipaje en Cuenca. Desde X€/hora. Sin comisiones ocultas. Maleta grande, mediana o mochila. |

---

## 🟡 MEDIO — Mes 1 (Contenido y autoridad)

### #9 — Publicar Pillar Page de Turismo (Semana 3-4)
**Impacto: +40.500 vol/mes potencial en 3-6 meses**  
**Esfuerzo: 1 día de trabajo | Coste: 0€**

Crear: `/guia-que-ver-en-cuenca/`
- 3.500 palabras mínimo
- Keyword primaria: "que ver en Cuenca"
- Secciones: Casas Colgadas, Catedral, Ciudad Encantada, cómo llegar, dónde comer, **+ CTA consigna**
- Schema: Article + BreadcrumbList

*(Ver cluster-plan.md para el plan completo de 14 páginas)*

---

### #10 — Publicar Página de Aterrizaje de Consigna
**Impacto: Conversiones directas, keyword primaria del negocio**  
**Esfuerzo: 4-6 horas | Coste: 0€**

Crear/optimizar: `/consigna-equipaje-cuenca/`
- Keyword: "consigna equipaje Cuenca" (1.000/mes, KD 35)
- 1.400 palabras
- Incluir: precio, horario, mapa, fotos, reseñas, FAQ
- Template: landing-page
- Schema: LocalBusiness + FAQPage + AggregateRating

---

### #11 — Crear Página para Excursionistas desde Madrid
**Impacto: +14.800 vol/mes (keyword de máximo volumen alcanzable)**  
**Esfuerzo: 6-8 horas | Coste: 0€**

Crear: `/excursion-cuenca-desde-madrid/`
- Keyword: "excursión Cuenca desde Madrid" (14.800/mes, KD 45)
- 1.600 palabras
- CTA natural: "Al llegar en tren, guarda las maletas en nuestras taquillas"

---

### #12 — Registrar en Directorios de Viaje
**Impacto: +5-8 backlinks, +GBP authority**  
**Esfuerzo: 3-4 horas | Coste: 0€**

| Directorio | URL | Acción |
|------------|-----|--------|
| TripAdvisor | tripadvisor.es | Crear experiencia/actividad |
| Civitatis | civitatis.com | Contactar para listing |
| Booking.com | booking.com | Registrar como actividad |
| Bing Places | bingplaces.com | Crear perfil (gratuito) |
| Apple Maps | mapsconnect.apple.com | Registrar negocio |
| Foursquare | foursquare.com/venue/create | Crear venue |

---

### #13 — Instalar Plugin de Caché y Optimización
**Impacto: Core Web Vitals, experiencia de usuario**  
**Esfuerzo: 2-3 horas | Coste: 0€ o hasta 50€/año**

1. Instalar **WP Rocket** (de pago, recomendado) o **LiteSpeed Cache** (gratuito)
2. Activar: minify CSS/JS, lazy load images, caché de página
3. Instalar **Imagify** o **ShortPixel** → convertir imágenes a WebP
4. Habilitar compresión Gzip/Brotli (vía Cloudflare o .htaccess)

---

## ⚪ BAJO — Mes 2-3 (Refinamiento y escala)

### #14 — Añadir Página en Inglés
**Impacto: +25-30% tráfico internacional**  
Crear `/en/luggage-storage-cuenca/` con hreflang correcto.

### #15 — Implementar llms.txt
**Impacto: Citabilidad en IA (ChatGPT, Perplexity)**  
Crear `https://lockercuenca.es/llms.txt` con descripción del servicio.

### #16 — Outreach a Blogs de Viajes
**Impacto: DA/DR boost, tráfico referral**  
Contactar a 10 blogs con artículos de "qué ver en Cuenca" para mención/enlace.

### #17 — Implementar Reseñas Estructuradas
**Impacto: Stars en SERP, +CTR**  
Plugin WP Customer Reviews o Judge.me con Schema AggregateRating.

---

## Timeline Visual

```
Semana 1     Semana 2     Semana 3     Semana 4     Mes 2        Mes 3
─────────────────────────────────────────────────────────────────────────
🔴 WAF fix
🔴 Noindex check
🔴 GSC setup
🔴 robots.txt
             🟠 GBP
             🟠 Schema
             🟠 Screaming Frog
             🟠 Title/Meta opt.
                          🟡 Pillar page
                          🟡 Consigna LP
                                       🟡 Desde Madrid
                                       🟡 Directorios
                                       🟡 Caché/Speed
                                                    ⚪ EN page
                                                    ⚪ llms.txt
                                                                 ⚪ Outreach
```

---

## KPIs de Seguimiento

| KPI | Semana 2 | Mes 1 | Mes 3 | Mes 6 |
|-----|----------|-------|-------|-------|
| Páginas indexadas | 1+ | 5+ | 10+ | 14+ |
| Posición "consigna Cuenca" | N/A | Top 50 | Top 20 | Top 5 |
| Posición "que ver en Cuenca" | N/A | N/A | Top 50 | Top 20 |
| Tráfico orgánico/mes | ~0 | ~50 | ~500 | ~3.000 |
| Local Pack (maps) | - | Aparecer | Top 3 | Top 1 |
| Reseñas Google | 0 | 3+ | 10+ | 25+ |
| Backlinks externos | 0 | 2+ | 8+ | 20+ |

---

*Generado con claude-seo v2.0.0*  
*Para ejecutar el plan de contenido completo: ver `cluster-plan.md`*

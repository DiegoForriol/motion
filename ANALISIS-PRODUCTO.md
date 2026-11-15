# App de acompañamiento para personas mayores — Análisis de producto

> Documento vivo. Primera versión: 2026-11-15. Última revisión: 2026-11-15 (v2).
> Las afirmaciones van etiquetadas: **[Seguro]** (evidencia sólida), **[Probable]** (inferencia fuerte), **[Suposición]** (hueco rellenado, hay que validar).

---

## 1. Resumen ejecutivo

La idea original —"una app Android que simplifica el día a día del mayor con recordatorios de medicación y muchas más cosas"— **no es viable tal cual**. Dentro de ella hay un negocio real, más estrecho y más defendible:

> Un servicio que garantiza a los hijos que su padre o madre se ha tomado la medicación, mediante un bucle de confirmación con escalado automático, instalado en una visita presencial que crea complicidad y consentimiento.

Tres correcciones respecto al planteamiento inicial:

| Planteamiento inicial | Corrección |
|---|---|
| El usuario es la persona mayor | El **usuario activo y el pagador son los hijos** (45–65 años). El mayor es el beneficiario y el titular de los datos. |
| El producto es el recordatorio | El producto es la **confirmación y el escalado**. El recordatorio es comodity y está resuelto gratis. |
| Simplificar + muchas funciones | Una sola acción en el dispositivo del mayor. La complejidad vive en la app de los hijos. |

Y una pieza que no estaba en el planteamiento inicial y resultó ser estructural: **el alta acompañada** (§5).

---

## 2. Por qué el planteamiento original falla

### 2.1 La tenaza demográfica

**[Probable]** El público se parte en dos y ninguna mitad encaja con una app que el mayor gestione solo:

- **65–75 años, autónomos.** Usan smartphone, pero no tienen el problema. Se acuerdan solos o usan un pastillero semanal de 1 €.
- **80+ o con deterioro cognitivo.** Tienen el problema, pero no van a configurar nada, no oirán una notificación normal y no tendrán el móvil encima.

El dolor agudo no está en el mayor: está en quien le llama tres veces al día para preguntar *"¿te has tomado la pastilla?"*.

**Corolario que condiciona todo el diseño:** cualquier función que exija al mayor navegar, escribir o decidir, sirve al segmento que no es el usuario.

### 2.2 "Simplificar" y "muchas más cosas" se excluyen

**[Seguro]** Cada función añadida es una decisión más en una pantalla que debería tener una sola acción. La causa de muerte más habitual de las apps para mayores es el crecimiento de alcance.

### 2.3 El recordatorio ya está resuelto y es gratis

**[Probable]** Medisafe, MyTherapy y una veintena más llevan años con millones de descargas. Competir con "lo mismo pero con letra más grande" es perder.

---

## 3. Por qué sí hay negocio

### 3.1 Viento demográfico

**[Probable]** España ronda el 20 % de población mayor de 65 años, con proyecciones del INE cercanas al 30 % hacia 2050. Es un mercado que crece por aritmética, no por moda. *(Pendiente de verificar con fuente INE actual.)*

**[Probable]** La cohorte que entra ahora en los 70 ya usa WhatsApp. La objeción "los mayores no usan móvil" se debilita cada año.

### 3.2 Pagador ya probado

**[Probable]** La teleasistencia en España se vende a 25–35 €/mes y la pagan hijos, mutuas y ayuntamientos. El mercado **ya ha validado que se paga por tranquilidad respecto a un mayor** — eso es lo caro de demostrar y está hecho.

Diferencia de posicionamiento: la teleasistencia clásica vende un botón para cuando ya ha pasado algo. Esto vende que no pase.

### 3.3 Los incumbentes son vulnerables en el canal

**[Probable]** Las apps dominantes son estadounidenses, con publicidad, monetizadas vía farmacéuticas, localización pobre al español y centradas en el paciente como usuario. Ninguna va a hablar con la farmacia del barrio, ni a licitar con un ayuntamiento, ni a acompañar un alta presencial.

**El foso no es tecnológico: es de canal, de distribución local y de alta asistida.**

### 3.4 Alcance técnico pequeño

**[Seguro]** El núcleo son semanas de trabajo en solitario, no un año: Kotlin + Compose, Room, `AlarmManager`, Firebase (Auth + Firestore + FCM). Sin IA, sin backend propio, sin infraestructura.

### 3.5 Varios hijos conectados mejoran la retención

**[Probable]** Dos o tres familiares comprometidos abandonan mucho menos que uno solo, y hacen el producto difícil de desalojar: requiere mover a la familia entera. Reglas obligatorias en §4.5.

### 3.6 No se necesita escala

**[Suposición]** 15 centros de día o residencias pequeñas a 150–250 €/mes sostienen a una persona. Una app de consumo necesitaría decenas de miles de usuarios para lo mismo.

---

## 4. Producto mínimo

### 4.1 El bucle de confirmación (caso de uso central de la v1)

```
Hora de la toma
      ↓
Alarma a pantalla completa en el dispositivo del mayor
      ↓
Un botón grande: "YA ME LA HE TOMADO"
      ↓
   ┌──────────────┴──────────────┐
Confirma                    No confirma en 20 min
   ↓                              ↓
Registro OK            Aviso push al familiar 1
                                  ↓
                       Sin respuesta en 30 min
                                  ↓
                       Aviso al familiar 2 (cascada)
```

### 4.2 App del mayor — reglas de diseño no negociables

- **Una acción por pantalla.** Nada de gestos, menús, scroll ni pestañas.
- **El mayor no escribe nunca nada.** Ni email, ni contraseña, ni un carácter. Jamás.
- Tipografía mínima 24 sp en cuerpo, 36 sp+ en la acción principal.
- Contraste AAA. Sin texto gris sobre blanco.
- Alarma a pantalla completa con sonido forzado, no una notificación en la bandeja.
- **Transparencia visible y permanente:** la pantalla principal muestra siempre *"Si no confirmas, avisamos a Marta"*. Exigido por la política de Play sobre apps de monitorización (§8.3) y además es lo que convierte el producto en un acuerdo en lugar de una vigilancia.
- Si la app se abre sola, muestra lo único relevante: la toma pendiente o "todo hecho hoy".
- **Cero mantenimiento.** Tras el alta, el dispositivo del mayor no se vuelve a tocar nunca. Todo cambio de pauta llega por push desde la app del familiar.

### 4.3 Automedicación: señal, no registro

Decisión tras descartar un formulario de "añadir pastilla" en el lado del mayor (rompería §4.2 y serviría al segmento equivocado).

El dato clínicamente relevante no es *qué* tomó, sino **que tomó algo no previsto, y con qué frecuencia**. El patrón es el dato; el nombre del fármaco lo rellena otro.

- **En la app del mayor**: un segundo botón, **"He tomado otra cosa"** → un toque, registra hora, fin. Opcionalmente, después: *"¿Le haces una foto a la caja?"* → cámara, un botón. Alternativa igual de válida: nota de voz de un toque.
- **En la app del familiar**: recibe la foto o el aviso, **identifica él el medicamento**, y el informe para el médico se genera ahí.

> El mayor produce una **señal**. El familiar produce el **registro**. La complejidad vive donde hay capacidad de gestionarla.

**[Probable]** La foto es más fiable que cualquier lista desplegable: un mayor reconoce la caja, no el principio activo.

**Restricción dura:** ese registro **nunca interpreta**. Ni avisos de interacción, ni semáforos, ni recomendaciones. Es un listado con fechas y el médico decide. Ver §8.2.

### 4.4 App del familiar — donde vive toda la complejidad

- Alta y gestión de las pautas (medicamento, dosis, horas, días).
- Panel de cumplimiento: histórico de confirmaciones.
- Recepción de escalados.
- **Vigilancia del estado del sistema (latido).** Aviso explícito al familiar cuando el dispositivo del mayor deja de reportar, pierde el permiso de alarma exacta o se queda sin batería. Ver §6.2: el fallo silencioso es el modo de fallo peligroso.
- Identificación y registro de las tomas no previstas; generación del informe para el médico.
- Lista de comprobación guiada del alta (§5.2).
- Aquí, y solo aquí, se añaden funciones en el futuro.

### 4.5 Varios familiares — tres reglas desde el día uno

1. **Un propietario.** Una sola persona decide las pautas. Si todos pueden editar dosis, habrá un disgusto.
2. **Escalado en cascada, no en paralelo.** Al primero; si no responde en 30 min, al siguiente. Evita el efecto *"pensaba que lo miraba mi hermana"*.
3. **Registro de quién cambió qué y cuándo.** Barato de implementar, y cubre el día que dos hermanos discutan sobre si la dosis se cambió.

### 4.6 Arquitectura de apps

**[Probable] Dos apps en Play con módulo común**, no una app con selector de rol: `:core` compartido, `:app-mayor`, `:app-familiar`.

Razón: la app del mayor debe ser **incapaz** de mostrar otra cosa. Que el código no exista es una garantía más fuerte que un condicional. Coste aceptado: dos fichas y dos revisiones de Play.

### 4.7 Fuera de alcance en v1 (explícitamente)

- Comprobación de interacciones medicamentosas. **Riesgo regulatorio, §8.2.**
- Cálculo o ajuste de dosis. **Mismo riesgo.**
- Citas médicas, hidratación, agenda, recados, videollamada. *(Aplazadas; entrarían por la app del familiar.)*
- **Detección de inactividad, ubicación, conteo de pasos y cualquier otra recogida pasiva de datos del mayor. No aplazado: prohibido.** Ver §8.3 — convierte el producto en vigilancia de un adulto, sin exención posible en Play.
- Integración con receta electrónica.
- iOS.
- El centro de día o la residencia **como usuario** del producto. (Siguen siendo canal de venta, §7.)

---

## 5. El alta acompañada

Pieza estructural, no detalle de onboarding. Nació de la pregunta "¿se puede instalar la app del mayor en remoto?".

### 5.1 La instalación remota no existe, y su versión viable es ilegal

**[Seguro]** Android no permite que una app instale otra app en un dispositivo ajeno. No hay API. Vías reales de instalación silenciosa:

| Vía | Por qué no sirve |
|---|---|
| Play "instalar en otro dispositivo" | Solo dispositivos de **tu propia** cuenta de Google. |
| Device Owner / Android Enterprise (MDM) | Exige provisionar el móvil desde fábrica o reset. Absurdo para una familia, y **[Suposición]** los términos de Enterprise probablemente lo prohíben en uso de consumo. |
| Family Link | Solo cuentas de menores. |
| Enviar el APK por Nearby Share | Obliga al mayor a aceptar "orígenes desconocidos" y te saca de las actualizaciones de Play. |

**[Probable]** Y lo más grave: una app de monitorización instalada en el móvil de un adulto sin que él participe entra de lleno en la política de Play sobre **stalkerware**, que exige consentimiento y notificación visible y persistente. *Pendiente de verificar contra la política actual.*

### 5.2 Lo que sí se hace: dos minutos presenciales

El familiar prepara **todo** en su app antes de la visita (perfil, medicamentos, horarios, orden de escalado). Al terminar, su app muestra un **código QR**.

Delante del mayor:

1. El familiar instala desde Play en el móvil del mayor, él mismo, con el teléfono en la mano.
2. Se abre y **escanea el QR** de la pantalla del familiar. El mayor no escribe nada.
3. La app del familiar le guía por una **lista de comprobación** sobre el móvil del mayor: permiso de alarma exacta, exención de optimización de batería, autoarranque según fabricante, volumen, desactivar "no molestar".
4. **Alarma de prueba ahí mismo.** Suena, el mayor pulsa el botón una vez con su hijo mirando.

### 5.3 Por qué esto es estructural y no un parche

1. **Resuelve el consentimiento.** El titular de los datos de salud es el mayor. Presente, informado y aceptando → consentimiento explícito válido (§8.1) y producto ético.
2. **Es el único momento en que se puede arreglar la fiabilidad de las alarmas.** Los ajustes de fabricante (§6) no los va a tocar un mayor de 83 años nunca. Su hijo, una vez, sí. El riesgo letal del producto solo tiene solución humana, presencial y única.
3. **Es la única formación que vas a tener.** Si el mayor no entiende por qué existe el botón, no lo pulsa.
4. El paso 4 es el control de calidad: **nadie se va de la casa sin haber visto sonar la alarma.**

### 5.4 Consecuencia estratégica

El alta acompañada **refuerza el canal** del §7 en lugar de competir con él: una farmacia o un centro de día puede hacer exactamente este alta de dos minutos. Un competidor financiado en California no.

Y pone un techo al crecimiento puramente orgánico: **[Probable]** este producto no se instala solo desde un anuncio. Eso es malo para escalar rápido y bueno para la retención y el precio.

---

## 6. El riesgo que puede matar el proyecto: fiabilidad de alarmas en Android

**[Seguro]** Un recordatorio de medicación que falla el 5 % de las veces es **peor que no tener app**, porque genera confianza falsa. Y fallar es el estado por defecto:

- **Doze mode / App Standby** retrasan alarmas inexactas de forma indefinida.
- **Los fabricantes** (Xiaomi/MIUI, Huawei/EMUI, Oppo, Vivo, Samsung) matan procesos en background de forma agresiva y mal documentada. Referencia: `dontkillmyapp.com`.
- **Android 12+** exige el acceso especial "Alarmas y recordatorios". Dos permisos posibles, ya verificados en §6.2.
- Hay que **reprogramar todas las alarmas** en `BOOT_COMPLETED` y tras cada actualización.

### 6.1 Spike técnico — hacer esto antes de cualquier pantalla

Objetivo: demostrar 100 % de disparos en 72 h sobre hardware real y hostil.

**Alcance (2 días):**

1. Proyecto Kotlin + Compose vacío.
2. `AlarmManager.setAlarmClock()` por toma. *No* `setExactAndAllowWhileIdle`, *no* WorkManager para el disparo.
3. `BroadcastReceiver` con `RECEIVE_BOOT_COMPLETED` que reprograma todo al arrancar.
4. Canal de notificación con importancia `HIGH`, sonido propio y `fullScreenIntent`.
5. **Log persistente** de cada disparo: hora programada vs. hora real.
6. Flujo de petición de exenciones: alarma exacta e ignorar optimización de batería.

**Protocolo:** alarmas cada hora durante 72 h, en al menos un Xiaomi y un Samsung reales, móvil quieto, con y sin exención de batería.

**Criterio de éxito:** desviación máxima < 60 s y **cero disparos perdidos** con la exención concedida.

### 6.2 Verificado: los permisos de alarma exacta no son un obstáculo

Comprobado el 2026-11-15 contra la documentación de Android y el anuncio de políticas de Play del 27 de julio de 2022.

| | `SCHEDULE_EXACT_ALARM` | `USE_EXACT_ALARM` (API 33+) |
|---|---|---|
| Concesión | La da el usuario en Ajustes | Automática al instalar |
| Revocable por el usuario | Sí | No |
| Filtro de política de Play | **Ninguno** | Sí, permiso restringido |
| Casos de uso | *"Broader set of use cases"* | Limitados |

**[Seguro]** La política de Play sobre el permiso restringido es un **test funcional, no una lista blanca de categorías**:

> *"apps must only declare this permission if their core functionality requires an exact alarm. Apps declaring the new restricted permission that do not meet these criteria will not be permitted on Google Play."*

Un recordatorio de medicación lo cumple de forma evidente. La idea de que solo cualifican despertadores y calendarios venía de guías de terceros, no de Google.

**Decisión:** v1 con `SCHEDULE_EXACT_ALARM`, que no pasa por ninguna puerta de política y se concede durante el alta acompañada (§5.2). Evaluar `USE_EXACT_ALARM` más adelante por la ventaja de ser irrevocable.

**Método confirmado:** `setAlarmClock()`. De la documentación: *"the system never adjusts their delivery time. The system identifies these alarms as the most critical ones and leaves low-power modes if necessary to deliver the alarms."*

### 6.3 El fallo silencioso: el riesgo real

**[Seguro]** De la documentación de Android:

> *"When the SCHEDULE_EXACT_ALARM permission is revoked for your app, your app stops, and all future exact alarms are canceled."*

Y lo pueden revocar **tanto el usuario como el sistema**. Además, `SCHEDULE_EXACT_ALARM` no se preconcede en instalaciones nuevas en API 33+, y se deniega al restaurar datos desde una copia de seguridad en un dispositivo nuevo.

Traducción: el dispositivo del mayor puede dejar de avisar **sin que nadie lo note**, hasta que haya un problema de salud. Es el modo de fallo que convierte este producto en peligroso.

**Requisito no negociable — latido:**

1. El dispositivo del mayor reporta a diario que sigue instalado, con permiso concedido y con alarmas programadas.
2. Si deja de reportar, **el familiar recibe un aviso de que el sistema está caído**.
3. Receptor de `ACTION_SCHEDULE_EXACT_ALARM_PERMISSION_STATE_CHANGED` que reprograma y notifica al familiar si se pierde el permiso.
4. Comprobar `canScheduleExactAlarms()` antes de cada programación.

> El fallo tiene que ser ruidoso en el lado de quien puede arreglarlo. Sin latido no tienes un producto fiable: tienes uno que lo parece.

---

## 7. Canal de distribución

Decisión: el producto es **solo familiar** (mayor + hijos), pero el canal de venta **no** es solo Google Play. Son cosas independientes y conviene no confundirlas: la farmacia no necesita ser usuaria de la app para recomendarla.

Prioridad descendente:

1. **Farmacias de barrio.** Recomiendan y tienen la confianza del mayor. Pueden hacer el alta del §5.2.
2. **Centros de día y residencias pequeñas.** Acceso a familias con el dolor agudo; posible pagador institucional más adelante.
3. **Asociaciones de familiares** (Alzheimer, párkinson). Acceso directo al cuidador.
4. **Servicios sociales municipales.** Ciclo largo, contrato grande, difícil sin referencias.
5. Google Play orgánico. **Último**, no primero.

**[Suposición]** El coste de adquisición vía farmacia será un orden de magnitud inferior al de Play. Medir con los primeros 20 usuarios.

---

## 8. Legal y regulatorio

### 8.1 RGPD

**[Probable]** Los datos de medicación son **categoría especial, art. 9 RGPD**:

- Consentimiento explícito, no implícito. El alta acompañada (§5) es el mecanismo que lo hace posible y demostrable.
- Cifrado en tránsito y en reposo.
- Definir **quién es el responsable del tratamiento** cuando el hijo introduce datos de salud del mayor, en especial si este tiene capacidad reducida. No es trivial; requiere asesoría.
- Guardar evidencia del consentimiento otorgado en el alta.

### 8.2 Producto sanitario (MDR)

**[Suposición — requiere consulta con especialista]** Un recordatorio puro, que no interpreta ni calcula, queda fuera del Reglamento (UE) 2017/745. Añadir comprobación de interacciones, cálculo de dosis o cualquier recomendación clínica lleva probablemente a la **Regla 11** y a clase IIa: organismo notificado, sistema de calidad, años.

**Decisión de diseño:** la frontera "solo registramos, nunca interpretamos" es una restricción deliberada que compra velocidad.

### 8.3 Política de Play sobre stalkerware — la restricción más dura del proyecto

Comprobado el 2026-11-15 contra el anuncio de políticas de Play de septiembre de 2020 (archivo de políticas; **la redacción viva puede diferir y conviene releerla antes de publicar**).

**El problema.** Literal:

> *"Apps exclusively designed and marketed for parents to track their children or enterprise management, provided they fully comply with the requirements described below are the only acceptable surveillance apps. These apps cannot be used to track anyone else (a spouse, for example) even with their knowledge and permission, regardless if persistent notification is displayed."*

Un hijo supervisando a su madre adulta **no entra en ninguna de las dos exenciones** (padres con hijos menores, o empresas con empleados). Y el consentimiento del mayor **no sirve** como defensa. Si el producto se clasifica como *surveillance app*, está prohibido.

**Lo que nos salva.** La misma política define una segunda categoría, permitida:

> *"Non-stalkerware apps distributed on the Play Store which monitor or track a user's behavior on a device must minimally comply with these requirements: Apps must not present themselves as a spying or secret surveillance solution. Apps must not hide or cloak tracking behavior or attempt to mislead users about such functionality. Apps must present users with a persistent notification at all times when the app is running and a unique icon that clearly identifies the app."*

**[Probable]** Este producto cae aquí, y no en *surveillance*, por una razón concreta: **el mayor pulsa el botón**. La app no le observa, recibe un parte que él emite voluntariamente. Es la diferencia entre un sensor y una lista de la compra compartida.

**Requisitos que esto impone:**

- Notificación persistente siempre que la app esté activa.
- Icono único e identificable.
- Nada de lenguaje de vigilancia en la copy ni en la ficha de Play. Nunca "controla", "vigila" o "supervisa a distancia".
- Declarar la función de aviso al familiar en la propia ficha de Play.
- La transparencia permanente en pantalla del §4.2.

**La consecuencia que cambia el roadmap:** cualquier recogida **pasiva** de datos del mayor (ubicación, inactividad, pasos, sensores) rompe el argumento activo/pasivo y te mete en *surveillance* de un adulto, sin exención posible. Por eso esas funciones pasan de "aplazadas" a **prohibidas** en §4.7.

**Pendiente:** la política advierte que *"You are solely responsible for determining the legality of your app in its targeted locale"*. Para España hay que sumar la capacidad jurídica del mayor y el RGPD. **Esto requiere abogado antes de publicar, no después.**

### 8.4 Lenguaje

Nunca usar "tratamiento", "diagnóstico", "terapia" ni verbos clínicos en la copy ni en la ficha de Play. Es "recordatorio" y "acompañamiento".

---

## 9. Validación previa al código

El spike técnico (§6.1) puede ir en paralelo. Antes de construir producto:

- [ ] **10 entrevistas con hijos cuidadores**, no con mayores. Preguntar por el último mes concreto, no por preferencias hipotéticas.
- [ ] **3 farmacias.** ¿Recomendarían esto? ¿Harían el alta de dos minutos? ¿Bajo qué condiciones?
- [ ] **2 centros de día.** ¿Quién decide? ¿Qué presupuesto?
- [ ] Preguntas que importan: ¿qué hacen hoy para resolverlo? ¿cuánto tiempo al día les cuesta? ¿han pagado ya por algo parecido?
- [ ] **Probar el guion del alta acompañada** con una familia real, aunque sea a mano y sin app.

**Señal de compra real:** que alguien pida ser el primero en probarlo sin que se lo ofrezcas.

---

## 10. Criterios de abandono

Definidos **ahora**, para no racionalizarlos después:

| Mátalo si... | Porque |
|---|---|
| ~~Play deniega el permiso de alarma exacta a esta categoría~~ | **Descartado el 2026-11-15.** Ver §6.2: `SCHEDULE_EXACT_ALARM` no pasa por ninguna política. |
| El spike no logra cero alarmas perdidas en 72 h en MIUI | El producto no puede cumplir su única promesa. |
| No se consigue un latido fiable que delate el fallo silencioso | Un producto que falla en silencio es peor que ninguno (§6.3). |
| Un abogado concluye que la supervisión familiar de un adulto no encaja en la categoría *non-stalkerware* de Play | No habría forma de publicarlo, con o sin consentimiento (§8.3). |
| De 10 familiares entrevistados, menos de 4 describen el problema sin que lo sugieras | No hay dolor, hay cortesía. |
| Ninguna farmacia acepta recomendarlo ni hacer el alta | Sin canal, quedas solo en Play contra incumbentes de diez años. |
| A los 60 días del piloto, la confirmación diaria baja del 60 % | El mayor no sostiene el hábito; el bucle no funciona. |
| El alta acompañada necesita más de 15 minutos en casa | No es replicable por una farmacia ni por un hijo con prisa. |
| Apareces necesitando marcado CE para el caso de uso central | Replantear, no empujar. |

---

## 11. Decisiones tomadas

| # | Decisión | Fecha | Estado |
|---|---|---|---|
| 1 | Usuario y pagador objetivo: los hijos, no el mayor | 2026-11-15 | Propuesta, sin validar |
| 2 | v1 = un único caso de uso: confirmación con escalado | 2026-11-15 | Propuesta |
| 3 | Sin interpretación clínica, para evitar MDR | 2026-11-15 | Propuesta |
| 4 | Android nativo (Kotlin + Compose), iOS fuera de v1 | 2026-11-15 | Propuesta |
| 5 | Canal prioritario: farmacias y centros, no Play | 2026-11-15 | Propuesta, sin validar |
| 6 | Producto solo familiar; la institución es canal, no usuario | 2026-11-15 | Propuesta |
| 7 | Automedicación = botón + foto; el registro lo hace el familiar | 2026-11-15 | Propuesta |
| 8 | Varios familiares con propietario, cascada y auditoría | 2026-11-15 | Propuesta |
| 9 | Dos apps en Play con módulo `:core` común | 2026-11-15 | Propuesta |
| 10 | Alta acompañada presencial con QR, checklist y alarma de prueba | 2026-11-15 | Propuesta, sin validar |
| 11 | Cero mantenimiento en el dispositivo del mayor tras el alta | 2026-11-15 | Propuesta |
| 12 | v1 con `SCHEDULE_EXACT_ALARM`; `USE_EXACT_ALARM` a evaluar después | 2026-11-15 | **Verificada contra la política de Play** |
| 13 | Latido obligatorio: el fallo del sistema se notifica al familiar | 2026-11-15 | Propuesta, derivada de §6.3 |
| 14 | Prohibida toda recogida pasiva de datos del mayor | 2026-11-15 | **Impuesta por la política de Play** (§8.3) |

---

## 12. Preguntas abiertas

1. **¿Y si el canal correcto no es una app en el móvil del mayor?** **[Suposición]** Para el segmento 80+ podría ganar una llamada automática, un SMS o un WhatsApp. En ese caso la app existiría solo para el familiar. Validar en las entrevistas: cambia la arquitectura entera.
2. ¿Modelo de negocio: suscripción del familiar, licencia por plaza, o marca blanca para teleasistencia?
3. ¿Hace falta hardware? Un tablet fijo en la cocina resuelve "el móvil no está encima" mejor que cualquier software — y el alta acompañada lo hace viable, porque alguien puede configurarlo.
4. ¿Qué pasa cuando dos hijos **no se hablan entre ellos**? Caso real y frecuente. El producto va a vivir dentro de conflictos familiares, no solo de olvidos.
5. ¿Qué cuenta como confirmación fiable? El botón puede pulsarse sin tomar la pastilla. **[Probable]** importa poco en familia, mucho en residencia.
6. ¿Quién hace el alta cuando no hay un hijo cerca geográficamente? Es el caso más común en la España vaciada, y es justo donde el dolor es mayor.

---

## 13. Siguiente acción

1. ~~Verificar la política de Play sobre alarmas exactas y apps de monitorización.~~ **Hecho el 2026-11-15.** Resultado: las alarmas exactas no son obstáculo (§6.2); la política de stalkerware sí impone límites permanentes al alcance (§8.3).
2. **Spike de fiabilidad de alarmas (§6.1), ampliado con el latido (§6.3).** Dos días, en paralelo a las entrevistas.
3. **Consulta legal** sobre el encaje de la supervisión familiar de un adulto en la categoría *non-stalkerware*, y sobre responsable del tratamiento en el RGPD. Antes de publicar, no antes de programar.

No empezar por las pantallas.

---

## Fuentes verificadas

- [Schedule alarms — Android Developers](https://developer.android.com/develop/background-work/services/alarms/schedule)
- [Policy announcement: July 27, 2022 — Exact Alarm API restricted permission](https://support.google.com/googleplay/android-developer/answer/14554661)
- [Policy announcement: September 16, 2020 — Stalkerware, effective October 1, 2020](https://support.google.com/googleplay/android-developer/answer/10065487)

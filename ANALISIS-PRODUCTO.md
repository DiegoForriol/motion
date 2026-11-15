# App de acompañamiento para personas mayores — Análisis de producto

> Documento vivo. Fecha de la primera versión: 2026-11-15.
> Las afirmaciones van etiquetadas: **[Seguro]** (evidencia sólida), **[Probable]** (inferencia fuerte), **[Suposición]** (hueco rellenado, hay que validar).

---

## 1. Resumen ejecutivo

La idea original —"una app Android que simplifica el día a día del mayor con recordatorios de medicación y muchas más cosas"— **no es viable tal cual**. Dentro de ella hay un negocio real, más estrecho y más defendible:

> Un servicio que garantiza al cuidador que su familiar se ha tomado la medicación, mediante un bucle de confirmación con escalado automático.

Tres correcciones respecto al planteamiento inicial:

| Planteamiento inicial | Corrección |
|---|---|
| El usuario es la persona mayor | El **usuario activo y el pagador es el cuidador** (hijo/hija, 45–65 años). El mayor es el beneficiario. |
| El producto es el recordatorio | El producto es la **confirmación y el escalado**. El recordatorio es comodity y está resuelto gratis. |
| Simplificar + muchas funciones | Una sola función en el dispositivo del mayor. La complejidad vive en la app del cuidador. |

---

## 2. Por qué el planteamiento original falla

### 2.1 La tenaza demográfica

**[Probable]** El público se parte en dos y ninguna mitad encaja con una app instalada en el móvil del mayor:

- **65–75 años, autónomos.** Usan smartphone, pero no tienen el problema. Se acuerdan solos o usan un pastillero semanal de 1 €.
- **80+ o con deterioro cognitivo.** Tienen el problema, pero no van a abrir la app, no oirán la notificación y no tendrán el móvil encima.

El dolor agudo no está en el mayor: está en quien le llama tres veces al día para preguntar *"¿te has tomado la pastilla?"*.

### 2.2 "Simplificar" y "muchas más cosas" se excluyen

**[Seguro]** Cada función añadida es una decisión más en una pantalla que debería tener dos botones. La causa de muerte más habitual de las apps para mayores es el crecimiento de alcance.

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

**[Probable]** Las apps dominantes son estadounidenses, con publicidad, monetizadas vía farmacéuticas, localización pobre al español y centradas en el paciente como usuario. Ninguna va a:

- hablar con la farmacia del barrio,
- licitar con un ayuntamiento de 40.000 habitantes,
- hacer alta asistida en un centro de día.

**El foso no es tecnológico: es de canal y de distribución local.**

### 3.4 Alcance técnico pequeño

**[Seguro]** El núcleo son semanas de trabajo en solitario, no un año: Kotlin + Compose, Room, `AlarmManager`, Firebase (Auth + Firestore + FCM). Sin IA, sin backend propio, sin infraestructura.

### 3.5 No se necesita escala

**[Suposición]** 15 centros de día o residencias pequeñas a 150–250 €/mes sostienen a una persona. Una app de consumo necesitaría decenas de miles de usuarios para lo mismo.

---

## 4. Producto mínimo

### 4.1 El bucle de confirmación (único caso de uso de la v1)

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
Registro OK            Aviso push al cuidador
                                  ↓
                       Sin respuesta en 40 min
                                  ↓
                       Segundo aviso / llamada
```

### 4.2 App del mayor — reglas de diseño no negociables

- **Una acción por pantalla.** Nada de gestos, menús, scroll ni pestañas.
- Tipografía mínima 24 sp en cuerpo, 36 sp+ en la acción principal.
- Contraste AAA. Sin texto gris sobre blanco.
- Alarma a pantalla completa con sonido forzado, no una notificación en la bandeja.
- Nunca pedir contraseña, email ni nada que haya que recordar. El alta la hace el cuidador.
- Si la app se abre sola, debe mostrar lo único relevante: la toma pendiente o "todo hecho hoy".

### 4.3 App del cuidador — donde vive toda la complejidad

- Alta y gestión de las pautas (medicamento, dosis, horas, días).
- Panel de cumplimiento: histórico de confirmaciones.
- Recepción de escalados.
- Aquí, y solo aquí, se añaden funciones en el futuro.

### 4.4 Fuera de alcance en v1 (explícitamente)

- Comprobación de interacciones medicamentosas. **Riesgo regulatorio, ver §7.**
- Cálculo o ajuste de dosis. **Mismo riesgo.**
- Citas médicas, hidratación, agenda, recados, detección de inactividad, videollamada.
- Integración con receta electrónica.
- iOS.

> El instinto de que hay mucho más que la medicación es correcto. Lo que estaba mal era el orden: esas funciones entran por la app del cuidador una vez el canal de confianza existe.

---

## 5. El riesgo que puede matar el proyecto: fiabilidad de alarmas en Android

**[Seguro]** Un recordatorio de medicación que falla el 5 % de las veces es **peor que no tener app**, porque genera confianza falsa. Y fallar es el estado por defecto en Android:

- **Doze mode / App Standby** retrasan alarmas inexactas de forma indefinida.
- **Los fabricantes** (Xiaomi/MIUI, Huawei/EMUI, Oppo, Vivo, Samsung) matan procesos en background de forma agresiva y mal documentada. Referencia: `dontkillmyapp.com`.
- **Android 12+** requiere `SCHEDULE_EXACT_ALARM`; `USE_EXACT_ALARM` está restringido por política de Google Play a apps de tipo despertador/calendario. **[Probable]** una app de medicación cualifica, pero hay que justificarlo en la ficha de Play. *Pendiente de verificar contra la política actual.*
- Hay que **reprogramar todas las alarmas** en `BOOT_COMPLETED` y tras cada actualización de la app.

### 5.1 Spike técnico — hacer esto antes de cualquier pantalla

Objetivo: demostrar 100 % de disparos en 72 h sobre hardware real y hostil.

**Alcance (2 días):**

1. Proyecto Kotlin + Compose vacío.
2. `AlarmManager.setAlarmClock()` para cada toma. *No* `setExactAndAllowWhileIdle`, *no* WorkManager para el disparo.
3. `BroadcastReceiver` con `RECEIVE_BOOT_COMPLETED` que reprograma todo al arrancar.
4. Canal de notificación con importancia `HIGH`, sonido propio y `fullScreenIntent`.
5. **Log persistente** de cada disparo: hora programada vs. hora real de ejecución, escrito a fichero o Room.
6. Flujo de petición de exenciones: `SCHEDULE_EXACT_ALARM` e ignorar optimización de batería.

**Protocolo de prueba:** alarmas cada hora durante 72 h, en al menos un Xiaomi y un Samsung reales, móvil quieto y sin tocar, con y sin exención de batería. Revisar el log al final.

**Criterio de éxito:** desviación máxima < 60 s y **cero disparos perdidos** con la exención concedida.

---

## 6. Canal de distribución (la parte defendible)

Prioridad descendente:

1. **Centros de día y residencias pequeñas.** Pagador institucional, ciclo de venta corto, alta asistida.
2. **Farmacias de barrio.** Recomiendan, y tienen la confianza del mayor. Posible comisión o marca blanca.
3. **Asociaciones de familiares** (Alzheimer, párkinson). Acceso directo al cuidador con el dolor agudo.
4. **Servicios sociales municipales.** Ciclo largo, contrato grande, difícil sin referencias previas.
5. Google Play orgánico. **Último**, no primero.

**[Suposición]** El coste de adquisición vía farmacia o centro será un orden de magnitud inferior al de Play. Hay que medirlo con los primeros 20 usuarios.

---

## 7. Legal y regulatorio

### 7.1 RGPD

**[Probable]** Los datos de medicación son **categoría especial, art. 9 RGPD**. Implicaciones:

- Consentimiento explícito, no implícito.
- Cifrado en tránsito y en reposo.
- Definir con claridad **quién es el responsable del tratamiento** cuando el cuidador introduce datos de salud de un tercero (el mayor), especialmente si este tiene capacidad reducida. Esto no es trivial y conviene asesoría.
- Si el cliente es una residencia, aparece un **encargado del tratamiento** y hace falta contrato (art. 28).

### 7.2 Producto sanitario (MDR)

**[Suposición — requiere consulta con especialista]** Un recordatorio puro, que no interpreta ni calcula, queda fuera del Reglamento (UE) 2017/745. En cuanto se añada comprobación de interacciones, cálculo de dosis o cualquier recomendación clínica, se entra probablemente en la **Regla 11** y en clase IIa: certificación, organismo notificado, sistema de calidad. Eso es un muro, no una tarea.

**Decisión de diseño:** la frontera "solo recordamos, nunca interpretamos" es una restricción de producto deliberada que compra velocidad.

### 7.3 Lenguaje

Nunca usar "tratamiento", "diagnóstico", "terapia" ni verbos clínicos en la copy ni en la ficha de Play. Es "recordatorio" y "acompañamiento".

---

## 8. Validación previa al código

Antes de escribir producto (el spike técnico del §5 sí puede ir en paralelo):

- [ ] **10 entrevistas con cuidadores**, no con mayores. Preguntar por el último mes concreto, no por preferencias hipotéticas.
- [ ] **3 conversaciones con centros de día.** ¿Quién decide? ¿Qué presupuesto? ¿Qué usan hoy?
- [ ] **2 farmacias.** ¿Recomendarían algo así? ¿Bajo qué condiciones?
- [ ] Preguntas que importan: ¿qué hacen hoy para resolverlo? ¿cuánto tiempo al día les cuesta? ¿han pagado ya por algo parecido?

**Señal de compra real:** que alguien pida ser el primero en probarlo sin que se lo ofrezcas.

---

## 9. Criterios de abandono

Definidos **ahora**, para no racionalizarlos después:

| Mátalo si... | Porque |
|---|---|
| El spike técnico no logra cero alarmas perdidas en 72 h en MIUI | El producto no puede cumplir su única promesa. |
| De 10 cuidadores entrevistados, menos de 4 describen el problema sin que lo sugieras | No hay dolor, hay cortesía. |
| Ningún centro de día acepta una prueba piloto gratuita | Si no lo quieren gratis, no lo van a pagar. |
| A los 60 días del piloto, la tasa de confirmación diaria baja del 60 % | El mayor no sostiene el hábito; el bucle no funciona. |
| Apareces necesitando marcado CE para resolver el caso de uso | Cambia el proyecto por completo; hay que replantear, no empujar. |

---

## 10. Decisiones tomadas

| # | Decisión | Fecha | Estado |
|---|---|---|---|
| 1 | El usuario y pagador objetivo es el cuidador, no el mayor | 2026-11-15 | Propuesta, sin validar |
| 2 | v1 = un único caso de uso: confirmación con escalado | 2026-11-15 | Propuesta |
| 3 | Sin interpretación clínica, para evitar MDR | 2026-11-15 | Propuesta |
| 4 | Android nativo (Kotlin + Compose), iOS fuera de v1 | 2026-11-15 | Propuesta |
| 5 | Canal prioritario: centros y farmacias, no Play | 2026-11-15 | Propuesta, sin validar |

---

## 11. Preguntas abiertas

1. **¿Y si el canal correcto no es una app en el móvil del mayor?** **[Suposición]** Para el segmento 80+, podría ganar una llamada automática, un SMS o un mensaje de WhatsApp — algo que no exija aprender nada. En ese caso la app existiría solo para el cuidador. Esto hay que validarlo en las entrevistas, porque cambia la arquitectura entera.
2. ¿Modelo de negocio: suscripción del cuidador, licencia por plaza al centro, o marca blanca para teleasistencia?
3. ¿Se necesita hardware? Un tablet fijo en la cocina resuelve "el móvil no está encima" mejor que cualquier software.
4. ¿Qué pasa cuando hay dos cuidadores que no se hablan entre ellos? (Caso real y frecuente.)
5. ¿Qué cuenta como confirmación fiable? El botón puede pulsarse sin tomar la pastilla. ¿Importa? **[Probable]** sí importa para residencias, no tanto para familia.

---

## 12. Siguiente acción

**Spike de fiabilidad de alarmas (§5.1).** Dos días. Elimina el riesgo que invalida todo lo demás, y se puede hacer en paralelo a las entrevistas.

No empezar por las pantallas.

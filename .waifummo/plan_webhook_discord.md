## 1. Feedback Arquitectónico
Tu propuesta de utilizar un flujo **Pizzant (Python) ➜ NestJS (Webhook) ➜ Gemini + Discord** demuestra una clara madurez en el diseño de sistemas (la "Arquitectura Brian"). 

**Puntos fuertes de tu diseño:**
* **Desacoplamiento total:** El bot de caza ya no necesita saber cómo hablar con Discord ni saber qué es Gemini. Solo grita al mundo: *"¡Encontré un Shiny!"*.
* **Seguridad perimetral:** Al agregar el JWT (JSON Web Token), evitas que cualquiera pueda hacer peticiones POST maliciosas a tu servidor de NestJS simulando capturas falsas.
* **Escalabilidad y Performance:** El bot no espera la respuesta. Esto significa $0$ latencia añadida al bucle de cacería. Si Discord se cae, Pizzant sigue atrapando Shinies.

**Puntos a tener en cuenta (Edge cases):**
* Es importante configurar un manejo de errores (try/catch) en NestJS por si la API de Gemini falla temporalmente, haciendo que el webhook recurra a un mensaje estándar por defecto y no pierdas la notificación del Shiny.

---

## 2. Resumen Ejecutivo (Resumen)
Vamos a extraer la lógica de alerta de Discord que actualmente vive dentro de `src/bot_main.py` (la cual es síncrona y bloqueante) y la moveremos a un nuevo módulo dedicado (`src/notifications/webhook_notifier.py`). Este módulo enviará de forma **asíncrona** los datos del Pokémon Shiny y la captura de pantalla a la URL de tu servidor. 

A nivel interfaz de usuario (UI), conectaremos los campos correspondientes para que puedas ingresar el **Token JWT** y la **URL del Webhook** sin tocar el código fuente del bot. Por tu lado, configurarás el servidor NestJS para recibir estos datos, validarlos, generar el texto dinámico con IA y publicarlo en Discord.

---

## 3. Tabla de Tareas y Componentes

| Fase | Componente / Archivo | Tarea Específica | Responsabilidad |
| :--- | :--- | :--- | :--- |
| **1. Pizzant (Core)** | `src/notifications/webhook_notifier.py` | Crear clase modular que maneje las peticiones HTTP (POST) hacia el Webhook de forma asíncrona (`threading`). | **Bot (Nosotros)** |
| **2. Pizzant (Core)** | `src/bot_main.py` | Eliminar lógica vieja (`requests.post` bloqueante a Discord) e instanciar el nuevo `WebhookNotifier`. | **Bot (Nosotros)** |
| **3. Pizzant (Config)**| `config.json` / UI | Añadir variables `webhook_url`, `webhook_jwt` y `webhook_enabled` al sistema de guardado y lectura de parámetros. | **Bot (Nosotros)** |
| **4. NestJS (API)** | `webhook.controller.ts` | Crear endpoint `POST /api/webhooks/shiny`, aplicar el `JwtAuthGuard` y el interceptor para recibir la imagen (`multer`). | **Servidor (Tú)** |
| **5. NestJS (Servicio)**| `shiny.service.ts` | Integrar `@google/generative-ai` para crear el prompt. Extraer el texto y publicarlo junto a la imagen usando `discord.js`. | **Servidor (Tú)** |

---

## Plan de Ejecución en Código (Pizzant)

### [NEW] `src/notifications/webhook_notifier.py`
Crearemos este archivo con la clase `WebhookNotifier`, la cual tendrá el método `send_shiny_event_async` para despachar el evento en segundo plano.

### [MODIFY] `src/bot_main.py`
Reemplazaremos `send_discord_alert` por la llamada asíncrona, liberando inmediatamente el hilo de ejecución principal.

## Verificación
* **Manual:** Simularemos una detección de Shiny. Observaremos los logs (`[INFO] Enviando evento Shiny...`) para asegurar que el tiempo de respuesta del código Python (Pizzant) sea instantáneo y no haya tirones ni pausas artificiales, validando la asincronía.
* **Integración:** Te enviaremos un payload de prueba a tu URL local o a un *webhook tester* temporal para confirmar que la estructura del JSON y el `multipart/form-data` llegan impecables al servidor.

## User Review Required
> [!IMPORTANT]
> Revisa la tabla de responsabilidades. Si estás de acuerdo con la división de tareas y el plan, presiona "Proceed" o dame el "OK", y procederé con la escritura del código en Python para dejar la parte del bot lista para conectarse a tu NestJS.

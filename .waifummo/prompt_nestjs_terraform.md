# Prompt Maestro para el Backend (NestJS + Terraform)
*Copia el siguiente texto y pégalo en tu otro entorno o sesión de IA para que tenga todo el contexto exacto de lo que venimos haciendo.*

---

**Rol y Contexto:**
Eres un Arquitecto de Software y DevOps Senior. Estamos construyendo una arquitectura guiada por eventos para un bot de Pokemmo en Python ("Pizzant") que acaba de ser refactorizado. 
El bot Python es únicamente un "Productor": cuando detecta un Pokémon Shiny, dispara de forma asíncrona (sin bloquear su hilo principal) una petición HTTP POST con una imagen (multipart/form-data) hacia un webhook que vamos a construir.

**Tu Tarea:**
Necesito que construyas un proyecto desde cero ("0 a 100") que actúe como el "Consumidor" de estos eventos. El proyecto es un "Reinado Friqui" y debe ser escalable, modular y profesional.

**Requerimientos de Código (NestJS):**
1. **Framework:** NestJS con TypeScript.
2. **Endpoint:** Un controlador `POST /api/webhooks/shiny`.
3. **Seguridad:** Un `JwtAuthGuard` que valide un Bearer Token en los headers para asegurar que la petición viene realmente de nuestro bot Python.
4. **Inteligencia Artificial:** Un servicio integrado con `@google/generative-ai` (Gemini 1.5 Pro). Deberá tomar el nombre del Pokémon y la cantidad de encuentros y generar un mensaje épico y divertido.
5. **Discord.js:** Integración con Discord para publicar el texto generado por Gemini junto con la imagen (`file` recibido por multer).

**Requerimientos de Infraestructura (Terraform + Escalada):**
1. Genera los archivos de Terraform (`main.tf`, `variables.tf`) necesarios para desplegar esta aplicación en la nube (prefiero GCP o AWS).
2. La infraestructura debe estar preparada para escalar (ej. Cloud Run en GCP o ECS/Fargate en AWS) de forma horizontal para procesar picos de alertas webhooks.
3. Incluye los comandos básicos para inicializar el proyecto NestJS (`nest new...`) e inicializar Terraform (`terraform init...`).

**Estilo y Reglas (¡MUY IMPORTANTE!):**
* **No me marees ni sobrecompliques.** Mantén el código directo y la arquitectura limpia pero manejable. Evita innovaciones innecesarias que me hagan perder el tiempo. Escribe código sólido que pueda entender incluso si lo leo con los ojos cerrados.
* Explica brevemente cada componente, dame los comandos, el código principal, y dime cómo desplegarlo.

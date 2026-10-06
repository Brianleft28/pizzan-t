# Análisis: Ejecución en Segundo Plano (Target a PokeMMO.exe)

## Goal Description
El usuario consultó si es posible configurar el bot para que envíe los comandos y capture la pantalla apuntando directamente al ejecutable `Pokemmo.exe`, permitiendo que el bot corra en un escritorio virtual separado o minimizado mientras el usuario utiliza la PC para otras cosas.

## Análisis Técnico (Por qué es complicado)

Actualmente, el bot utiliza dos librerías fundamentales que actúan a nivel del sistema operativo general:
1. **`pydirectinput`**: Emula pulsaciones de teclado a nivel hardware (DirectInput). Esto es necesario porque los juegos como PokeMMO ignoran las pulsaciones de teclado de software convencionales. La desventaja es que **solo envía la tecla a la ventana que tenga el foco activo en la pantalla principal**.
2. **`mss` / Screen Capture**: Toma fotos del monitor. No puede sacar fotos de una ventana que está tapada por otra o que está en un escritorio virtual inactivo (devolvería negro o la imagen congelada).

### ¿Se puede hacer?
Técnicamente sí, usando la API de Windows (`win32gui`, `win32ui`, `PostMessage`), pero:
- **Juegos en Java/OpenGL (PokeMMO)**: Suelen bloquear o ignorar los inputs en segundo plano (`PostMessage`).
- **Captura en segundo plano**: `PrintWindow` en OpenGL consume muchísimos recursos y a veces falla en Windows 10/11 si la ventana está minimizada o en otro escritorio virtual.

## Alternativa Recomendada (Zero Riesgo)
Ya que comentaste que vas a usar "otra PC" o "los bats en la otra PC", la forma correcta y god de hacerlo es:
- **Máquina Virtual (VM)**: Levantar un VirtualBox o VMware ligero. Correr el juego y el bot adentro de la VM. De esta forma, la VM cree que tiene la pantalla activa y el teclado, pero vos podés minimizar la ventana de la VM y seguir usando tu PC host sin problemas.
- **Segunda PC dedicada**: Literalmente dejar la otra PC corriendo el bot, que es lo que planeabas.

## Conclusión del Plan
No es viable modificar el código actual para que apunte al proceso en segundo plano sin reescribir todo el motor de captura y teclado (con altas chances de que el juego lo bloquee y detecte como bot inyectado). Recomiendo **mantener la arquitectura actual** y aislar el bot en la otra PC o en una VM.


# Respuestas — Actividad 3: Integración de DevOps y DevSecOps

## Parte teórica

### 1. ¿Qué es DevOps y qué no es?

DevOps es juntar desarrollo y operaciones para trabajar mejor y más rápido. No es solo usar herramientas nuevas, es colaborar y automatizar lo que se pueda. No es un puesto, es una forma de trabajar. Un ejemplo de gate de calidad sería que el Makefile no deje pasar si falla una prueba.

---

### 2. Marco CALMS en acción

- **Culture (Cultura):** En el laboratorio, todos los scripts y configuraciones están documentados y compartidos, lo que facilita que cualquier persona del equipo pueda entender y modificar el flujo. Se nota que la comunicación es importante para evitar silos.
- **Automation (Automatización):** El uso de Makefile y scripts Bash hace que todo el proceso de despliegue y pruebas sea automático y repetible. Así se ahorra tiempo y se evitan errores manuales.
- **Lean:** El laboratorio permite hacer cambios pequeños y frecuentes, y repetir el flujo fácilmente. Si algo falla, se detecta rápido y se puede corregir sin perder mucho tiempo.
- **Measurement (Medición):** Hay logs estructurados y endpoints de salud que permiten medir cómo está la app. Por ejemplo, con curl se puede ver el tiempo de respuesta y los códigos de estado.
- **Sharing (Compartir):** Se podría mejorar agregando runbooks y postmortems en el repositorio, para que todos sepan cómo actuar ante incidentes y aprendan de los errores.

Propongo que el equipo tenga un runbook sencillo y que después de cada incidente se haga un postmortem breve para compartir lo aprendido.

---

### 3. Visión cultural de DevOps y paso a DevSecOps

La cultura DevOps busca que todos colaboren y no haya barreras entre desarrollo, operaciones y ahora seguridad (DevSecOps). En vez de culpar a alguien cuando algo falla, se analiza el problema en conjunto y se documenta para que no vuelva a pasar.

En DevSecOps, la seguridad se integra desde el principio. Por ejemplo, en el laboratorio se usan cabeceras TLS seguras en Nginx y se podría agregar un escaneo de dependencias en el pipeline de CI/CD.

Si, por ejemplo, falla un certificado TLS, lo ideal es que el equipo lo detecte rápido, lo comunique y haga un postmortem para entender la causa y cómo evitarlo en el futuro.

Tres controles de seguridad que se pueden aplicar sin contenedores y que encajan en CI/CD:

1. Validar que Nginx tenga cabeceras HTTP seguras como HSTS y X-Frame-Options (en el archivo de configuración de Nginx).
2. Escanear dependencias con herramientas como `safety` o `npm audit` en la etapa de integración continua.
3. Revisar logs y configurar alertas automáticas usando journalctl o scripts Bash.

---

### 4. Metodología 12-Factor App

De los 12 factores, estos cuatro me parecen los más claros en el laboratorio:

- **III. Configuración por entorno:** La app usa variables de entorno como `PORT`, `MESSAGE` y `RELEASE`, así que no hay que tocar el código para cambiar el comportamiento.
- **IV. Backing services:** Si la app necesitara conectarse a una base de datos o API, lo haría usando una URL en una variable de entorno, lo que facilita cambiar de servicio sin modificar el código.
- **V. Build, release, run:** El flujo está bien separado: primero se construye el artefacto, luego se configura y finalmente se ejecuta. El Makefile ayuda a mantener este orden.
- **XI. Logs como flujos:** Los logs van a stdout, así cualquier sistema puede recolectarlos y analizarlos. Es mucho más flexible que escribir a un archivo fijo.

**Reto:** Si la app guarda datos en memoria, se pierden al reiniciar. Lo ideal sería usar algo externo como Redis.

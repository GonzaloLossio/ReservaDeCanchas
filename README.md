# API de Reservas de Canchas Deportivas

Este es el backend para un sistema de reservas de canchas deportivas (fútbol, tenis, basket, etc). Está construido con FastAPI y PostgreSQL. 

El objetivo principal de este proyecto no era solo hacer un CRUD de usuarios y canchas, sino enfrentarme a la lógica de negocio y problemas de concurrencia reales que ocurren cuando se manejan horarios y reservas.

## Stack Tecnológico

* FastAPI
* PostgreSQL
* SQLModel (ORM y validación)
* JWT y Bcrypt (Autenticación y seguridad)
* Uvicorn

## Funcionalidades principales

* **Autenticación y Roles:** Sistema de login basado en JSON Web Tokens (JWT). Existen roles de usuario (cliente y administrador) que limitan qué endpoints se pueden consumir.
* **Gestión de sedes y canchas:** Los administradores pueden dar de alta canchas, definir qué deporte se juega en ellas y establecer su precio base por hora.
* **Lógica de reservas (Core del proyecto):** * El sistema rechaza automáticamente cualquier reserva cuyo rango de horas se solape con una reserva ya existente para esa misma cancha y fecha.
  * Cálculos de precios dinámicos dependiendo del día (fines de semana) y el horario.
* **Control de concurrencia:** Implementé bloqueos transaccionales a nivel de base de datos (`pg_advisory_xact_lock` en PostgreSQL) para evitar condiciones de carrera (Race Conditions). Si dos usuarios intentan tomar el mismo turno al mismo exacto milisegundo, la base de datos evita que se duplique la reserva.
* **Reglas de cancelación:** Bloqueo de cancelaciones si el usuario intenta cancelar con menos de 2 horas de anticipación.

## Ejecución local

Para levantar este proyecto en tu máquina:

1. Clona el repositorio.
2. Crea un entorno virtual:
   `python -m venv venv`
3. Activa el entorno virtual.
4. Instala las dependencias:
   `pip install -r requirements.txt`
5. Crea un archivo `.env` en la raíz con tus variables de entorno (puedes guiarte de la estructura que usa el archivo `database.py` y `config.py` para la URL de la base de datos y la llave secreta).
6. Corre el servidor:
   `uvicorn app.main:app --reload`

La documentación interactiva de Swagger estará disponible en `http://127.0.0.1:8000/docs`.

## Deuda técnica y áreas de mejora

El proyecto es funcional, pero soy consciente de que hay aspectos de la arquitectura y el código que debo mejorar para llevarlo a un estándar de producción real:

1. **Migraciones:** Actualmente la base de datos se inicializa usando `SQLModel.metadata.create_all` en el arranque de la aplicación. El siguiente paso lógico es integrar Alembic para tener un control de versiones real sobre la base de datos.
2. **Actualización de Pydantic:** Todavía hay partes del código utilizando métodos legacy como `.dict()` que deben actualizarse a `.model_dump()` para estar 100% alineados con Pydantic v2.
3. **Manejo de fechas:** Estoy usando `datetime.utcnow()`, lo cual genera fechas sin zona horaria (naive datetimes). Esto puede causar problemas de desfase si el servidor y la base de datos se despliegan en distintas zonas geográficas, por lo que debo refactorizarlo a fechas con información de zona horaria (timezone-aware).

# Liga_de_eSports_PYTHON
# Gestión de Jugadores y Equipos en una Liga de eSports

Este proyecto es una aplicación de Python que utiliza la librería `psycopg3` para gestionar jugadores y equipos en una liga de eSports mediante una base de datos PostgreSQL.

## Requisitos

-   Windows 10 o superior
-   Python 3.6 o superior instalado (asegúrate de que Python esté añadido al PATH)
-   PostgreSQL instalado y en ejecución
-   Librería `psycopg3` instalada

## Instalación

1.  **Clona el repositorio:**

    -   Abre `PowerShell`.
    -   Navega al directorio donde deseas clonar el repositorio.
    -   Ejecuta el siguiente comando:

        ```powershell
        git clone <URL_del_repositorio>
        cd <nombre_del_repositorio>
        ```

2.  **Crea un entorno virtual (recomendado):**

    -   Abre `PowerShell`.
    -   Navega al directorio del proyecto.
    -   Ejecuta el siguiente comando:

        ```powershell
        python -m venv venv
        ```

3.  **Activa el entorno virtual:**

    -   Ejecuta el siguiente comando:

        ```powershell
        venv\Scripts\Activate
        ```

    -   Verás que `(venv)` aparece al principio de la línea de comandos, indicando que el entorno virtual está activo.

4.  **Instala las dependencias:**

    -   Con el entorno virtual activo, ejecuta el siguiente comando:

        ```powershell
        pip install psycopg[binary]
        ```

5.  **Configura la base de datos:**

    -   Asegúrate de que PostgreSQL esté en ejecución.
    -   Modifica las credenciales de la base de datos en el script `esports.py` con los valores correctos para tu instalación:

        ```python
        DB_PARAMS = {
            'dbname': 'esports_db',
            'user': 'postgres',
            'password': 'tu contraseña', #Reemplazar por tu contraseña
            'host': 'localhost',
            'port': '5432'
        }
        ```

## Uso

1.  **Ejecuta el script:**

    -   Abre `PowerShell` en el directorio del proyecto.
    -   Asegúrate de que el entorno virtual esté activo.
    -   Ejecuta el siguiente comando:

        ```powershell
        python esports.py
        ```

2.  **Interactúa con la aplicación a través de la interfaz de línea de comandos:**

    -   El menú te permitirá realizar las siguientes operaciones:
        -   **Insertar equipo:** Ingresa el nombre, país y entrenador del nuevo equipo.
        -   **Insertar jugador:** Ingresa el nickname, rol y ID del equipo al que pertenece el jugador.
        -   **Leer equipos:** Muestra la lista de equipos y sus jugadores asociados.
        -   **Actualizar equipo:** Ingresa el ID del equipo y el nuevo nombre.
        -   **Actualizar jugador:** Ingresa el ID del jugador y el nuevo nickname.
        -   **Eliminar jugador:** Ingresa el ID del jugador a eliminar.
        -   **Eliminar equipo:** Ingresa el ID del equipo a eliminar (esto también elimina los jugadores asociados).
        -   **Salir:** Cierra la aplicación.

## Estructura de la Base de Datos

La base de datos consta de dos tablas:

-   `equipos`: Almacena información sobre los equipos.
    -   `id` (SERIAL PRIMARY KEY)
    -   `nombre` (TEXT NOT NULL UNIQUE)
    -   `pais` (TEXT)
    -   `entrenador` (TEXT)
-   `jugadores`: Almacena información sobre los jugadores.
    -   `id` (SERIAL PRIMARY KEY)
    -   `nickname` (TEXT NOT NULL UNIQUE)
    -   `rol` (TEXT NOT NULL)
    -   `equipo_id` (INTEGER REFERENCES equipos(id) ON DELETE CASCADE)

## Relación entre Tablas

-   La tabla `jugadores` tiene una clave foránea (`equipo_id`) que hace referencia a la tabla `equipos`, estableciendo una relación de uno a muchos (un equipo puede tener varios jugadores).
-   Se utiliza `ON DELETE CASCADE` para eliminar automáticamente los jugadores de un equipo cuando se elimina el equipo.

## Manejo de Errores

La aplicación maneja errores como nombres de equipos o nicknames duplicados y la inserción de jugadores en equipos inexistentes.

## Archivos

-   `esports.py`: El script principal de Python.
-   `explicacion.txt`: Descripción del funcionamiento del código y la relación entre las tablas.
-   `README.md`: Este archivo, con instrucciones de uso.

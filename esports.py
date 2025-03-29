import psycopg
from psycopg.rows import dict_row

# Configuración de la base de datos
DB_PARAMS = {
    'dbname': 'esports_db',
    'user': 'postgres',
    'password': 'serped11348',
    'host': 'localhost',
    'port': '5432'
}

def crear_tablas():
    # Crea las tablas 'equipos' y 'jugadores' si no existen.
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS equipos (
                    id SERIAL PRIMARY KEY,
                    nombre TEXT NOT NULL UNIQUE,
                    pais TEXT,
                    entrenador TEXT
                )
            """)# Crea la tabla 'jugadores' con clave foránea a 'equipos' y ON DELETE CASCADE
            cur.execute("""
                CREATE TABLE IF NOT EXISTS jugadores (
                    id SERIAL PRIMARY KEY,
                    nickname TEXT NOT NULL UNIQUE,
                    rol TEXT NOT NULL,
                    equipo_id INTEGER REFERENCES equipos(id) ON DELETE CASCADE
                )
            """)
        conn.commit()

def insertar_equipo(nombre, pais, entrenador):
    # Inserta un nuevo equipo en la tabla 'equipos'.
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("INSERT INTO equipos (nombre, pais, entrenador) VALUES (%s, %s, %s)", (nombre, pais, entrenador))
                conn.commit()
                print(f"Equipo '{nombre}' insertado correctamente.")
            except psycopg.errors.UniqueViolation:
                print(f"Error: El equipo '{nombre}' ya existe.")

def insertar_jugador(nickname, rol, equipo_id):
    # Inserta un nuevo jugador en la tabla 'jugadores'.
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("INSERT INTO jugadores (nickname, rol, equipo_id) VALUES (%s, %s, %s)", (nickname, rol, equipo_id))
                conn.commit()
                print(f"Jugador '{nickname}' insertado correctamente.")
            except psycopg.errors.UniqueViolation:
                print(f"Error: El nickname '{nickname}' ya existe.")
            except psycopg.errors.ForeignKeyViolation:
                print(f"Error: El equipo con ID {equipo_id} no existe.")

def leer_equipos():
    # Muestra la lista de equipos y sus jugadores.
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM equipos")
            equipos = cur.fetchall()
            for equipo in equipos:
                print(f"Equipo: {equipo['nombre']} (ID: {equipo['id']})")
                cur.execute("SELECT * FROM jugadores WHERE equipo_id = %s", (equipo['id'],))
                jugadores = cur.fetchall()
                if jugadores:
                    print("  Jugadores:")
                    for jugador in jugadores:
                        print(f"    - {jugador['nickname']} ({jugador['rol']})")
                else:
                    print("  No tiene jugadores.")

def actualizar_equipo(equipo_id, nuevo_nombre):
    # Actualiza el nombre de un equipo.
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("UPDATE equipos SET nombre = %s WHERE id = %s", (nuevo_nombre, equipo_id))
                conn.commit()
                if cur.rowcount > 0:
                    print(f"Equipo con ID {equipo_id} actualizado a '{nuevo_nombre}'.")
                else:
                    print(f"Error: No se encontró el equipo con ID {equipo_id}.")
            except psycopg.errors.UniqueViolation:
                print(f"Error: El nombre '{nuevo_nombre}' ya existe.")

def actualizar_jugador(jugador_id, nuevo_nickname):
    # Actualiza el nickname de un jugador.
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("UPDATE jugadores SET nickname = %s WHERE id = %s", (nuevo_nickname, jugador_id))
                conn.commit()
                if cur.rowcount > 0:
                    print(f"Jugador con ID {jugador_id} actualizado a '{nuevo_nickname}'.")
                else:
                    print(f"Error: No se encontró el jugador con ID {jugador_id}.")
            except psycopg.errors.UniqueViolation:
                print(f"Error: El nickname '{nuevo_nickname}' ya existe.")

def eliminar_jugador(jugador_id):
    # Elimina un jugador.
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM jugadores WHERE id = %s", (jugador_id,))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Jugador con ID {jugador_id} eliminado.")
            else:
                print(f"Error: No se encontró el jugador con ID {jugador_id}.")

def eliminar_equipo(equipo_id):
    # Elimina un equipo y sus jugadores.
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM equipos WHERE id = %s", (equipo_id,))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Equipo con ID {equipo_id} eliminado.")
            else:
                print(f"Error: No se encontró el equipo con ID {equipo_id}.")

def main():
    crear_tablas()
    while True:
        print("\nOpciones:")
        print("1. Insertar equipo")
        print("2. Insertar jugador")
        print("3. Leer equipos")
        print("4. Actualizar equipo")
        print("5. Actualizar jugador")
        print("6. Eliminar jugador")
        print("7. Eliminar equipo")
        print("8. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            nombre = input("Nombre del equipo: ")
            pais = input("País: ")
            entrenador = input("Entrenador: ")
            insertar_equipo(nombre, pais, entrenador)
        elif opcion == '2':
            nickname = input("Nickname del jugador: ")
            rol = input("Rol: ")
            equipo_id = int(input("ID del equipo: "))
            insertar_jugador(nickname, rol, equipo_id)
        elif opcion == '3':
            leer_equipos()
        elif opcion == '4':
            equipo_id = int(input("ID del equipo a actualizar: "))
            nuevo_nombre = input("Nuevo nombre del equipo: ")
            actualizar_equipo(equipo_id, nuevo_nombre)
        elif opcion == '5':
            jugador_id = int(input("ID del jugador a actualizar: "))
            nuevo_nickname = input("Nuevo nickname del jugador: ")
            actualizar_jugador(jugador_id, nuevo_nickname)
        elif opcion == '6':
            jugador_id = int(input("ID del jugador a eliminar: "))
            eliminar_jugador(jugador_id)
        elif opcion == '7':
            equipo_id = int(input("ID del equipo a eliminar: "))
            eliminar_equipo(equipo_id)
        elif opcion == '8':
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
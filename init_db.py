import sqlite3


con = sqlite3.connect("instance/aime_profe.sqlite")

cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS asistencia")

# crear tablas

cur.execute("""
    CREATE TABLE asistencia(
    id serial PRIMARY KEY, 
    apellido VARCHAR(50), 
    nombre VARCHAR(50), 
    ci VARCHAR(50), 
    asistencia INTEGER, 
    grado VARCHAR(20), 
    justificativo VARCHAR(100), 
    fecha VARCHAR(50))
""")

cur.execute(
    "INSERT INTO asistencia(id, apellido, nombre, ci, asistencia, grado, justificativo, fecha) VALUES (2, 'Kent', 'Clark', '123456', 0, '3M', 'Es kaigue', '23-11-2022');"
)

cur.execute(
    "INSERT INTO asistencia(id, apellido, nombre, ci, asistencia, grado, justificativo, fecha) VALUES (1, 'Parker', 'Peter', '123456', 0, '5T', 'trabaja a la noche', '23-11-2022');"
)

cur.execute(
    "INSERT INTO asistencia(id, apellido, nombre, ci, asistencia, grado, justificativo, fecha) VALUES (5, 'Rogers', 'Steve', '123456', 1, '3M', '---', '02-02-2023');"
)

cur.execute(
    "INSERT INTO asistencia(id, apellido, nombre, ci, asistencia, grado, justificativo, fecha) VALUES (6, 'Ruggilo', 'Fio', '123456', 1, '3M', '---', '23-11-2022');"
)

cur.execute(
    "INSERT INTO asistencia(id, apellido, nombre, ci, asistencia, grado, justificativo, fecha) VALUES (7, 'Del Puerto', 'Marcelo', '123456', 1, '3M', '---', '23-11-2022');"
)

cur.execute(
    "INSERT INTO asistencia(id, apellido, nombre, ci, asistencia, grado, justificativo, fecha) VALUES (9, 'Cabañas', 'Florencia', '123456', 1, '3M', '---', '23-11-2022');"
)

cur.execute(
    "INSERT INTO asistencia(id, apellido, nombre, ci, asistencia, grado, justificativo, fecha) VALUES (4, 'Midoriya', 'Izuku', '123456', 1, '3M', '---', '28-02-2023');"
)

cur.execute(
    "INSERT INTO asistencia(id, apellido, nombre, ci, asistencia, grado, justificativo, fecha) VALUES (99, 'Stark', 'Tony', '123456', 0, '5T', 'trabaja', '28-02-2023');"
)

con.commit()
cur.close()
con.close()
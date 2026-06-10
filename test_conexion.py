from conexion_db import ConexionDB

db = ConexionDB()
conn = db.conectar()

if conn:
    print("Conexión exitosa a videojuegos")
else:
    print("Algo falló, revisa usuario y contraseña")

db.cerrar()
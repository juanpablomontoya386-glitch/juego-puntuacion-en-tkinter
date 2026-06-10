from conexion_db import ConexionDB

class ScoresModel:
    def __init__(self):
        self.db = ConexionDB()

    # CREATE — guardar un score nuevo
    def guardar_score(self, jugador, puntuacion, nivel, tiempo):
        query = """
            INSERT INTO scores (jugador, puntuacion, nivel, tiempo)
            VALUES (%s, %s, %s, %s)
        """
        return self.db.ejecutar_consulta(query, (jugador, puntuacion, nivel, tiempo))

    # — obtener todos los scores
    def obtener_todos(self):
        query = "SELECT * FROM scores ORDER BY puntuacion DESC"
        return self.db.obtener_datos(query)

    # — obtener top 10 para el ranking
    def obtener_ranking(self):
        query = "SELECT * FROM scores ORDER BY puntuacion DESC LIMIT 10"
        return self.db.obtener_datos(query)

    # — actualizar un score existente
    def actualizar_score(self, id, jugador, puntuacion, nivel, tiempo):
        query = """
            UPDATE scores
            SET jugador=%s, puntuacion=%s, nivel=%s, tiempo=%s
            WHERE id=%s
        """
        return self.db.ejecutar_consulta(query, (jugador, puntuacion, nivel, tiempo, id))

    # — eliminar un score por su id
    def eliminar_score(self, id):
        query = "DELETE FROM scores WHERE id=%s"
        return self.db.ejecutar_consulta(query, (id,))
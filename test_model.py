from scores_model import ScoresModel

model = ScoresModel()

# Prueba CREATE
model.guardar_score("Juan", 4500, 7, "02:35")
model.guardar_score("Maria", 8200, 12, "05:10")
model.guardar_score("Carlos", 3100, 5, "01:50")

# Prueba READ
scores = model.obtener_todos()
for s in scores:
    print(s)
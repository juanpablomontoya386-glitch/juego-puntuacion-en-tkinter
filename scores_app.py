import tkinter as tk
from tkinter import ttk, messagebox
from scores_model import ScoresModel

class ScoresApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Puntuaciones - CRUD")
        self.root.geometry("700x500")
        self.model = ScoresModel()
        self.id_seleccionado = None

        # Pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Registrar Score")
        self.notebook.add(self.tab2, text="Editar / Eliminar")
        self.notebook.add(self.tab3, text="Ranking Top 10")

        self.construir_tab1()
        self.construir_tab2()
        self.construir_tab3()

    # ─── PESTAÑA 1 ───────────────────────────────────────────
    def construir_tab1(self):
        frame = ttk.LabelFrame(self.tab1, text="Datos del Score")
        frame.pack(padx=20, pady=20, fill="x")

        ttk.Label(frame, text="Jugador:").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.entry_jugador = ttk.Entry(frame, width=30)
        self.entry_jugador.grid(row=0, column=1, padx=10, pady=8)

        ttk.Label(frame, text="Puntuación:").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.entry_puntuacion = ttk.Entry(frame, width=30)
        self.entry_puntuacion.grid(row=1, column=1, padx=10, pady=8)

        ttk.Label(frame, text="Nivel:").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.entry_nivel = ttk.Entry(frame, width=30)
        self.entry_nivel.grid(row=2, column=1, padx=10, pady=8)

        ttk.Label(frame, text="Tiempo:").grid(row=3, column=0, padx=10, pady=8, sticky="w")
        self.entry_tiempo = ttk.Entry(frame, width=30)
        self.entry_tiempo.grid(row=3, column=1, padx=10, pady=8)

        ttk.Button(frame, text="Guardar", command=self.guardar).grid(row=4, column=0, padx=10, pady=12)
        ttk.Button(frame, text="Limpiar", command=self.limpiar_tab1).grid(row=4, column=1, padx=10, pady=12)

    def guardar(self):
        jugador    = self.entry_jugador.get().strip()
        puntuacion = self.entry_puntuacion.get().strip()
        nivel      = self.entry_nivel.get().strip()
        tiempo     = self.entry_tiempo.get().strip()

        if not jugador or not puntuacion or not nivel or not tiempo:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
            return

        try:
            self.model.guardar_score(jugador, int(puntuacion), int(nivel), tiempo)
            messagebox.showinfo("Éxito", "Score guardado correctamente.")
            self.limpiar_tab1()
            self.cargar_tabla()
        except ValueError:
            messagebox.showerror("Error", "Puntuación y Nivel deben ser números enteros.")

    def limpiar_tab1(self):
        self.entry_jugador.delete(0, tk.END)
        self.entry_puntuacion.delete(0, tk.END)
        self.entry_nivel.delete(0, tk.END)
        self.entry_tiempo.delete(0, tk.END)

    # ─── PESTAÑA 2 ───────────────────────────────────────────
    def construir_tab2(self):
        frame_form = ttk.LabelFrame(self.tab2, text="Editar Score Seleccionado")
        frame_form.pack(padx=20, pady=10, fill="x")

        ttk.Label(frame_form, text="Jugador:").grid(row=0, column=0, padx=10, pady=6, sticky="w")
        self.entry_jugador2 = ttk.Entry(frame_form, width=25)
        self.entry_jugador2.grid(row=0, column=1, padx=10, pady=6)

        ttk.Label(frame_form, text="Puntuación:").grid(row=0, column=2, padx=10, pady=6, sticky="w")
        self.entry_puntuacion2 = ttk.Entry(frame_form, width=15)
        self.entry_puntuacion2.grid(row=0, column=3, padx=10, pady=6)

        ttk.Label(frame_form, text="Nivel:").grid(row=1, column=0, padx=10, pady=6, sticky="w")
        self.entry_nivel2 = ttk.Entry(frame_form, width=25)
        self.entry_nivel2.grid(row=1, column=1, padx=10, pady=6)

        ttk.Label(frame_form, text="Tiempo:").grid(row=1, column=2, padx=10, pady=6, sticky="w")
        self.entry_tiempo2 = ttk.Entry(frame_form, width=15)
        self.entry_tiempo2.grid(row=1, column=3, padx=10, pady=6)

        ttk.Button(frame_form, text="Actualizar", command=self.actualizar).grid(row=2, column=1, pady=10)
        ttk.Button(frame_form, text="Eliminar",   command=self.eliminar).grid(row=2, column=2, pady=10)
        ttk.Button(frame_form, text="Limpiar",    command=self.limpiar_tab2).grid(row=2, column=3, pady=10)

        # Tabla
        cols = ("ID", "Jugador", "Puntuación", "Nivel", "Tiempo", "Fecha")
        self.tabla = ttk.Treeview(self.tab2, columns=cols, show="headings", height=8)
        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100, anchor="center")
        self.tabla.pack(padx=20, pady=5, fill="both")
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)
        self.cargar_tabla()

    def cargar_tabla(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        for s in self.model.obtener_todos():
            self.tabla.insert("", "end", values=(
                s["id"], s["jugador"], s["puntuacion"],
                s["nivel"], s["tiempo"], s["fecha"]
            ))

    def seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            valores = self.tabla.item(seleccion[0])["values"]
            self.id_seleccionado = valores[0]
            self.entry_jugador2.delete(0, tk.END);    self.entry_jugador2.insert(0, valores[1])
            self.entry_puntuacion2.delete(0, tk.END); self.entry_puntuacion2.insert(0, valores[2])
            self.entry_nivel2.delete(0, tk.END);      self.entry_nivel2.insert(0, valores[3])
            self.entry_tiempo2.delete(0, tk.END);     self.entry_tiempo2.insert(0, valores[4])

    def actualizar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Sin selección", "Selecciona un registro de la tabla.")
            return
        try:
            self.model.actualizar_score(
                self.id_seleccionado,
                self.entry_jugador2.get().strip(),
                int(self.entry_puntuacion2.get().strip()),
                int(self.entry_nivel2.get().strip()),
                self.entry_tiempo2.get().strip()
            )
            messagebox.showinfo("Éxito", "Score actualizado correctamente.")
            self.limpiar_tab2()
            self.cargar_tabla()
        except ValueError:
            messagebox.showerror("Error", "Puntuación y Nivel deben ser números enteros.")

    def eliminar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Sin selección", "Selecciona un registro de la tabla.")
            return
        if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este registro?"):
            self.model.eliminar_score(self.id_seleccionado)
            messagebox.showinfo("Éxito", "Score eliminado correctamente.")
            self.limpiar_tab2()
            self.cargar_tabla()

    def limpiar_tab2(self):
        self.id_seleccionado = None
        self.entry_jugador2.delete(0, tk.END)
        self.entry_puntuacion2.delete(0, tk.END)
        self.entry_nivel2.delete(0, tk.END)
        self.entry_tiempo2.delete(0, tk.END)

    # ─── PESTAÑA 3 ───────────────────────────────────────────
    def construir_tab3(self):
        ttk.Label(self.tab3, text="Top 10 — Mejores Puntuaciones",
                  font=("Arial", 13, "bold")).pack(pady=15)

        cols = ("#", "Jugador", "Puntuación", "Nivel", "Tiempo")
        self.tabla_ranking = ttk.Treeview(self.tab3, columns=cols, show="headings", height=10)
        for col in cols:
            self.tabla_ranking.heading(col, text=col)
            self.tabla_ranking.column(col, width=120, anchor="center")
        self.tabla_ranking.pack(padx=20, fill="both")

        ttk.Button(self.tab3, text="Actualizar Ranking",
                   command=self.cargar_ranking).pack(pady=10)
        self.cargar_ranking()

    def cargar_ranking(self):
        for row in self.tabla_ranking.get_children():
            self.tabla_ranking.delete(row)
        for i, s in enumerate(self.model.obtener_ranking(), start=1):
            self.tabla_ranking.insert("", "end", values=(
                i, s["jugador"], s["puntuacion"], s["nivel"], s["tiempo"]
            ))

# ─── MAIN ─────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = ScoresApp(root)
    root.mainloop()
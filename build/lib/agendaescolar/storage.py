import json
import os

class Storage:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.all_data = {}
        self.current_user = None
        self.cargar_datos()

    @property
    def materias(self):
        if self.current_user:
            return self.all_data[self.current_user]["materias"]
        return []

    @property
    def notas(self):
        if self.current_user:
            return self.all_data[self.current_user]["notas"]
        return []

    @property
    def inasistencias(self):
        if self.current_user:
            return self.all_data[self.current_user].get("inasistencias", 0)
        return 0

    @property
    def comentario(self):
        if self.current_user:
            return self.all_data[self.current_user].get("comentario", "")
        return ""

    def get_user_list(self):
        return list(self.all_data.keys())

    def set_current_user(self, username):
        self.current_user = username
        if username not in self.all_data:
            self.all_data[username] = {
                "materias": [],
                "notas": [],
                "inasistencias": 0,
                "comentario": ""
            }
            self.guardar_datos()

    def agregar_materia(self, materia, nota):
        if self.current_user:
            self.materias.append(materia)
            self.notas.append(nota)
            self.guardar_datos()

    def eliminar_materia(self, index):
        if self.current_user and 0 <= index < len(self.materias):
            self.materias.pop(index)
            self.notas.pop(index)
            self.guardar_datos()

    def modificar_materia(self, index, materia, nota):
        if self.current_user and 0 <= index < len(self.materias):
            self.materias[index] = materia
            self.notas[index] = nota
            self.guardar_datos()

    def eliminar_usuario(self, username):
        if username in self.all_data:
            del self.all_data[username]
            self.guardar_datos()
            if self.current_user == username:
                self.current_user = None

    def actualizar_inasistencias(self, cantidad):
        if self.current_user:
            self.all_data[self.current_user]['inasistencias'] = max(0, cantidad)
            self.guardar_datos()

    def actualizar_comentario(self, texto):
        if self.current_user:
            self.all_data[self.current_user]['comentario'] = texto
            self.guardar_datos()

    def guardar_datos(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.all_data, f, ensure_ascii=False, indent=4)

    def cargar_datos(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self.all_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.all_data = {}
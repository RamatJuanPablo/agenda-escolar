import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class UserSelectionDialog(simpledialog.Dialog):
    """Diálogo personalizado para seleccionar un usuario de una lista."""
    def __init__(self, parent, title, user_list):
        self.user_list = user_list
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Seleccione un usuario:").pack()
        self.listbox = tk.Listbox(master)
        self.listbox.pack(padx=5, pady=5)
        for user in self.user_list:
            self.listbox.insert(tk.END, user)
        
        if self.user_list:
            self.listbox.select_set(0) # Seleccionar el primer item por defecto
        return self.listbox # set initial focus

    def apply(self):
        selected_indices = self.listbox.curselection()
        if selected_indices:
            self.result = self.user_list[selected_indices[0]]


class AgendaEscolarUI:
    def __init__(self, master, storage):
        self.master = master
        self.storage = storage

        master.title("Agenda Escolar")

        # Label para mostrar el usuario actual
        self.label_usuario = tk.Label(master, text="", font=("Arial", 12, "bold"))
        self.label_usuario.grid(row=0, column=0, columnspan=3, pady=(5, 10))

        # Tabla
        self.tree = ttk.Treeview(master, columns=("Materia", "Nota"), show="headings")
        self.tree.heading("Materia", text="Materia")
        self.tree.heading("Nota", text="Nota")
        self.tree.grid(row=1, column=0, columnspan=3, pady=(0, 10))

        # Entradas
        tk.Label(master, text="Materia:").grid(row=2, column=0)
        self.entry_materia = tk.Entry(master)
        self.entry_materia.grid(row=2, column=1)

        tk.Label(master, text="Nota:").grid(row=3, column=0)
        self.entry_nota = tk.Entry(master)
        self.entry_nota.grid(row=3, column=1)

        # Frame para botones de acción
        action_frame = tk.Frame(master)
        action_frame.grid(row=4, column=0, columnspan=3, pady=(10,0))
        tk.Button(action_frame, text="Agregar", command=self.agregar_materia).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Modificar", command=self.modificar_materia).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Eliminar", command=self.eliminar_materia).pack(side=tk.LEFT, padx=5)

# Etiqueta de promedio
        self.label_promedio = tk.Label(master, text="Promedio: 0.00")
        self.label_promedio.grid(row=5, column=0, columnspan=3, pady=(5, 5))

        # --- Inasistencias ---
        inasistencias_frame = tk.Frame(master)
        inasistencias_frame.grid(row=6, column=0, columnspan=3, pady=5)
        tk.Label(inasistencias_frame, text="Inasistencias:").pack(side=tk.LEFT)
        self.label_inasistencias = tk.Label(inasistencias_frame, text="0", width=4)
        self.label_inasistencias.pack(side=tk.LEFT)
        tk.Button(inasistencias_frame, text="-", command=self.decrementar_inasistencia).pack(side=tk.LEFT)
        tk.Button(inasistencias_frame, text="+", command=self.incrementar_inasistencia).pack(side=tk.LEFT)

        # --- Comentarios ---
        comentarios_frame = tk.LabelFrame(master, text="Comentarios Generales")
        comentarios_frame.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        self.text_comentario = tk.Text(comentarios_frame, height=4, wrap=tk.WORD)
        self.text_comentario.pack(side=tk.TOP, fill=tk.X, expand=True, padx=5, pady=5)
        self.text_comentario.bind("<FocusOut>", self.guardar_comentario_auto)

        # --- Etiqueta del Creador ---
        creator_label = tk.Label(master, text="Creado por: Ramat, Juan Pablo", font=("Arial", 8, "italic"), fg="grey")
        creator_label.grid(row=8, column=0, columnspan=3, pady=(10, 5))

        # --- Menú de Usuario ---
        self.crear_menu()

        # --- Lógica de inicio ---
        self.master.withdraw() # Ocultar ventana principal al inicio
        self.seleccionar_usuario_inicial()

    def crear_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        user_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Usuario", menu=user_menu)
        user_menu.add_command(label="Cambiar de Usuario", command=self.cambiar_usuario)
        user_menu.add_command(label="Crear Nuevo Usuario", command=self.crear_nuevo_usuario)
        user_menu.add_command(label="Eliminar Usuario Actual", command=self.eliminar_usuario_actual)
        user_menu.add_separator()
        user_menu.add_command(label="Salir", command=self.master.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de...", command=self.mostrar_acerca_de)

    def mostrar_acerca_de(self):
        """Muestra una ventana con información sobre la aplicación."""
        messagebox.showinfo("Acerca de Agenda Escolar", "Agenda Escolar v0.1.0\n\nCreado por: Ramat, Juan Pablo\nEmail:ramatjuanpablo@gmail.com")

    def eliminar_usuario_actual(self):
        if not self.storage.current_user:
            messagebox.showerror("Error", "No hay ningún usuario seleccionado.")
            return

        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar permanentemente al usuario '{self.storage.current_user}' y todos sus datos?"):
            user_to_delete = self.storage.current_user
            self.storage.eliminar_usuario(user_to_delete)
            messagebox.showinfo("Usuario Eliminado", f"El usuario '{user_to_delete}' ha sido eliminado.")
            
            # Resetear la UI para seleccionar otro usuario o crear uno nuevo
            self.master.withdraw()
            self.seleccionar_usuario_inicial()

    def seleccionar_usuario_inicial(self):
        user_list = self.storage.get_user_list()
        if user_list:
            self.cambiar_usuario()
        else:
            self.crear_nuevo_usuario()

    def cambiar_usuario(self):
        user_list = self.storage.get_user_list()
        if not user_list:
            messagebox.showinfo("Sin Usuarios", "No hay usuarios creados. Por favor, cree uno nuevo.")
            self.crear_nuevo_usuario()
            return
        
        dialog = UserSelectionDialog(self.master, "Seleccionar Usuario", user_list)
        chosen_user = dialog.result
        if chosen_user:
            self.cargar_boletin(chosen_user)

    def crear_nuevo_usuario(self):
        new_user = simpledialog.askstring("Nuevo Usuario", "Ingrese el nombre del nuevo usuario:", parent=self.master)
        if new_user:
            if new_user in self.storage.get_user_list():
                messagebox.showwarning("Usuario Existente", "Este usuario ya existe. Cargando su boletín.")
            self.cargar_boletin(new_user)

    def cargar_boletin(self, username):
        self.storage.set_current_user(username)
        self.label_usuario.config(text=f"Boletín de: {username}")
        self.actualizar_tabla()
        self.label_inasistencias.config(text=str(self.storage.inasistencias))
        self.text_comentario.delete("1.0", tk.END)
        self.text_comentario.insert("1.0", self.storage.comentario)
        self.master.deiconify() # Mostrar la ventana principal

    def actualizar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for materia, nota in zip(self.storage.materias, self.storage.notas):
            self.tree.insert("", tk.END, values=(materia, nota))
        self.label_inasistencias.config(text=str(self.storage.inasistencias))
        self.actualizar_promedio()
    
    def actualizar_promedio(self):
        if self.storage.notas:
            promedio = sum(self.storage.notas) / len(self.storage.notas)
            self.label_promedio.config(text=f"Promedio: {promedio:.2f}")
        else:
            self.label_promedio.config(text="Promedio: 0.00")

    def agregar_materia(self):
        materia = self.entry_materia.get()
        try:
            nota = float(self.entry_nota.get())
        except ValueError:
            messagebox.showerror("Error", "La nota debe ser un número.")
            return
        if not materia:
            messagebox.showerror("Error", "Ingrese el nombre de la materia.")
            return
        if 0 <= nota <= 10:
            self.storage.agregar_materia(materia, nota)
            self.actualizar_tabla()
            self.entry_materia.delete(0, tk.END)
            self.entry_nota.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "La nota debe estar entre 0 y 10.")

    def modificar_materia(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una materia para modificar.")
            return

        index = self.tree.index(selected_item[0])
        
        materia_actual = self.storage.materias[index] # Accede a la propiedad
        nota_actual = self.storage.notas[index]
        
        nueva_nota_str = simpledialog.askstring("Modificar Nota", "Nueva nota:", initialvalue=str(nota_actual))
        if nueva_nota_str is None: return # El usuario canceló

        try:
            nueva_nota = float(nueva_nota_str)
            if 0 <= nueva_nota <= 10:
                self.storage.modificar_materia(index, materia_actual, nueva_nota)
                self.actualizar_tabla()
            else:
                messagebox.showerror("Error", "La nota debe estar entre 0 y 10.")
        except ValueError:
            messagebox.showerror("Error", "La nota debe ser un número.")

    def eliminar_materia(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una materia para eliminar.")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar la materia seleccionada?"):
            index = self.tree.index(selected_item[0])
            self.storage.eliminar_materia(index)
            self.actualizar_tabla()

    def incrementar_inasistencia(self):
        nueva_cantidad = self.storage.inasistencias + 1
        self.storage.actualizar_inasistencias(nueva_cantidad)
        self.label_inasistencias.config(text=str(nueva_cantidad))

    def decrementar_inasistencia(self):
        nueva_cantidad = self.storage.inasistencias - 1
        if nueva_cantidad >= 0:
            self.storage.actualizar_inasistencias(nueva_cantidad)
            self.label_inasistencias.config(text=str(nueva_cantidad))

    def guardar_comentario_auto(self, event=None):
        """Guarda el comentario cuando el cuadro de texto pierde el foco."""
        comentario_actual = self.text_comentario.get("1.0", tk.END).strip()
        self.storage.actualizar_comentario(comentario_actual)
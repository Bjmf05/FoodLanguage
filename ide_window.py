import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from lexer import Lexer
from parser import CulinaryParser
from interpreter import CulinaryInterpreter
import io
import sys
import os

# Importar módulos
from code_templates import CODE_TEMPLATES, EXAMPLE_NAMES, EXAMPLE_CODES
from ui_components import (
    create_info_window,
    KEYWORDS_CONTENT, DATA_TYPES_CONTENT, SPECIAL_VALUES_CONTENT,
    ARITHMETIC_CONTENT, COMPARISON_CONTENT, LOGICAL_CONTENT,
    SEMANTICS_VARIABLES_CONTENT, SEMANTICS_FUNCTIONS_CONTENT, 
    SEMANTICS_SCOPE_CONTENT, ABOUT_TEXT
)

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, funciona para dev y para PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
class FoodLanguageIDE:
    """Clase principal del IDE de FoodLanguage"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("FoodLanguage IDE - Lenguaje Culinario")
        self.root.geometry("1400x800")
        self.root.configure(bg='#2b2b2b')
        
        # Variables de estado
        self.current_code = ""
        self.ast = None
        self.current_file = None
        self.file_modified = False
        self.compilation_successful = False
        self.last_compiled_code = ""
        
        # Configurar la interfaz
        self.setup_style()
        self.create_menu()
        self.create_main_layout()
        self.setup_bindings()
        
        # Ícono de la ventana
        icon_path = resource_path('foodIcon.png')  # Ruta del ícono
        icon_image = tk.PhotoImage(file=icon_path)
        self.root.iconphoto(False, icon_image)
    
    def setup_style(self):
        """Configurar estilo de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores del tema
        bg_dark = '#2b2b2b'
        bg_medium = '#3c3c3c'
        bg_light = '#4a4a4a'
        fg_color = '#e0e0e0'
        accent = '#4a9eff'
        
        style.configure('TFrame', background=bg_dark)
        style.configure('TLabel', background=bg_dark, foreground=fg_color)
        style.configure('TButton', background=bg_medium, foreground=fg_color, 
                       borderwidth=1, focuscolor='none', padding=10)
        style.map('TButton', background=[('active', accent)])
    
    def setup_bindings(self):
        """Configurar atajos de teclado y eventos"""
        self.code_text.bind('<<Modified>>', self.on_text_modified)
        
        # Atajos de teclado
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_file_as())
        
        # Protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    #  Creación de menú
    
    def create_menu(self):
        """Crear menú """
        menubar = tk.Menu(self.root, bg='#3c3c3c', fg='#e0e0e0')
        self.root.config(menu=menubar)
        
        self._create_file_menu(menubar)
        self._create_keywords_menu(menubar)
        self._create_syntax_menu(menubar)
        self._create_semantic_menu(menubar)
        self._create_types_menu(menubar)
        self._create_help_menu(menubar)
    
    def _create_file_menu(self, menubar):
        """Crear menú Archivo"""
        file_menu = tk.Menu(menubar, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Abrir...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Guardar", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Guardar como...", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Limpiar", command=self.clear_code)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.on_closing)
    
    def _create_keywords_menu(self, menubar):
        """Crear menú Palabras Reservadas"""
        keywords_menu = tk.Menu(menubar, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        menubar.add_cascade(label="Palabras Reservadas", menu=keywords_menu)
        keywords_menu.add_command(label="Ver todas", command=self.show_keywords)
        keywords_menu.add_command(label="Tipos de datos", command=self.show_data_types)
        keywords_menu.add_command(label="Valores especiales", command=self.show_special_values)
    
    def _create_syntax_menu(self, menubar):
        """Crear menú Sintaxis"""
        syntax_menu = tk.Menu(menubar, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        menubar.add_cascade(label="Sintaxis", menu=syntax_menu)
        
        # Submenú Control
        control_menu = tk.Menu(syntax_menu, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        syntax_menu.add_cascade(label="Estructuras de Control", menu=control_menu)
        control_menu.add_command(label="if-else", command=lambda: self.insert_template('if'))
        control_menu.add_command(label="while", command=lambda: self.insert_template('while'))
        control_menu.add_command(label="for", command=lambda: self.insert_template('for'))
        control_menu.add_command(label="switch", command=lambda: self.insert_template('switch'))
        
        # Submenú Funciones
        functions_menu = tk.Menu(syntax_menu, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        syntax_menu.add_cascade(label="Funciones", menu=functions_menu)
        functions_menu.add_command(label="Definir función", command=lambda: self.insert_template('function'))
        functions_menu.add_command(label="Llamar función", command=lambda: self.insert_template('call'))
        
        # Submenú Entrada/Salida
        io_menu = tk.Menu(syntax_menu, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        syntax_menu.add_cascade(label="Entrada/Salida", menu=io_menu)
        io_menu.add_command(label="add (Input)", command=lambda: self.insert_template('input'))
        io_menu.add_command(label="taste (Print)", command=lambda: self.insert_template('print'))
        
        # Submenú Operaciones
        operations_menu = tk.Menu(syntax_menu, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        syntax_menu.add_cascade(label="Operaciones", menu=operations_menu)
        operations_menu.add_command(label="Aritméticas", command=self.show_arithmetic)
        operations_menu.add_command(label="Comparación", command=self.show_comparison)
        operations_menu.add_command(label="Lógicas", command=self.show_logical)
    
    def _create_semantic_menu(self, menubar):
        """Crear menú Semántica"""
        semantic_menu = tk.Menu(menubar, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        menubar.add_cascade(label="Semántica", menu=semantic_menu)
        semantic_menu.add_command(label="Variables", command=self.show_semantics_variables)
        semantic_menu.add_command(label="Funciones", command=self.show_semantics_functions)
        semantic_menu.add_command(label="Alcance (Scope)", command=self.show_semantics_scope)
    
    def _create_types_menu(self, menubar):
        """Crear menú Tipos de Datos"""
        types_menu = tk.Menu(menubar, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        menubar.add_cascade(label="Tipos de Datos", menu=types_menu)
        types_menu.add_command(label="quantity (entero)", command=lambda: self.insert_template('int'))
        types_menu.add_command(label="portion (flotante)", command=lambda: self.insert_template('float'))
        types_menu.add_command(label="ingredient (string)", command=lambda: self.insert_template('string'))
        types_menu.add_command(label="menu (lista)", command=lambda: self.insert_template('list'))
        types_menu.add_command(label="menu 2D (matriz)", command=lambda: self.insert_template('matrix'))
    
    def _create_help_menu(self, menubar):
        """Crear menú Ayuda"""
        help_menu = tk.Menu(menubar, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Ejemplos", command=self.show_examples)
        help_menu.add_command(label="Acerca de", command=self.show_about)
    
    # Layout principal
    
    def create_main_layout(self):
        """Crear el layout principal"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Paneles izquierdo y derecho
        self._create_left_panel(main_frame)
        self._create_right_panel(main_frame)
    
    def _create_left_panel(self, parent):
        """Crear panel izquierdo - Editor de código"""
        left_panel = ttk.Frame(parent)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        

        editor_label = ttk.Label(left_panel, text="Editor de Código", 
                                font=('Consolas', 12, 'bold'))
        editor_label.pack(pady=(0, 5))
        
        # Frame contenedor para editor con números de línea
        editor_frame = ttk.Frame(left_panel)
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        # Widget para números de línea
        self.line_numbers = tk.Text(
            editor_frame,
            width=4,
            padx=5,
            pady=10,
            font=('Consolas', 11),
            bg='#2d2d2d',
            fg='#858585',
            relief=tk.FLAT,
            state=tk.DISABLED,
            takefocus=0,
            cursor='arrow'
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Área de texto para código
        self.code_text = tk.Text(
            editor_frame,
            wrap=tk.NONE,
            width=60,
            height=30,
            font=('Consolas', 11),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='#ffffff',
            selectbackground='#264f78',
            relief=tk.FLAT,
            padx=10,
            pady=10,
            undo=True,
            maxundo=-1
        )
        self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar para el editor
        scrollbar = tk.Scrollbar(editor_frame, command=self._on_scroll)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar scroll
        self.code_text.config(yscrollcommand=scrollbar.set)
        
        # Bind eventos para actualizar números de línea
        self.code_text.bind('<KeyRelease>', self._update_line_numbers)
        self.code_text.bind('<MouseWheel>', self._update_line_numbers)
        self.code_text.bind('<Button-1>', self._update_line_numbers)
        
        # Inicializar números de línea
        self._update_line_numbers()
        
        # Frame de botones
        self._create_button_frame(left_panel)
    
    def _create_button_frame(self, parent):
        """Crear frame con botones de acción"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=10)
        
        # Boton compilar
        self.compile_btn = tk.Button(
            button_frame,
            text="Compilar",
            command=self.compile_code,
            bg='#0e639c',
            fg='white',
            font=('Arial', 11, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.compile_btn.pack(side=tk.LEFT, padx=5)
        
        # Boton Ejecutar
        self.run_btn = tk.Button(
            button_frame,
            text="Ejecutar",
            command=self.run_code,
            bg='#16825d',
            fg='white',
            font=('Arial', 11, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.run_btn.pack(side=tk.LEFT, padx=5)
        
        # Boton Limpiar
        clear_btn = tk.Button(
            button_frame,
            text="Limpiar",
            command=self.clear_all,
            bg='#a51d2d',
            fg='white',
            font=('Arial', 11, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
    
    def _create_right_panel(self, parent):
        """Crear panel derecho - Output"""
        right_panel = ttk.Frame(parent)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Título del output
        output_label = ttk.Label(right_panel, text="Salida / Errores", 
                                font=('Consolas', 12, 'bold'))
        output_label.pack(pady=(0, 5))
        
        # Frame contenedor para output y input
        console_frame = ttk.Frame(right_panel)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de output
        self.output_text = scrolledtext.ScrolledText(
            console_frame,
            wrap=tk.WORD,
            width=50,
            height=30,
            font=('Consolas', 10),
            bg='#1e1e1e',
            fg='#d4d4d4',
            relief=tk.FLAT,
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame para input (inicialmente oculto)
        self.input_frame = ttk.Frame(console_frame)
        
        # Label para el prompt
        self.input_label = ttk.Label(
            self.input_frame,
            text="",
            font=('Consolas', 10),
            foreground='#9cdcfe'
        )
        self.input_label.pack(side=tk.LEFT, padx=(5, 5))
        
        # Entry para el input del usuario
        self.input_entry = tk.Entry(
            self.input_frame,
            font=('Consolas', 10),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='#ffffff',
            relief=tk.FLAT
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Variable para almacenar el resultado del input
        self.input_result = None
        self.waiting_for_input = False
        
        # Configurar tags para colores
        self.output_text.tag_config('error', foreground='#f48771')
        self.output_text.tag_config('success', foreground='#4ec9b0')
        self.output_text.tag_config('info', foreground='#9cdcfe')
        self.output_text.tag_config('prompt', foreground='#dcdcaa')
        self.output_text.tag_config('input', foreground='#4fc1ff')
    
    # Archivos
    
    def new_file(self):
        """Crear nuevo archivo"""
        if self.file_modified:
            response = messagebox.askyesnocancel(
                "Archivo sin guardar",
                "¿Deseas guardar los cambios antes de crear un nuevo archivo?"
            )
            if response is None:
                return
            elif response:
                self.save_file()
        
        self.code_text.delete(1.0, tk.END)
        self.current_file = None
        self.file_modified = False
        self.update_title()
        self.clear_output()
    
    def open_file(self):
        """Abrir un archivo existente"""
        if self.file_modified:
            response = messagebox.askyesnocancel(
                "Archivo sin guardar",
                "¿Deseas guardar los cambios antes de abrir otro archivo?"
            )
            if response is None:
                return
            elif response:
                self.save_file()
        
        file_path = filedialog.askopenfilename(
            title="Abrir archivo",
            filetypes=[
                ("FoodLanguage Files", "*.food"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ],
            defaultextension=".food"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.code_text.delete(1.0, tk.END)
                    self.code_text.insert(1.0, content)
                    self.current_file = file_path
                    self.file_modified = False
                    self.update_title()
                    self.write_output(f"Archivo abierto: {os.path.basename(file_path)}", 'success')
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{str(e)}")
    
    def save_file(self):
        """Guardar el archivo actual"""
        if self.current_file:
            try:
                content = self.code_text.get(1.0, tk.END)
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.file_modified = False
                self.update_title()
                self.write_output(f"Archivo guardado: {os.path.basename(self.current_file)}", 'success')
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """Guardar el archivo con un nuevo nombre"""
        file_path = filedialog.asksaveasfilename(
            title="Guardar archivo como",
            filetypes=[
                ("FoodLanguage Files", "*.food"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ],
            defaultextension=".food"
        )
        
        if file_path:
            try:
                content = self.code_text.get(1.0, tk.END)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.current_file = file_path
                self.file_modified = False
                self.update_title()
                self.write_output(f"Archivo guardado como: {os.path.basename(file_path)}", 'success')
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")
    
    def on_text_modified(self, event=None):
        """Evento cuando el texto es modificado"""
        if self.code_text.edit_modified():
            self.file_modified = True
            self.update_title()
            self.code_text.edit_modified(False)
    
    def update_title(self):
        """Actualizar el título de la ventana"""
        title = "FoodLanguage IDE"
        if self.current_file:
            title += f" - {os.path.basename(self.current_file)}"
        else:
            title += " - Nuevo archivo"
        
        if self.file_modified:
            title += " *"
        
        self.root.title(title)
    
    def on_closing(self):
        """Manejar el evento de cierre de la ventana"""
        if self.file_modified:
            response = messagebox.askyesnocancel(
                "Archivo sin guardar",
                "¿Deseas guardar los cambios antes de salir?"
            )
            if response is None:
                return
            elif response:
                self.save_file()
        
        self.root.destroy()
    
    # Números de línea
    
    def _update_line_numbers(self, event=None):
        """Actualizar los números de línea"""
        # Obtener el contenido actual
        line_count = self.code_text.get(1.0, tk.END).count('\n')
        
        # Generar números de línea
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count + 1))
        
        # Actualizar el widget de números de línea
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        self.line_numbers.insert(1.0, line_numbers_string)
        self.line_numbers.config(state=tk.DISABLED)
        
        # Sincronizar el scroll
        self._sync_scroll()
    
    def _on_scroll(self, *args):
        """Manejar el scroll del editor"""
        self.code_text.yview(*args)
        self.line_numbers.yview(*args)
    
    def _sync_scroll(self):
        """Sincronizar el scroll entre el editor y los números de línea"""
        self.line_numbers.yview_moveto(self.code_text.yview()[0])

    # Interfaz de usuario

    def clear_code(self):
        """Limpiar el editor de código"""
        self.code_text.delete(1.0, tk.END)
    
    def clear_all(self):
        """Limpiar código y output"""
        self.clear_code()
        self.clear_output()
    
    def clear_output(self):
        """Limpiar el área de output"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def write_output(self, text, tag=None):
        """Escribir en el área de output"""
        self.output_text.config(state=tk.NORMAL)
        if tag:
            self.output_text.insert(tk.END, text, tag)
        else:
            self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    # Ventanas de información
    
    def show_keywords(self):
        """Mostrar todas las palabras reservadas"""
        create_info_window(self.root, "Palabras Reservadas - FoodLanguage", KEYWORDS_CONTENT)
    
    def show_data_types(self):
        """Mostrar información sobre tipos de datos"""
        create_info_window(self.root, "Tipos de Datos", DATA_TYPES_CONTENT, 600, 500)
    
    def show_special_values(self):
        """Mostrar valores especiales"""
        create_info_window(self.root, "Valores Especiales", SPECIAL_VALUES_CONTENT, 500, 300)
    
    def show_arithmetic(self):
        """Mostrar operaciones aritméticas"""
        create_info_window(self.root, "Operaciones Aritméticas", ARITHMETIC_CONTENT, 600, 400)
    
    def show_comparison(self):
        """Mostrar operadores de comparación"""
        create_info_window(self.root, "Operadores de Comparación", COMPARISON_CONTENT, 600, 450)
    
    def show_logical(self):
        """Mostrar operadores lógicos"""
        create_info_window(self.root, "Operadores Lógicos", LOGICAL_CONTENT, 600, 400)
       
    def show_semantics_variables(self):
        """Mostrar semántica de variables"""
        create_info_window(self.root, "Semántica - Variables", SEMANTICS_VARIABLES_CONTENT, 700, 500)
    
    def show_semantics_functions(self):
        """Mostrar semántica de funciones"""
        create_info_window(self.root, "Semántica - Funciones", SEMANTICS_FUNCTIONS_CONTENT, 700, 550)
    
    def show_semantics_scope(self):
        """Mostrar semántica de alcance"""
        create_info_window(self.root, "Semántica - Alcance (Scope)", SEMANTICS_SCOPE_CONTENT, 700, 550)
    
    def show_about(self):
        """Mostrar información sobre el IDE"""
        messagebox.showinfo("Acerca de FoodLanguage", ABOUT_TEXT)
    
    # Ejemplos
    
    def show_examples(self):
        """Mostrar ventana de ejemplos"""
        examples_window = tk.Toplevel(self.root)
        examples_window.title("Ejemplos - FoodLanguage")
        examples_window.geometry("800x600")
        examples_window.configure(bg='#2b2b2b')
        
        # Frame para lista y botones
        frame = ttk.Frame(examples_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lista de ejemplos
        label = ttk.Label(frame, text="Seleccione un ejemplo:", 
                         font=('Arial', 11, 'bold'))
        label.pack(pady=(0, 10))
        
        listbox = tk.Listbox(frame, font=('Consolas', 10), 
                            bg='#1e1e1e', fg='#d4d4d4',
                            selectbackground='#264f78',
                            height=20)
        listbox.pack(fill=tk.BOTH, expand=True)
        
        for ex in EXAMPLE_NAMES:
            listbox.insert(tk.END, ex)
        
        # Botón para cargar ejemplo
        def load_example():
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                self.insert_example(idx)
                examples_window.destroy()
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        load_btn = tk.Button(btn_frame, text="Cargar Ejemplo", 
                            command=load_example,
                            bg='#0e639c', fg='white',
                            font=('Arial', 10, 'bold'),
                            padx=20, pady=8)
        load_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="Cancelar", 
                              command=examples_window.destroy,
                              bg='#5a5a5a', fg='white',
                              font=('Arial', 10, 'bold'),
                              padx=20, pady=8)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def insert_example(self, idx):
        """Insertar código de ejemplo en el editor"""
        if 0 <= idx < len(EXAMPLE_CODES):
            self.code_text.delete(1.0, tk.END)
            self.code_text.insert(1.0, EXAMPLE_CODES[idx])
    
    def insert_template(self, template_type):
        """Insertar plantilla de código"""
        if template_type in CODE_TEMPLATES:
            self.code_text.insert(tk.INSERT, CODE_TEMPLATES[template_type])
    
    # Compilación y ejecución
    
    def compile_code(self):
        """Compilar el código (verificar sintaxis)"""
        self.clear_output()
        code = self.code_text.get(1.0, tk.END).strip()
        
        if not code:
            self.write_output("No hay código para compilar", 'error')
            self.compilation_successful = False
            return
        
        self.write_output("Compilando...\n", 'info')
        
        try:
            # Lexer
            self.write_output("-> Análisis léxico... ", 'info')
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            self.write_output("OK\n", 'success')
            
            # Parser
            self.write_output("-> Análisis sintáctico... ", 'info')
            parser = CulinaryParser(tokens)
            self.ast = parser.parse()
            self.write_output("OK\n", 'success')

            self.write_output("\nCompilación exitosa \n", 'success')
            self.write_output("   El código está listo para ejecutarse.\n")
            
            # Marcar compilación exitosa
            self.compilation_successful = True
            self.last_compiled_code = code
            
        except SyntaxError as e:
            self.write_output("ERROR\n\n", 'error')
            error_msg = str(e)
            # Resaltar el número de línea si existe
            if "Línea" in error_msg:

                self.write_output("   ERROR DE SINTAXIS                   \n", 'error')
                self.write_output(f"\n{error_msg}\n\n", 'error')
            else:
                self.write_output(f"Error de sintaxis:\n{error_msg}\n", 'error')
            self.ast = None
            self.compilation_successful = False
            
        except ValueError as e:
            self.write_output("ERROR\n\n", 'error')
            error_msg = str(e)
            if "Línea" in error_msg:
                self.write_output("   ERROR LÉXICO                        \n", 'error')
                self.write_output(f"\n{error_msg}\n\n", 'error')
            else:
                self.write_output(f"Error léxico:\n{error_msg}\n", 'error')
            self.ast = None
            self.compilation_successful = False
            
        except Exception as e:
            self.write_output("ERROR\n\n", 'error')
            self.write_output(f"Error inesperado:\n{str(e)}\n", 'error')
            self.ast = None
            self.compilation_successful = False
    
    def run_code(self):
        """Ejecutar el código"""
        self.clear_output()
        code = self.code_text.get(1.0, tk.END).strip()
        
        if not code:
            self.write_output("No hay código para ejecutar", 'error')
            return
        
        # Verificar si el código ha sido modificado desde la última compilación
        if code != self.last_compiled_code or not self.compilation_successful:
            self.write_output("El código no ha sido compilado o tiene errores.\n", 'error')
            self.write_output("Compilando primero...\n\n", 'info')
            self.write_output("─" * 50 + "\n\n")
            
            # Intentar compilar
            try:
                # Lexer
                self.write_output("-> Análisis léxico... ", 'info')
                lexer = Lexer(code)
                tokens = lexer.tokenize()
                self.write_output("OK\n", 'success')
                
                # Parser
                self.write_output("-> Análisis sintáctico... ", 'info')
                parser = CulinaryParser(tokens)
                self.ast = parser.parse()
                self.write_output("OK\n", 'success')
                
                self.write_output("\nCompilación exitosa \n", 'success')
                self.write_output("─" * 50 + "\n\n")
                
                self.compilation_successful = True
                self.last_compiled_code = code
                
            except SyntaxError as e:
                self.write_output("ERROR\n\n", 'error')
                error_msg = str(e)
                if "Línea" in error_msg:
                    self.write_output("   ERROR DE SINTAXIS                   \n", 'error')
                    self.write_output(f"\n{error_msg}\n\n", 'error')
                else:
                    self.write_output(f"Error de sintaxis:\n{error_msg}\n", 'error')
                
                self.write_output("\n" + "─" * 50 + "\n")
                self.write_output("✗ No se puede ejecutar: hay errores de compilación\n", 'error')
                self.ast = None
                self.compilation_successful = False
                return
                
            except ValueError as e:
                self.write_output("ERROR\n\n", 'error')
                error_msg = str(e)
                if "Línea" in error_msg:
                    self.write_output("   ERROR LÉXICO                        \n", 'error')
                    self.write_output(f"\n{error_msg}\n\n", 'error')
                else:
                    self.write_output(f"Error léxico:\n{error_msg}\n", 'error')
                
                self.write_output("\n" + "─" * 50 + "\n")
                self.write_output("✗ No se puede ejecutar: hay errores de compilación\n", 'error')
                self.ast = None
                self.compilation_successful = False
                return
                
            except Exception as e:
                self.write_output("ERROR\n\n", 'error')
                self.write_output(f"Error inesperado:\n{str(e)}\n", 'error')
                self.write_output("\n" + "─" * 50 + "\n")
                self.write_output("✗ No se puede ejecutar: hay errores de compilación\n", 'error')
                self.ast = None
                self.compilation_successful = False
                return

        self.write_output("Ejecutando...\n", 'info')
        self.write_output("─" * 50 + "\n\n")
        
        try:
            # Lexer
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            
            # Parser
            parser = CulinaryParser(tokens)
            ast = parser.parse()
            
            # Capturar stdout
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            # Interpreter con callback para input
            interpreter = CulinaryInterpreter(input_callback=self.console_input)
            interpreter.interpret(ast)
            
            # Obtener output
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            if output:
                self.write_output(output)
            else:
                self.write_output("(sin salida)\n", 'info')
            
            self.write_output("\n" + "─" * 50 + "\n")
            self.write_output("Ejecución completada exitosamente\n", 'success')
            
        except SyntaxError as e:
            sys.stdout = old_stdout
            error_msg = str(e)
            if "Línea" in error_msg:
                self.write_output("\n   ERROR DE SINTAXIS                   \n", 'error')
                self.write_output(f"\n{error_msg}\n\n", 'error')
            else:
                self.write_output(f"\nError de sintaxis:\n{error_msg}\n", 'error')

        except (TypeError, ValueError, NameError, RuntimeError) as e:
            sys.stdout = old_stdout
            error_msg = str(e)
            self.write_output("\n   ERROR EN TIEMPO DE EJECUCIÓN        \n", 'error')
            self.write_output(f"\n{error_msg}\n\n", 'error')

        except Exception as e:
            sys.stdout = old_stdout
            self.write_output(f"\nError inesperado:\n{str(e)}\n", 'error')
            import traceback
            self.write_output("\nDetalles técnicos:\n", 'info')
            self.write_output(traceback.format_exc(), 'error')
    
    def console_input(self, prompt):
        """Input estilo consola en el panel de output"""
        self.write_output(prompt, 'prompt')
        
        # Resetear variables
        self.input_result = None
        self.waiting_for_input = True
        
        # Configurar el input_entry
        self.input_label.config(text="Ingresa valor: ")
        self.input_entry.delete(0, tk.END)
        
        # Mostrar el frame de input
        self.input_frame.pack(fill=tk.X, pady=(5, 5))
        
        # Enfocar el entry
        self.input_entry.focus_set()
        
        # Bind para capturar Enter
        def on_enter(event):
            if self.waiting_for_input:
                self.input_result = self.input_entry.get()
                self.waiting_for_input = False
                
                
                self.write_output(self.input_result + "\n", 'input')
                
            
                self.input_frame.pack_forget()
                
                # Unbind el evento
                self.input_entry.unbind('<Return>')
        
        self.input_entry.bind('<Return>', on_enter)
        
        # Esperar a que el usuario ingrese algo
        self.root.wait_variable(self._create_wait_variable())
        
        return self.input_result if self.input_result is not None else ""
    
    def _create_wait_variable(self):
        """Crear una variable para wait_variable que se actualiza cuando se completa el input"""
        var = tk.StringVar()
        
        def check_input():
            if not self.waiting_for_input:
                var.set("done")
            else:
                self.root.after(100, check_input)
        
        check_input()
        return var
    
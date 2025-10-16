import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from lexer import Lexer
from parser import CulinaryParser
from interpreter import CulinaryInterpreter
import io
import sys

class FoodLanguageIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("FoodLanguage IDE - Lenguaje de Programación Culinario")
        self.root.geometry("1400x800")
        self.root.configure(bg='#2b2b2b')
        
        # Configurar estilo
        self.setup_style()
        
        # Variables
        self.current_code = ""
        self.ast = None
        
        # Crear interfaz
        self.create_menu()
        self.create_main_layout()
        
    def setup_style(self):
        """Configurar estilo visual de la aplicación"""
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
        
    def create_menu(self):
        """Crear menú superior"""
        menubar = tk.Menu(self.root, bg='#3c3c3c', fg='#e0e0e0')
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo", command=self.new_file)
        file_menu.add_command(label="Limpiar", command=self.clear_code)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Palabras Reservadas
        keywords_menu = tk.Menu(menubar, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        menubar.add_cascade(label="Palabras Reservadas", menu=keywords_menu)
        keywords_menu.add_command(label="Ver todas", command=self.show_keywords)
        keywords_menu.add_command(label="Tipos de datos", command=self.show_data_types)
        keywords_menu.add_command(label="Valores especiales", command=self.show_special_values)
        
        # Menú Sintaxis
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
        
        # Submenú Operaciones
        operations_menu = tk.Menu(syntax_menu, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        syntax_menu.add_cascade(label="Operaciones", menu=operations_menu)
        operations_menu.add_command(label="Aritméticas", command=self.show_arithmetic)
        operations_menu.add_command(label="Comparación", command=self.show_comparison)
        operations_menu.add_command(label="Lógicas", command=self.show_logical)
        
        # Menú Semántica
        semantic_menu = tk.Menu(menubar, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        menubar.add_cascade(label="Semántica", menu=semantic_menu)
        semantic_menu.add_command(label="Variables", command=self.show_semantics_variables)
        semantic_menu.add_command(label="Funciones", command=self.show_semantics_functions)
        semantic_menu.add_command(label="Alcance (Scope)", command=self.show_semantics_scope)
        
        # Menú Tipos de Datos
        types_menu = tk.Menu(menubar, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        menubar.add_cascade(label="Tipos de Datos", menu=types_menu)
        types_menu.add_command(label="quantity (entero)", command=lambda: self.insert_template('int'))
        types_menu.add_command(label="portion (flotante)", command=lambda: self.insert_template('float'))
        types_menu.add_command(label="ingredient (string)", command=lambda: self.insert_template('string'))
        types_menu.add_command(label="menu (lista)", command=lambda: self.insert_template('list'))
        types_menu.add_command(label="menu 2D (matriz)", command=lambda: self.insert_template('matrix'))
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0, bg='#3c3c3c', fg='#e0e0e0')
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Ejemplos", command=self.show_examples)
        help_menu.add_command(label="Acerca de", command=self.show_about)
        
    def create_main_layout(self):
        """Crear el layout principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo - Editor de código
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Título del editor
        editor_label = ttk.Label(left_panel, text="Editor de Código", 
                                font=('Consolas', 12, 'bold'))
        editor_label.pack(pady=(0, 5))
        
        # Área de texto para código
        self.code_text = scrolledtext.ScrolledText(
            left_panel,
            wrap=tk.WORD,
            width=60,
            height=30,
            font=('Consolas', 11),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='#ffffff',
            selectbackground='#264f78',
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.code_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame de botones
        button_frame = ttk.Frame(left_panel)
        button_frame.pack(pady=10)
        
        # Botón Compilar
        self.compile_btn = tk.Button(
            button_frame,
            text="🔍 Compilar",
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
        
        # Botón Ejecutar
        self.run_btn = tk.Button(
            button_frame,
            text="▶ Ejecutar",
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
        
        # Botón Limpiar
        clear_btn = tk.Button(
            button_frame,
            text="🗑 Limpiar",
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
        
        # Panel derecho - Output
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Título del output
        output_label = ttk.Label(right_panel, text="Salida / Errores", 
                                font=('Consolas', 12, 'bold'))
        output_label.pack(pady=(0, 5))
        
        # Área de output
        self.output_text = scrolledtext.ScrolledText(
            right_panel,
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
        
        # Configurar tags para colores
        self.output_text.tag_config('error', foreground='#f48771')
        self.output_text.tag_config('success', foreground='#4ec9b0')
        self.output_text.tag_config('info', foreground='#9cdcfe')
        
    # ==================== FUNCIONES DE MENÚ ====================
    
    def new_file(self):
        """Crear nuevo archivo"""
        if messagebox.askyesno("Nuevo archivo", "¿Limpiar el código actual?"):
            self.clear_code()
            
    def clear_code(self):
        """Limpiar el editor de código"""
        self.code_text.delete(1.0, tk.END)
        
    def clear_all(self):
        """Limpiar código y output"""
        self.clear_code()
        self.clear_output()
        
    def show_keywords(self):
        """Mostrar todas las palabras reservadas"""
        keywords_window = tk.Toplevel(self.root)
        keywords_window.title("Palabras Reservadas - FoodLanguage")
        keywords_window.geometry("700x600")
        keywords_window.configure(bg='#2b2b2b')
        
        text = scrolledtext.ScrolledText(keywords_window, wrap=tk.WORD, 
                                        font=('Consolas', 10),
                                        bg='#1e1e1e', fg='#d4d4d4', padx=20, pady=20)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        content = """
╔════════════════════════════════════════════════════════════╗
║         PALABRAS RESERVADAS - FOODLANGUAGE                 ║
╚════════════════════════════════════════════════════════════╝

📌 TIPOS DE DATOS:
   • quantity      → Entero (int)
   • portion       → Flotante (float)
   • ingredient    → Cadena (string)
   • menu          → Lista/Array

📌 ESTRUCTURAS DE CONTROL:
   • if / if_has   → Condicional if
   • otherwise     → else
   • cook_while    → Bucle while
   • stir          → Bucle for
   • season        → Switch/case
   • with          → Case en switch
   • default_flavor → Default en switch

📌 FUNCIONES:
   • recipe        → Definir función
   • serve         → Return
   • taste         → Print/Imprimir
   • add           → Input/Leer entrada

📌 VALORES ESPECIALES:
   • ready         → true
   • raw           → false
   • flavorless    → null

📌 CONTROL DE FLUJO:
   • stop_stirring  → break
   • keep_stirring  → continue

📌 OPERADORES LÓGICOS:
   • spoon         → AND (&&)
   • fork          → OR (||)
   • unseasoned    → NOT (!)

📌 OPERADORES ARITMÉTICOS:
   • ++            → Suma
   • --            → Resta
   • **            → Multiplicación
   • \\\\          → División

📌 OPERADORES DE COMPARACIÓN:
   • ===           → Igual a
   • !=            → Diferente de
   • >             → Mayor que
   • <             → Menor que
   • >=            → Mayor o igual
   • <=            → Menor o igual

📌 ASIGNACIÓN:
   • ==            → Asignación (=)
"""
        text.insert(1.0, content)
        text.config(state=tk.DISABLED)
        
    def show_data_types(self):
        """Mostrar información sobre tipos de datos"""
        info_window = tk.Toplevel(self.root)
        info_window.title("Tipos de Datos")
        info_window.geometry("600x500")
        info_window.configure(bg='#2b2b2b')
        
        text = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, 
                                        font=('Consolas', 10),
                                        bg='#1e1e1e', fg='#d4d4d4', padx=20, pady=20)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        content = """
╔════════════════════════════════════════════════════════════╗
║              TIPOS DE DATOS - FOODLANGUAGE                 ║
╚════════════════════════════════════════════════════════════╝

🔢 QUANTITY (Entero):
   Representa números enteros.
   
   Ejemplo:
   quantity edad == 25
   quantity contador == 0

📊 PORTION (Flotante):
   Representa números decimales.
   
   Ejemplo:
   portion precio == 19.99
   portion temperatura == 36.5

📝 INGREDIENT (String):
   Representa cadenas de texto.
   
   Ejemplo:
   ingredient nombre == "Juan"
   ingredient mensaje == "Hola Mundo"

📋 MENU (Lista):
   Representa arreglos/listas de elementos.
   
   Ejemplo:
   menu numeros == [1, 2, 3, 4, 5]
   menu nombres == ["Ana", "Luis", "María"]
   
   Acceso: numeros[0]  → primer elemento

🎯 MENU 2D (Matriz):
   Representa matrices (listas de listas).
   
   Ejemplo:
   menu matriz == [[1, 2], [3, 4]]
   
   Acceso: matriz[0][1]  → elemento en fila 0, columna 1
"""
        text.insert(1.0, content)
        text.config(state=tk.DISABLED)
        
    def show_special_values(self):
        """Mostrar valores especiales"""
        info_window = tk.Toplevel(self.root)
        info_window.title("Valores Especiales")
        info_window.geometry("500x300")
        info_window.configure(bg='#2b2b2b')
        
        text = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, 
                                        font=('Consolas', 10),
                                        bg='#1e1e1e', fg='#d4d4d4', padx=20, pady=20)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        content = """
╔════════════════════════════════════════════════════════════╗
║           VALORES ESPECIALES - FOODLANGUAGE                ║
╚════════════════════════════════════════════════════════════╝

✅ READY (true):
   Representa el valor booleano verdadero.
   
   Ejemplo:
   if_has (ready) {
       taste("Es verdadero")
   }

❌ RAW (false):
   Representa el valor booleano falso.
   
   Ejemplo:
   if_has (raw) {
       taste("Es falso")
   }

⭕ FLAVORLESS (null):
   Representa un valor nulo o sin sabor.
   
   Ejemplo:
   ingredient nombre == flavorless
"""
        text.insert(1.0, content)
        text.config(state=tk.DISABLED)
        
    def show_arithmetic(self):
        """Mostrar operaciones aritméticas"""
        info_window = tk.Toplevel(self.root)
        info_window.title("Operaciones Aritméticas")
        info_window.geometry("600x400")
        info_window.configure(bg='#2b2b2b')
        
        text = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, 
                                        font=('Consolas', 10),
                                        bg='#1e1e1e', fg='#d4d4d4', padx=20, pady=20)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        content = """
╔════════════════════════════════════════════════════════════╗
║         OPERACIONES ARITMÉTICAS - FOODLANGUAGE             ║
╚════════════════════════════════════════════════════════════╝

➕ SUMA (++):
   quantity resultado == 5 ++ 3    → 8

➖ RESTA (--):
   quantity resultado == 10 -- 4   → 6

✖️ MULTIPLICACIÓN (**):
   quantity resultado == 6 ** 7    → 42

➗ DIVISIÓN (\\\\):
   quantity resultado == 20 \\\\ 4   → 5

📌 INCREMENTO/DECREMENTO:
   • Prefijo:  ++x  o  --x
   • Postfijo: x++  o  x--
   
   Ejemplo:
   quantity i == 0
   i++              → i ahora es 1
   ++i              → i ahora es 2

💡 NOTA: Los operadores usan símbolos dobles para
   diferenciarlos del incremento/decremento.
"""
        text.insert(1.0, content)
        text.config(state=tk.DISABLED)
        
    def show_comparison(self):
        """Mostrar operadores de comparación"""
        info_window = tk.Toplevel(self.root)
        info_window.title("Operadores de Comparación")
        info_window.geometry("600x450")
        info_window.configure(bg='#2b2b2b')
        
        text = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, 
                                        font=('Consolas', 10),
                                        bg='#1e1e1e', fg='#d4d4d4', padx=20, pady=20)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        content = """
╔════════════════════════════════════════════════════════════╗
║        OPERADORES DE COMPARACIÓN - FOODLANGUAGE            ║
╚════════════════════════════════════════════════════════════╝

🟰 IGUAL A (===):
   if_has (x === 5) {
       taste("x es igual a 5")
   }

≠ DIFERENTE DE (!=):
   if_has (x != 0) {
       taste("x no es cero")
   }

> MAYOR QUE (>):
   if_has (edad > 18) {
       taste("Mayor de edad")
   }

< MENOR QUE (<):
   if_has (temperatura < 0) {
       taste("Bajo cero")
   }

≥ MAYOR O IGUAL (>=):
   if_has (nota >= 70) {
       taste("Aprobado")
   }

≤ MENOR O IGUAL (<=):
   if_has (stock <= 10) {
       taste("Stock bajo")
   }

💡 NOTA: Use === para igualdad (tres signos igual)
   y == para asignación (dos signos igual).
"""
        text.insert(1.0, content)
        text.config(state=tk.DISABLED)
        
    def show_logical(self):
        """Mostrar operadores lógicos"""
        info_window = tk.Toplevel(self.root)
        info_window.title("Operadores Lógicos")
        info_window.geometry("600x400")
        info_window.configure(bg='#2b2b2b')
        
        text = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, 
                                        font=('Consolas', 10),
                                        bg='#1e1e1e', fg='#d4d4d4', padx=20, pady=20)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        content = """
╔════════════════════════════════════════════════════════════╗
║          OPERADORES LÓGICOS - FOODLANGUAGE                 ║
╚════════════════════════════════════════════════════════════════╝

🥄 SPOON (AND - &&):
   Ambas condiciones deben ser verdaderas.
   
   Ejemplo:
   if_has (edad >= 18 spoon tieneLicencia === ready) {
       taste("Puede conducir")
   }

🍴 FORK (OR - ||):
   Al menos una condición debe ser verdadera.
   
   Ejemplo:
   if_has (esFinde === ready fork esVacacion === ready) {
       taste("Puede descansar")
   }

� UNSEASONED (NOT - !):
   Invierte el valor de verdad de una condición.
   
   Ejemplo:
   if_has (unseasoned estaLloviendo) {
       taste("Hace buen tiempo")
   }
   
   if_has (edad >= 18 spoon unseasoned tieneLicencia) {
       taste("Mayor de edad pero sin licencia")
   }

�📊 TABLA DE VERDAD SPOON (AND):
   ready spoon ready   → ready
   ready spoon raw     → raw
   raw spoon ready     → raw
   raw spoon raw       → raw

📊 TABLA DE VERDAD FORK (OR):
   ready fork ready    → ready
   ready fork raw      → ready
   raw fork ready      → ready
   raw fork raw        → raw

� TABLA DE VERDAD UNSEASONED (NOT):
   unseasoned ready    → raw
   unseasoned raw      → ready

�💡 TIP: Use paréntesis para operaciones complejas:
   if_has ((a > 5 spoon b < 10) fork unseasoned c) { }
   if_has (unseasoned (x < 0 fork x > 100)) { }
"""
        text.insert(1.0, content)
        text.config(state=tk.DISABLED)
        
    def show_semantics_variables(self):
        """Mostrar semántica de variables"""
        info_window = tk.Toplevel(self.root)
        info_window.title("Semántica - Variables")
        info_window.geometry("700x500")
        info_window.configure(bg='#2b2b2b')
        
        text = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, 
                                        font=('Consolas', 10),
                                        bg='#1e1e1e', fg='#d4d4d4', padx=20, pady=20)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        content = """
╔════════════════════════════════════════════════════════════╗
║            SEMÁNTICA - VARIABLES                           ║
╚════════════════════════════════════════════════════════════╝

📝 DECLARACIÓN:
   Las variables deben declararse con un tipo antes de usarse.
   
   Sintaxis:
   <tipo> <nombre> == <valor>
   
   Ejemplos:
   quantity edad == 25
   ingredient nombre == "María"
   menu numeros == [1, 2, 3]

🔄 ASIGNACIÓN:
   Una vez declarada, puede asignarse un nuevo valor.
   
   edad == 26
   nombre == "Pedro"

⚠️ REGLAS IMPORTANTES:
   1. El nombre debe ser único en su scope
   2. Los nombres distinguen mayúsculas/minúsculas
   3. No pueden empezar con números
   4. Pueden contener letras, números y guiones bajos

✅ NOMBRES VÁLIDOS:
   • miVariable
   • contador_1
   • temperatura_max
   • _privado

❌ NOMBRES INVÁLIDOS:
   • 1variable    (empieza con número)
   • mi-variable  (contiene guión)
   • for          (palabra reservada)

💡 CONVENCIÓN:
   Use camelCase: miVariable, contadorTotal
   O snake_case: mi_variable, contador_total
"""
        text.insert(1.0, content)
        text.config(state=tk.DISABLED)
        
    def show_semantics_functions(self):
        """Mostrar semántica de funciones"""
        info_window = tk.Toplevel(self.root)
        info_window.title("Semántica - Funciones")
        info_window.geometry("700x550")
        info_window.configure(bg='#2b2b2b')
        
        text = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, 
                                        font=('Consolas', 10),
                                        bg='#1e1e1e', fg='#d4d4d4', padx=20, pady=20)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        content = """
╔════════════════════════════════════════════════════════════╗
║            SEMÁNTICA - FUNCIONES (RECIPES)                 ║
╚════════════════════════════════════════════════════════════╝

🍳 DEFINICIÓN:
   Las funciones se definen con la palabra 'recipe'.
   
   Sintaxis:
   recipe nombreFuncion(tipo param1, tipo param2) {
       // cuerpo de la función
       serve valor_retorno
   }

📥 PARÁMETROS:
   Los parámetros deben tener tipo explícito.
   
   Ejemplo:
   recipe sumar(quantity a, quantity b) {
       quantity resultado == a ++ b
       serve resultado
   }

📤 RETORNO:
   Use 'serve' para retornar valores.
   
   • serve valor      → retorna un valor
   • serve flavorless → retorna null
   • Solo serve       → retorna sin valor

📞 LLAMADA:
   nombreFuncion(arg1, arg2)
   
   Ejemplo:
   quantity total == sumar(5, 3)

⚠️ REGLAS:
   1. El número de argumentos debe coincidir con parámetros
   2. Los tipos deben ser compatibles
   3. Las funciones se declaran antes de usarse
   4. Los parámetros son pasados por valor

💡 EJEMPLO COMPLETO:
   recipe calcularArea(quantity base, quantity altura) {
       quantity area == base ** altura \\\\ 2
       serve area
   }
   
   quantity triangulo == calcularArea(10, 5)
   taste("Área:", triangulo)
"""
        text.insert(1.0, content)
        text.config(state=tk.DISABLED)
        
    def show_semantics_scope(self):
        """Mostrar semántica de alcance"""
        info_window = tk.Toplevel(self.root)
        info_window.title("Semántica - Alcance (Scope)")
        info_window.geometry("700x550")
        info_window.configure(bg='#2b2b2b')
        
        text = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, 
                                        font=('Consolas', 10),
                                        bg='#1e1e1e', fg='#d4d4d4', padx=20, pady=20)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        content = """
╔════════════════════════════════════════════════════════════╗
║            SEMÁNTICA - ALCANCE (SCOPE)                     ║
╚════════════════════════════════════════════════════════════╝

🌍 ALCANCE GLOBAL:
   Variables declaradas fuera de funciones.
   Visibles en todo el programa.
   
   quantity global == 100
   
   recipe mostrar() {
       taste(global)  // Puede acceder a 'global'
   }

🏠 ALCANCE LOCAL:
   Variables declaradas dentro de funciones.
   Solo visibles dentro de esa función.
   
   recipe ejemplo() {
       quantity local == 50  // Solo existe aquí
       taste(local)
   }
   
   taste(local)  // ❌ ERROR: 'local' no existe aquí

🔍 BÚSQUEDA DE VARIABLES:
   El intérprete busca en este orden:
   1. Scope local (de la función actual)
   2. Scope global
   
   Si no encuentra la variable, genera error.

⚠️ SHADOWING (SOMBREADO):
   Una variable local puede tener el mismo nombre
   que una global, "ocultando" la global.
   
   quantity x == 10  // Global
   
   recipe test() {
       quantity x == 5  // Local, oculta la global
       taste(x)  // Imprime 5, no 10
   }
   
   test()
   taste(x)  // Imprime 10 (la global)

💡 EJEMPLO COMPLETO:
   quantity contador == 0  // Global
   
   recipe incrementar() {
       contador == contador ++ 1  // Modifica global
       taste("Contador:", contador)
   }
   
   incrementar()  // contador = 1
   incrementar()  // contador = 2
   taste(contador)  // Imprime 2

🎯 PARÁMETROS:
   Los parámetros son variables locales.
   
   recipe sumar(quantity a, quantity b) {
       // 'a' y 'b' solo existen aquí
       serve a ++ b
   }
"""
        text.insert(1.0, content)
        text.config(state=tk.DISABLED)
        
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
        
        examples = [
            "1. Hola Mundo",
            "2. Variables y Tipos",
            "3. Operaciones Aritméticas",
            "4. Condicional If-Else",
            "5. Bucle While",
            "6. Bucle For",
            "7. Listas (Menu)",
            "8. Matrices",
            "9. Función Simple",
            "10. Función con Retorno",
            "11. Factorial Recursivo",
            "12. Switch (Season)",
            "13. Entrada de Usuario",
            "14. Programa Completo"
        ]
        
        for ex in examples:
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
        examples_code = [
            # 0. Hola Mundo
            '''taste("¡Hola Mundo desde FoodLanguage!")''',
            
            # 1. Variables y Tipos
            '''quantity edad == 25
portion precio == 19.99
ingredient nombre == "Chef Carlos"
menu ingredientes == ["sal", "pimienta", "ajo"]

taste("Edad:", edad)
taste("Precio:", precio)
taste("Nombre:", nombre)
taste("Ingredientes:", ingredientes)''',
            
            # 2. Operaciones Aritméticas
            '''quantity a == 10
quantity b == 3

quantity suma == a ++ b
quantity resta == a -- b
quantity multiplicacion == a ** b
quantity division == a \\\\ b

taste("Suma:", suma)
taste("Resta:", resta)
taste("Multiplicación:", multiplicacion)
taste("División:", division)''',
            
            # 3. Condicional If-Else
            '''quantity edad == 20

if_has (edad >= 18) {
    taste("Eres mayor de edad")
    taste("Puedes votar")
} otherwise {
    taste("Eres menor de edad")
    quantity anios == 18 -- edad
    taste("Te faltan", anios, "años")
}''',
            
            # 4. Bucle While
            '''quantity contador == 1

taste("Contando del 1 al 5:")
cook_while (contador <= 5) {
    taste("  Número:", contador)
    contador == contador ++ 1
}
taste("¡Terminado!")''',
            
            # 5. Bucle For
            '''taste("Tabla del 7:")
stir (quantity i == 1, i <= 10, i == i ++ 1) {
    quantity resultado == 7 ** i
    taste("  7 x", i, "=", resultado)
}''',
            
            # 6. Listas (Menu)
            '''menu frutas == ["manzana", "banana", "naranja"]
taste("Frutas:", frutas)
taste("Primera fruta:", frutas[0])

frutas[1] == "fresa"
taste("Segunda fruta modificada:", frutas[1])

menu numeros == [10, 20, 30, 40]
quantity suma == numeros[0] ++ numeros[3]
taste("Suma:", suma)''',
            
            # 7. Matrices
            '''menu matriz == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

taste("Matriz completa:", matriz)
taste("Elemento [0][0]:", matriz[0][0])
taste("Elemento [1][2]:", matriz[1][2])

matriz[1][1] == 100
taste("Centro modificado:", matriz[1][1])''',
            
            # 8. Función Simple
            '''recipe saludar(ingredient nombre) {
    taste("¡Hola", nombre, "!")
    taste("Bienvenido a FoodLanguage")
    serve flavorless
}

saludar("Chef")
saludar("María")''',
            
            # 9. Función con Retorno
            '''recipe sumar(quantity a, quantity b) {
    quantity resultado == a ++ b
    serve resultado
}

recipe multiplicar(quantity x, quantity y) {
    serve x ** y
}

quantity total == sumar(15, 25)
taste("15 + 25 =", total)

quantity producto == multiplicar(6, 7)
taste("6 × 7 =", producto)''',
            
            # 10. Factorial Recursivo
            '''recipe factorial(quantity n) {
    if_has (n <= 1) {
        serve 1
    }
    quantity resultado == n ** factorial(n -- 1)
    serve resultado
}

taste("Factorial de 5:", factorial(5))
taste("Factorial de 7:", factorial(7))''',
            
            # 11. Switch (Season)
            '''quantity dia == 3

season (dia) {
    with 1:
        taste("Lunes - Preparación")
    with 2:
        taste("Martes - Cocción")
    with 3:
        taste("Miércoles - Horneado")
        taste("Día especial!")
    with 4:
        taste("Jueves - Fritura")
    with 5:
        taste("Viernes - Parrilla")
    default_flavor:
        taste("Fin de semana - Descanso")
}''',
            
            # 12. Entrada de Usuario
            '''ingredient nombre
add("Ingrese su nombre:", nombre)
taste("¡Hola", nombre, "!")

quantity edad
add("Ingrese su edad:", edad)

if_has (edad >= 18) {
    taste("Eres mayor de edad,", nombre)
} otherwise {
    taste("Eres menor de edad,", nombre)
}''',
            
            # 13. Programa Completo
            '''recipe calcularPromedio(menu notas) {
    quantity suma == 0
    quantity i == 0
    
    cook_while (i < 3) {
        suma == suma ++ notas[i]
        i++
    }
    
    portion promedio == suma \\\\ 3
    serve promedio
}

recipe evaluarPromedio(portion prom) {
    if_has (prom >= 70) {
        taste("¡APROBADO! 🎉")
        serve ready
    } otherwise {
        taste("Reprobado 😢")
        serve raw
    }
}

taste("=== SISTEMA DE CALIFICACIONES ===")
menu calificaciones == [85, 90, 78]

taste("Calificaciones:", calificaciones)

portion promedio == calcularPromedio(calificaciones)
taste("Promedio:", promedio)

evaluarPromedio(promedio)'''
        ]
        
        if 0 <= idx < len(examples_code):
            self.code_text.delete(1.0, tk.END)
            self.code_text.insert(1.0, examples_code[idx])
    
    def show_about(self):
        """Mostrar información sobre el IDE"""
        about_text = """
FoodLanguage IDE v1.0

Lenguaje de Programación Culinario

Desarrollado como proyecto académico
para demostrar conceptos de compiladores
e intérpretes.

Características:
• Sintaxis basada en términos culinarios
• Compilación y ejecución en tiempo real
• Detección de errores sintácticos
• Soporte para funciones, ciclos y estructuras de datos

© 2024 - Todos los derechos reservados
        """
        messagebox.showinfo("Acerca de FoodLanguage", about_text)
    
    # ==================== PLANTILLAS DE CÓDIGO ====================
    
    def insert_template(self, template_type):
        """Insertar plantilla de código"""
        templates = {
            'if': '''if_has (condicion) {
    // código si verdadero
} otherwise {
    // código si falso
}''',
            'while': '''cook_while (condicion) {
    // código del bucle
}''',
            'for': '''stir (quantity i == 0, i < 10, i == i ++ 1) {
    // código del bucle
}''',
            'switch': '''season (variable) {
    with valor1:
        // código caso 1
    with valor2:
        // código caso 2
    default_flavor:
        // código por defecto
}''',
            'function': '''recipe nombreFuncion(quantity param1, ingredient param2) {
    // cuerpo de la función
    serve resultado
}''',
            'call': '''nombreFuncion(arg1, arg2)''',
            'int': '''quantity variable == 0''',
            'float': '''portion variable == 0.0''',
            'string': '''ingredient variable == "texto"''',
            'list': '''menu lista == [1, 2, 3, 4, 5]''',
            'matrix': '''menu matriz == [[1, 2], [3, 4]]'''
        }
        
        if template_type in templates:
            # Insertar en la posición del cursor
            self.code_text.insert(tk.INSERT, templates[template_type])
    
    # ==================== FUNCIONES DE COMPILACIÓN Y EJECUCIÓN ====================
    
    def compile_code(self):
        """Compilar el código (verificar sintaxis)"""
        self.clear_output()
        code = self.code_text.get(1.0, tk.END).strip()
        
        if not code:
            self.write_output("⚠️  No hay código para compilar", 'error')
            return
        
        self.write_output("🔍 Compilando...\n", 'info')
        
        try:
            # Lexer
            self.write_output("→ Análisis léxico... ", 'info')
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            self.write_output("✓ OK\n", 'success')
            
            # Parser
            self.write_output("→ Análisis sintáctico... ", 'info')
            parser = CulinaryParser(tokens)
            self.ast = parser.parse()
            self.write_output("✓ OK\n", 'success')
            
            self.write_output("\n✅ Compilación exitosa\n", 'success')
            self.write_output("   El código está listo para ejecutarse.\n")
            
        except SyntaxError as e:
            self.write_output("✗ ERROR\n\n", 'error')
            self.write_output(f"❌ Error de sintaxis:\n{str(e)}\n", 'error')
            self.ast = None
            
        except Exception as e:
            self.write_output("✗ ERROR\n\n", 'error')
            self.write_output(f"❌ Error inesperado:\n{str(e)}\n", 'error')
            self.ast = None
    
    def run_code(self):
        """Ejecutar el código"""
        self.clear_output()
        code = self.code_text.get(1.0, tk.END).strip()
        
        if not code:
            self.write_output("⚠️  No hay código para ejecutar", 'error')
            return
        
        self.write_output("▶️  Ejecutando...\n", 'info')
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
            
            # Interpreter
            interpreter = CulinaryInterpreter()
            interpreter.interpret(ast)
            
            # Obtener output
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            if output:
                self.write_output(output)
            else:
                self.write_output("(sin salida)\n", 'info')
            
            self.write_output("\n" + "─" * 50 + "\n")
            self.write_output("✅ Ejecución completada exitosamente\n", 'success')
            
        except SyntaxError as e:
            sys.stdout = old_stdout
            self.write_output(f"\n❌ Error de sintaxis:\n{str(e)}\n", 'error')
            
        except Exception as e:
            sys.stdout = old_stdout
            self.write_output(f"\n❌ Error en tiempo de ejecución:\n{str(e)}\n", 'error')
            import traceback
            self.write_output("\nDetalles técnicos:\n", 'info')
            self.write_output(traceback.format_exc(), 'error')
    
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


# ==================== FUNCIÓN PRINCIPAL ====================

def main():
    root = tk.Tk()
    app = FoodLanguageIDE(root)
    root.mainloop()


if __name__ == '__main__':
    main()
import tkinter as tk
from tkinter import scrolledtext

# INFORMACIÓN GENERAL

def create_info_window(parent, title, content, width=700, height=600):
    """Crear una ventana de información genérica"""
    info_window = tk.Toplevel(parent)
    info_window.title(title)
    info_window.geometry(f"{width}x{height}")
    info_window.configure(bg='#2b2b2b')
    
    text = scrolledtext.ScrolledText(
        info_window, 
        wrap=tk.WORD, 
        font=('Consolas', 10),
        bg='#1e1e1e', 
        fg='#d4d4d4', 
        padx=20, 
        pady=20
    )
    text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    text.insert(1.0, content)
    text.config(state=tk.DISABLED)
    
    return info_window

#  CONTENIDOS INFORMATIVOS 

KEYWORDS_CONTENT = """

         PALABRAS RESERVADAS - FOODLANGUAGE                 


 TIPOS DE DATOS:
   * quantity      -> Entero (int)
   * portion       -> Flotante (float)
   * ingredient    -> Cadena (string)
   * menu          -> Lista/Array

 ESTRUCTURAS DE CONTROL:
   * if / if_has   -> Condicional if
   * otherwise     -> else
   * cook_while    -> Bucle while
   * stir          -> Bucle for
   * season        -> Switch/case
   * with          -> Case en switch
   * default_flavor -> Default en switch

 FUNCIONES:
   * recipe        -> Definir función
   * serve         -> Return
   * taste         -> Print/Imprimir
   * add           -> Input/Leer entrada del usuario

 VALORES ESPECIALES:
   * ready         -> true
   * raw           -> false
   * flavorless    -> null

 CONTROL DE FLUJO:
   * stop_stirring  -> break
   * keep_stirring  -> continue

 OPERADORES LÓGICOS:
   * spoon         -> AND (&&)
   * fork          -> OR (||)
   * unseasoned    -> NOT (!)

 OPERADORES ARITMÉTICOS:
   * ++            -> Suma
   * --            -> Resta
   * **            -> Multiplicación
   * \\\\          -> División

 OPERADORES DE COMPARACIÓN:
   * ===           -> Igual a
   * !=            -> Diferente de
   * >             -> Mayor que
   * <             -> Menor que
   * >=            -> Mayor o igual
   * <=            -> Menor o igual

 ASIGNACIÓN:
   * ==            -> Asignación (=)

 COMENTARIOS:
   * //            -> Comentario de una línea
"""

DATA_TYPES_CONTENT = """

              TIPOS DE DATOS - FOODLANGUAGE

 QUANTITY (Entero):
   Representa números enteros.
   
   Ejemplo:
   quantity edad == 25
   quantity contador == 0

 PORTION (Flotante):
   Representa números decimales.
   
   Ejemplo:
   portion precio == 19.99
   portion temperatura == 36.5

 INGREDIENT (String):
   Representa cadenas de texto.
   
   Ejemplo:
   ingredient nombre == "Juan"
   ingredient mensaje == "Hola Mundo"

 MENU (Lista):
   Representa arreglos/listas de elementos.
   
   Ejemplo:
   menu numeros == [1, 2, 3, 4, 5]
   menu nombres == ["Ana", "Luis", "María"]
   
   Acceso: numeros[0]  -> primer elemento

 MENU 2D (Matriz):
   Representa matrices (listas de listas).
   
   Ejemplo:
   menu matriz == [[1, 2], [3, 4]]
   
   Acceso: matriz[0][1]  -> elemento en fila 0, columna 1
"""

SPECIAL_VALUES_CONTENT = """
           VALORES ESPECIALES - FOODLANGUAGE


 READY (true):
   Representa el valor booleano verdadero.
   
   Ejemplo:
   if_has (ready) {
       taste("Es verdadero")
   }

 RAW (false):
   Representa el valor booleano falso.
   
   Ejemplo:
   if_has (raw) {
       taste("Es falso")
   }

 FLAVORLESS (null):
   Representa un valor nulo o sin sabor.
   
   Ejemplo:
   ingredient nombre == flavorless
"""

ARITHMETIC_CONTENT = """

         OPERACIONES ARITMÉTICAS - FOODLANGUAGE

 SUMA (++):
   quantity resultado == 5 ++ 3    -> 8

 RESTA (--):
   quantity resultado == 10 -- 4   -> 6

 MULTIPLICACIÓN (**):
   quantity resultado == 6 ** 7    -> 42

 DIVISIÓN (\\\\):
   quantity resultado == 20 \\\\ 4   -> 5

  INCREMENTO/DECREMENTO:
    • Postfijo: x++  o  x--
    • Explícito: x == x ++ 1  o  x == x -- 1
    
    Ejemplo:
    quantity i == 0
    i++              -> i ahora es 1
    i == i ++ 2      -> i ahora es 3

  NOTA: Los operadores usan símbolos dobles para
    diferenciarlos del incremento/decremento.
"""

COMPARISON_CONTENT = """

        OPERADORES DE COMPARACIÓN - FOODLANGUAGE            


= IGUAL A (===):
   if_has (x === 5) {
       taste("x es igual a 5")
   }

!= DIFERENTE DE (!=):
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

>= MAYOR O IGUAL (>=):
   if_has (nota >= 70) {
       taste("Aprobado")
   }

<= MENOR O IGUAL (<=):
   if_has (stock <= 10) {
       taste("Stock bajo")
   }

 NOTA: Use === para igualdad (tres signos igual)
   y == para asignación (dos signos igual).
"""

LOGICAL_CONTENT = """

          OPERADORES LÓGICOS - FOODLANGUAGE

 SPOON (AND - &&):
   Ambas condiciones deben ser verdaderas.
   
   Ejemplo:
   if_has (edad >= 18 spoon tieneLicencia === ready) {
       taste("Puede conducir")
   }

 FORK (OR - ||):
   Al menos una condición debe ser verdadera.
   
   Ejemplo:
   if_has (esFinde === ready fork esVacacion === ready) {
       taste("Puede descansar")
   }

 UNSEASONED (NOT - !):
   Invierte el valor de verdad de una condición.
   
   Ejemplo:
   if_has (unseasoned estaLloviendo) {
       taste("Hace buen tiempo")
   }
   
   if_has (edad >= 18 spoon unseasoned tieneLicencia) {
       taste("Mayor de edad pero sin licencia")
   }

 TABLA DE VERDAD SPOON (AND):
   ready spoon ready   -> ready
   ready spoon raw     -> raw
   raw spoon ready     -> raw
   raw spoon raw       -> raw

 TABLA DE VERDAD FORK (OR):
   ready fork ready    -> ready
   ready fork raw      -> ready
   raw fork ready      -> ready
   raw fork raw        -> raw

 TABLA DE VERDAD UNSEASONED (NOT):
   unseasoned ready    -> raw
   unseasoned raw      -> ready

 TIP: Use paréntesis para operaciones complejas:
   if_has ((a > 5 spoon b < 10) fork unseasoned c) { }
   if_has (unseasoned (x < 0 fork x > 100)) { }
"""

SEMANTICS_VARIABLES_CONTENT = """

            SEMÁNTICA - VARIABLES                           


 DECLARACIÓN:
   Las variables deben declararse con un tipo antes de usarse.
   
   Sintaxis:
   <tipo> <nombre> == <valor>
   
   Ejemplos:
   quantity edad == 25
   ingredient nombre == "María"
   menu numeros == [1, 2, 3]

 ASIGNACIÓN:
   Una vez declarada, puede asignarse un nuevo valor.
   
   edad == 26
   nombre == "Pedro"

 REGLAS IMPORTANTES:
   1. El nombre debe ser único en su scope
   2. Los nombres distinguen mayúsculas/minúsculas
   3. No pueden empezar con números
   4. Pueden contener letras, números y guiones bajos

 NOMBRES VÁLIDOS:
   • miVariable
   • contador_1
   • temperatura_max
   • _privado

 NOMBRES INVÁLIDOS:
   • 1variable    (empieza con número)
   • mi-variable  (contiene guión)
   • for          (palabra reservada)

 CONVENCIÓN:
   Use camelCase: miVariable, contadorTotal
   O snake_case: mi_variable, contador_total
"""

SEMANTICS_FUNCTIONS_CONTENT = """

            SEMÁNTICA - FUNCIONES (RECIPES)                 


 DEFINICIÓN:
   Las funciones se definen con la palabra 'recipe'.
   
   Sintaxis:
   recipe nombreFuncion(tipo param1, tipo param2) {
       // cuerpo de la función
       serve valor_retorno
   }

 PARÁMETROS:
   Los parámetros deben tener tipo explícito.
   
   Ejemplo:
   recipe sumar(quantity a, quantity b) {
       quantity resultado == a ++ b
       serve resultado
   }

 RETORNO:
   Use 'serve' para retornar valores.
   
   • serve valor      -> retorna un valor
   • serve flavorless -> retorna null
   • Solo serve       -> retorna sin valor

 LLAMADA:
   nombreFuncion(arg1, arg2)
   
   Ejemplo:
   quantity total == sumar(5, 3)

 REGLAS:
   1. El número de argumentos debe coincidir con parámetros
   2. Los tipos deben ser compatibles
   3. Las funciones se declaran antes de usarse
   4. Los parámetros son pasados por valor

 EJEMPLO COMPLETO:
   recipe calcularArea(quantity base, quantity altura) {
       quantity area == base ** altura \\\\ 2
       serve area
   }
   
   quantity triangulo == calcularArea(10, 5)
   taste("Área:", triangulo)
"""

SEMANTICS_SCOPE_CONTENT = """

            SEMÁNTICA - ALCANCE (SCOPE)                    

 ALCANCE GLOBAL:
   Variables declaradas fuera de funciones.
   Visibles en todo el programa.
   
   quantity global == 100
   
   recipe mostrar() {
       taste(global)  // Puede acceder a 'global'
   }

 ALCANCE LOCAL:
   Variables declaradas dentro de funciones.
   Solo visibles dentro de esa función.
   
   recipe ejemplo() {
       quantity local == 50  // Solo existe aquí
       taste(local)
   }
   
   taste(local)  //  ERROR: 'local' no existe aquí

 BÚSQUEDA DE VARIABLES:
   El intérprete busca en este orden:
   1. Scope local (de la función actual)
   2. Scope global
   
   Si no encuentra la variable, genera error.

 SHADOWING (SOMBREADO):
   Una variable local puede tener el mismo nombre
   que una global, "ocultando" la global.
   
   quantity x == 10  // Global
   
   recipe test() {
       quantity x == 5  // Local, oculta la global
       taste(x)  // Imprime 5, no 10
   }
   
   test()
   taste(x)  // Imprime 10 (la global)

 EJEMPLO COMPLETO:
   quantity contador == 0  // Global
   
   recipe incrementar() {
       contador == contador ++ 1  // Modifica global
       taste("Contador:", contador)
   }
   
   incrementar()  // contador = 1
   incrementar()  // contador = 2
   taste(contador)  // Imprime 2

 PARÁMETROS:
   Los parámetros son variables locales.
   
   recipe sumar(quantity a, quantity b) {
       // 'a' y 'b' solo existen aquí
       serve a ++ b
   }
"""

ABOUT_TEXT = """
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

"""

# FoodLanguage

**FoodLanguage** es un lenguaje de programación educativo con sintaxis basada en términos
culinarios, acompañado de un IDE de escritorio construido con Tkinter. El proyecto implementa
la cadena completa de un lenguaje interpretado: analizador léxico (lexer), analizador sintáctico
(parser → AST) e intérprete, más un entorno gráfico para escribir, compilar y ejecutar programas.

Fue desarrollado como proyecto académico para demostrar conceptos de compiladores e intérpretes.

---

## Características

- **Sintaxis culinaria**: las palabras reservadas son términos de cocina (`recipe`, `taste`, `cook_while`…).
- **IDE integrado**: editor con números de línea, compilación y ejecución en tiempo real.
- **Reporte de errores** léxicos, sintácticos y de tipos con número de línea.
- **Entrada/Salida en la GUI**: `add` para leer datos del usuario y `taste` para imprimir.
- **Plantillas de código** y **17 ejemplos** listos para cargar desde el menú de Ayuda.
- **Documentación en el menú**: palabras reservadas, tipos de datos, operadores y semántica.
- **Tipado**: declaración de tipos con validación (`quantity`, `portion`, `ingredient`, `menu`),
  además de listas y matrices, funciones con recursión y estructuras de control.
- **Sin dependencias externas**: solo la biblioteca estándar de Python.

---

## Requisitos

- Python **3.10+** (probado con 3.12)
- Tkinter (incluido en la mayoría de instalaciones de Python; en Linux puede requerir
  `sudo apt install python3-tk`)

---

## Uso

```bash
git clone https://github.com/Bjmf05/FoodLanguage.git
cd FoodLanguage
python main.py
```

Se abre el **FoodLanguage IDE**. Escribe código en el panel izquierdo, pulsa **Compilar**
para verificar la sintaxis y **Ejecutar** para correr el programa. La salida y los errores
aparecen en el panel derecho.

---

## La sintaxis en un vistazo

```
recipe factorial(quantity n) {
    if_has (n <= 1) {
        serve 1
    }
    quantity resultado == n ** factorial(n -- 1)
    serve resultado
}

taste("Factorial de 5:", factorial(5))
```

### Tipos de datos

| FoodLanguage | Equivalente    | Ejemplo                       |
| ------------ | -------------- | ----------------------------- |
| `quantity`   | entero         | `quantity edad == 25`         |
| `portion`    | flotante       | `portion precio == 19.99`     |
| `ingredient` | cadena         | `ingredient nombre == "Chef"` |
| `menu`       | lista / matriz | `menu nums == [1, 2, 3]`      |

### Valores especiales

| FoodLanguage | Significado |
| ------------ | ----------- |
| `ready`      | `true`      |
| `raw`        | `false`     |
| `flavorless` | `null`      |

### Operadores

| FoodLanguage                 | Operación      |
| ---------------------------- | -------------- |
| `++`                         | suma           |
| `--`                         | resta          |
| `**`                         | multiplicación |
| `\\` (dos barras invertidas) | división       |
| `==`                         | asignación     |
| `===`                        | igualdad       |
| `!=`                         | distinto       |
| `>` `<` `>=` `<=`            | comparación    |
| `spoon`                      | AND lógico     |
| `fork`                       | OR lógico      |
| `unseasoned`                 | NOT lógico     |

### Palabras reservadas principales

| FoodLanguage                         | Concepto                |
| ------------------------------------ | ----------------------- |
| `recipe`                             | definición de función   |
| `serve`                              | retorno (`return`)      |
| `taste`                              | imprimir (`print`)      |
| `add`                                | leer entrada (`input`)  |
| `if_has` / `otherwise`               | condicional             |
| `cook_while`                         | bucle `while`           |
| `stir`                               | bucle `for`             |
| `season` / `with` / `default_flavor` | `switch`                |
| `stop_stirring` / `keep_stirring`    | `break` / `continue`    |
| `//`                                 | comentario de una línea |

---

## Estructura del proyecto

| Archivo             | Responsabilidad                                               |
| ------------------- | ------------------------------------------------------------- |
| `main.py`           | Punto de entrada; lanza el IDE.                               |
| `tokens.py`         | Definición de tokens y patrones (expresiones regulares).      |
| `lexer.py`          | `Lexer`: convierte el código fuente en una lista de tokens.   |
| `parser.py`         | `CulinaryParser`: construye el AST a partir de los tokens.    |
| `interpreter.py`    | `CulinaryInterpreter`: recorre el AST y ejecuta el programa.  |
| `ide_window.py`     | `FoodLanguageIDE`: ventana principal, menús y lógica del IDE. |
| `ui_components.py`  | Ventanas de ayuda y textos de referencia del lenguaje.        |
| `code_templates.py` | Plantillas de sintaxis y ejemplos precargados.                |

---

## Licencia

Distribuido bajo la licencia **MIT**. Ver [LICENSE](LICENSE).

Copyright (c) 2025 Breiner Muñoz Fallas

"""
code_templates.py
Contiene todas las plantillas de código y ejemplos para FoodLanguage IDE
"""

# ==================== PLANTILLAS DE CÓDIGO ====================

CODE_TEMPLATES = {
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

# ==================== EJEMPLOS DE CÓDIGO ====================

EXAMPLE_NAMES = [
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

EXAMPLE_CODES = [
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

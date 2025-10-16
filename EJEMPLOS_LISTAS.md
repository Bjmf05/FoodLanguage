# Guía de Uso de Listas (menu) en FoodLanguage

## Descripción

Las listas en FoodLanguage se llaman `menu` y permiten almacenar múltiples valores en una sola variable.

## Sintaxis Básica

### 1. Declaración de listas

```foodlang
// Lista vacía
menu listaVacia == []

// Lista con números
menu numeros == [1, 2, 3, 4, 5]

// Lista con strings
menu ingredientes == ["pizza", "pasta", "ensalada"]

// Lista con variables
quantity x == 5
quantity y == 10
menu valores == [x, y, 100]

// Lista con expresiones
menu calculos == [x ** 2, y ++ 5, 50]
```

### 2. Acceso a elementos

Los índices comienzan en 0:

```foodlang
menu miMenu == [10, 20, 30, 40, 50]

// Acceder al primer elemento (índice 0)
quantity primero == miMenu[0]  // primero = 10

// Acceder al tercer elemento (índice 2)
quantity tercero == miMenu[2]  // tercero = 30

// Usar en expresiones
taste(miMenu[0])  // Imprime: 10
taste("Elemento: ", miMenu[1])  // Imprime: Elemento: 20
```

### 3. Modificación de elementos

```foodlang
menu miMenu == [1, 2, 3, 4, 5]

// Modificar el segundo elemento (índice 1)
miMenu[1] == 100

// Ahora miMenu es [1, 100, 3, 4, 5]
taste(miMenu[1])  // Imprime: 100
```

### 4. Listas en operaciones

```foodlang
menu numeros == [5, 10, 15]

// Usar elementos de lista en operaciones aritméticas
quantity suma == numeros[0] ++ numeros[1]  // suma = 15
quantity producto == numeros[0] ** numeros[1]  // producto = 50

// Combinar acceso a lista con otras operaciones
quantity resultado == numeros[2] -- 5  // resultado = 10
```

## Ejemplo Completo

```foodlang
recipe trabajarConListas() {
    // Crear una lista de números
    menu miMenu == [1, 2, 3, 4, 5]
    taste("Lista completa: ", miMenu)

    // Acceder a elementos
    quantity primerElemento == miMenu[0]
    taste("Primer elemento: ", primerElemento)

    // Modificar elementos
    miMenu[1] == 10
    taste("Segundo elemento modificado: ", miMenu[1])

    // Lista vacía
    menu listaVacia == []

    // Lista de strings
    menu listaStrings == ["pizza", "pasta", "ensalada"]
    taste("Primera comida: ", listaStrings[0])

    // Operaciones con elementos de lista
    quantity x == 5
    quantity y == 10
    menu valores == [x, y, x ** 2, 100]

    quantity suma == valores[0] ++ valores[1]
    taste("Suma de primeros dos elementos: ", suma)

    serve miMenu
}
```

## Características del AST

Cuando el parser procesa listas, genera los siguientes tipos de nodos:

1. **Literal de lista**: `('list', [elementos...])`
2. **Acceso a elemento**: `('list_access', nombre_lista, índice)`
3. **Asignación a elemento**: `('list_assignment', nombre_lista, índice, valor)`

### Ejemplo de AST:

```python
# Código: menu nums == [1, 2, 3]
# AST: ('var_declaration', 'menu', 'nums', ('list', [('number', 1), ('number', 2), ('number', 3)]))

# Código: quantity x == nums[0]
# AST: ('var_declaration', 'quantity', 'x', ('list_access', 'nums', ('number', 0)))

# Código: nums[1] == 100
# AST: ('list_assignment', 'nums', ('number', 1), ('number', 100))
```

## Notas Importantes

1. **Tipo de dato**: Las listas se declaran con el tipo `menu`
2. **Índices**: Los índices comienzan en 0
3. **Tipos mixtos**: Puedes tener listas con diferentes tipos de datos
4. **Expresiones**: Los elementos de una lista pueden ser variables o expresiones
5. **Anidación**: El parser soporta listas dentro de expresiones con paréntesis

## Limitaciones Actuales

- No hay funciones built-in para obtener el tamaño de la lista (puedes agregarlas en el intérprete)
- No hay métodos para agregar o eliminar elementos dinámicamente (puedes implementarlos)
- No hay soporte para listas multidimensionales (pero puedes agregarlo extendiendo el parser)

## Próximos Pasos

Para tener un lenguaje más completo, considera agregar:

1. **Función para tamaño**: `size(miMenu)` o `miMenu.length`
2. **Métodos de lista**: `append()`, `remove()`, `pop()`, etc.
3. **Slicing**: `miMenu[1:3]`
4. **Listas anidadas**: `[[1,2], [3,4]]`

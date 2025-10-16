from lexer import Lexer
from parser import CulinaryParser

class CulinaryInterpreter:
    def __init__(self):
        self.global_scope = {}
        self.local_scopes = [{}]
        self.functions = {}
        self.return_value = None
        self.break_flag = False
        self.continue_flag = False
    
    def get_current_scope(self):
        """Retorna el scope actual (local si existe, sino global)"""
        return self.local_scopes[-1] if len(self.local_scopes) > 1 else self.global_scope
    
    def get_variable(self, name):
        """Busca una variable en los scopes (local primero, luego global)"""
        # Buscar en scopes locales (de más reciente a más antiguo)
        for scope in reversed(self.local_scopes):
            if name in scope:
                return scope[name]
        
        # Buscar en scope global
        if name in self.global_scope:
            return self.global_scope[name]
        
        raise NameError(f"Variable '{name}' no está definida")
    
    def set_variable(self, name, value):
        """Asigna una variable en el scope actual"""
        scope = self.get_current_scope()
        scope[name] = value
    
    def interpret(self, ast):
        """Punto de entrada principal del intérprete"""
        for node in ast:
            result = self.eval_node(node)
            if self.return_value is not None:
                break
        return result
    
    def eval_node(self, node):
        """Evalúa un nodo del AST"""
        if node is None:
            return None
        
        node_type = node[0]
        
        if node_type == 'recipe':
            return self.eval_recipe(node)
        elif node_type == 'var_declaration':
            return self.eval_var_declaration(node)
        elif node_type == 'assignment':
            return self.eval_assignment(node)
        elif node_type == 'list_assignment':
            return self.eval_list_assignment(node)
        elif node_type == 'matrix_assignment':
            return self.eval_matrix_assignment(node)
        elif node_type == 'print':
            return self.eval_print(node)
        elif node_type == 'input':
            return self.eval_input(node)
        elif node_type == 'if':
            return self.eval_if(node)
        elif node_type == 'while':
            return self.eval_while(node)
        elif node_type == 'for':
            return self.eval_for(node)
        elif node_type == 'switch':
            return self.eval_switch(node)
        elif node_type == 'function_call':
            return self.eval_function_call(node)
        elif node_type == 'return':
            return self.eval_return(node)
        elif node_type == 'break':
            self.break_flag = True
            return None
        elif node_type == 'continue':
            self.continue_flag = True
            return None
        else:
            return self.eval_expression(node)
    
    def eval_recipe(self, node):
        """Evalúa la definición de una función (recipe)"""
        _, name, params, body = node
        self.functions[name] = (params, body)
        return None
    
    def eval_var_declaration(self, node):
        """Evalúa la declaración de una variable"""
        if len(node) == 4:
            _, var_type, var_name, value = node
            evaluated_value = self.eval_expression(value)
            self.set_variable(var_name, evaluated_value)
        else:
            _, var_type, var_name = node
            # Inicializar con valor por defecto según tipo
            default_values = {
                'quantity': 0,
                'portion': 0.0,
                'ingredient': '',
                'menu': []
            }
            self.set_variable(var_name, default_values.get(var_type.lower(), None))
        return None
    
    def eval_assignment(self, node):
        """Evalúa la asignación a una variable"""
        _, var_name, value = node
        evaluated_value = self.eval_expression(value)
        
        # Buscar en qué scope existe la variable
        found = False
        for scope in reversed(self.local_scopes):
            if var_name in scope:
                scope[var_name] = evaluated_value
                found = True
                break
        
        if not found and var_name in self.global_scope:
            self.global_scope[var_name] = evaluated_value
        elif not found:
            # Si no existe, crearla en el scope actual
            self.set_variable(var_name, evaluated_value)
        
        return evaluated_value
    
    def eval_list_assignment(self, node):
        """Evalúa la asignación a un elemento de lista"""
        _, list_name, index_expr, value = node
        
        list_var = self.get_variable(list_name)
        index = self.eval_expression(index_expr)
        evaluated_value = self.eval_expression(value)
        
        if not isinstance(list_var, list):
            raise TypeError(f"'{list_name}' no es una lista")
        
        if not isinstance(index, int):
            raise TypeError(f"El índice debe ser un entero, no {type(index).__name__}")
        
        if index < 0 or index >= len(list_var):
            raise IndexError(f"Índice {index} fuera de rango para lista de tamaño {len(list_var)}")
        
        list_var[index] = evaluated_value
        return evaluated_value
    
    def eval_matrix_assignment(self, node):
        """Evalúa la asignación a un elemento de matriz"""
        _, matrix_name, row_expr, col_expr, value = node
        
        matrix = self.get_variable(matrix_name)
        row = self.eval_expression(row_expr)
        col = self.eval_expression(col_expr)
        evaluated_value = self.eval_expression(value)
        
        if not isinstance(matrix, list):
            raise TypeError(f"'{matrix_name}' no es una matriz")
        
        if not isinstance(row, int) or not isinstance(col, int):
            raise TypeError(f"Los índices deben ser enteros")
        
        if row < 0 or row >= len(matrix):
            raise IndexError(f"Índice de fila {row} fuera de rango")
        
        if not isinstance(matrix[row], list):
            raise TypeError(f"La fila {row} no es una lista")
        
        if col < 0 or col >= len(matrix[row]):
            raise IndexError(f"Índice de columna {col} fuera de rango")
        
        matrix[row][col] = evaluated_value
        return evaluated_value
    
    def eval_print(self, node):
        """Evalúa la función taste (print)"""
        _, arguments = node
        output = []
        for arg in arguments:
            value = self.eval_expression(arg)
            output.append(str(value))
        print(' '.join(output))
        return None
    
    def eval_input(self, node):
        """Evalúa la función add (input)"""
        _, var_name, prompt = node
        if prompt:
            user_input = input(prompt + " ")
        else:
            user_input = input()
        
        # Intentar convertir a número si es posible
        try:
            if '.' in user_input:
                value = float(user_input)
            else:
                value = int(user_input)
        except ValueError:
            value = user_input
        
        self.set_variable(var_name, value)
        return value
    
    def eval_if(self, node):
        """Evalúa una estructura if/else"""
        _, condition, if_body, else_body = node
        
        condition_value = self.eval_expression(condition)
        
        if condition_value:
            for statement in if_body:
                self.eval_node(statement)
                if self.return_value is not None or self.break_flag or self.continue_flag:
                    break
        elif else_body:
            for statement in else_body:
                self.eval_node(statement)
                if self.return_value is not None or self.break_flag or self.continue_flag:
                    break
        
        return None
    
    def eval_while(self, node):
        """Evalúa un ciclo while"""
        _, condition, body = node
        
        while self.eval_expression(condition):
            for statement in body:
                self.eval_node(statement)
                
                if self.return_value is not None:
                    return None
                
                if self.break_flag:
                    self.break_flag = False
                    return None
                
                if self.continue_flag:
                    self.continue_flag = False
                    break
        
        return None
    
    def eval_for(self, node):
        """Evalúa un ciclo for"""
        _, var_type, var_name, start_value, condition, increment, body = node
        
        # Inicializar variable del for
        start = self.eval_expression(start_value)
        self.set_variable(var_name, start)
        
        # Ejecutar el ciclo
        while self.eval_expression(condition):
            for statement in body:
                self.eval_node(statement)
                
                if self.return_value is not None:
                    return None
                
                if self.break_flag:
                    self.break_flag = False
                    return None
                
                if self.continue_flag:
                    self.continue_flag = False
                    break
            
            # Ejecutar incremento (puede ser expresión o statement)
            if increment[0] == 'assignment':
                self.eval_node(increment)
            else:
                self.eval_expression(increment)
        
        return None
    
    def eval_switch(self, node):
        """Evalúa una estructura switch (season)"""
        _, switch_expr, cases, default_case = node
        
        # Evaluar la expresión del switch
        switch_value = self.eval_expression(switch_expr)
        
        # Buscar caso coincidente
        case_matched = False
        for case_value, case_body in cases:
            evaluated_case = self.eval_expression(case_value)
            
            if switch_value == evaluated_case:
                case_matched = True
                # Ejecutar cuerpo del caso
                for statement in case_body:
                    self.eval_node(statement)
                    
                    if self.return_value is not None:
                        return None
                    
                    if self.break_flag:
                        self.break_flag = False
                        return None
                    
                    if self.continue_flag:
                        return None
                
                # En FoodLanguage, por defecto hay break implícito
                # (no hay fall-through como en C)
                break
        
        # Si no coincidió ningún caso, ejecutar default
        if not case_matched and default_case is not None:
            for statement in default_case:
                self.eval_node(statement)
                
                if self.return_value is not None:
                    return None
                
                if self.break_flag:
                    self.break_flag = False
                    return None
                
                if self.continue_flag:
                    return None
        
        return None
    
    def eval_function_call(self, node):
        """Evalúa una llamada a función"""
        _, func_name, arguments = node
        
        if func_name not in self.functions:
            raise NameError(f"Función '{func_name}' no está definida")
        
        params, body = self.functions[func_name]
        
        # Evaluar argumentos
        arg_values = [self.eval_expression(arg) for arg in arguments]
        
        # Verificar cantidad de argumentos
        if len(arg_values) != len(params):
            raise TypeError(f"Función '{func_name}' espera {len(params)} argumentos, se proporcionaron {len(arg_values)}")
        
        # Crear nuevo scope local
        self.local_scopes.append({})
        
        # Asignar parámetros
        for (param_type, param_name), arg_value in zip(params, arg_values):
            self.set_variable(param_name, arg_value)
        
        # Ejecutar cuerpo de la función
        for statement in body:
            self.eval_node(statement)
            if self.return_value is not None:
                break
        
        # Guardar valor de retorno
        return_val = self.return_value
        self.return_value = None
        
        # Salir del scope local
        self.local_scopes.pop()
        
        return return_val
    
    def eval_return(self, node):
        """Evalúa un return"""
        _, value = node
        if value is not None:
            self.return_value = self.eval_expression(value)
        else:
            self.return_value = None
        return self.return_value
    
    def eval_expression(self, node):
        """Evalúa una expresión"""
        if node is None:
            return None
        
        node_type = node[0]
        
        if node_type == 'number':
            return node[1]
        elif node_type == 'string':
            return node[1]
        elif node_type == 'char':
            return node[1]
        elif node_type == 'boolean':
            return node[1]
        elif node_type == 'null':
            return None
        elif node_type == 'variable':
            return self.get_variable(node[1])
        elif node_type == 'list':
            # Evaluar cada elemento de la lista
            return [self.eval_expression(elem) for elem in node[1]]
        elif node_type == 'list_access':
            return self.eval_list_access(node)
        elif node_type == 'matrix_access':
            return self.eval_matrix_access(node)
        elif node_type == 'binary_op':
            return self.eval_binary_op(node)
        elif node_type == 'comparison':
            return self.eval_comparison(node)
        elif node_type == 'logical_and':
            return self.eval_logical_and(node)
        elif node_type == 'logical_or':
            return self.eval_logical_or(node)
        elif node_type == 'logical_not':
            return self.eval_logical_not(node)
        elif node_type == 'inc_dec_prefix':
            return self.eval_inc_dec_prefix(node)
        elif node_type == 'inc_dec_postfix':
            return self.eval_inc_dec_postfix(node)
        elif node_type == 'function_call':
            return self.eval_function_call(node)
        else:
            raise RuntimeError(f"Tipo de nodo desconocido: {node_type}")
    
    def eval_list_access(self, node):
        """Evalúa el acceso a un elemento de lista"""
        _, list_name, index_expr = node
        
        list_var = self.get_variable(list_name)
        index = self.eval_expression(index_expr)
        
        if not isinstance(list_var, list):
            raise TypeError(f"'{list_name}' no es una lista")
        
        if not isinstance(index, int):
            raise TypeError(f"El índice debe ser un entero, no {type(index).__name__}")
        
        if index < 0 or index >= len(list_var):
            raise IndexError(f"Índice {index} fuera de rango para lista de tamaño {len(list_var)}")
        
        return list_var[index]
    
    def eval_matrix_access(self, node):
        """Evalúa el acceso a un elemento de matriz"""
        _, matrix_name, row_expr, col_expr = node
        
        matrix = self.get_variable(matrix_name)
        row = self.eval_expression(row_expr)
        col = self.eval_expression(col_expr)
        
        if not isinstance(matrix, list):
            raise TypeError(f"'{matrix_name}' no es una matriz")
        
        if not isinstance(row, int) or not isinstance(col, int):
            raise TypeError(f"Los índices deben ser enteros")
        
        if row < 0 or row >= len(matrix):
            raise IndexError(f"Índice de fila {row} fuera de rango")
        
        if not isinstance(matrix[row], list):
            raise TypeError(f"La fila {row} no es una lista")
        
        if col < 0 or col >= len(matrix[row]):
            raise IndexError(f"Índice de columna {col} fuera de rango")
        
        return matrix[row][col]
    
    def eval_binary_op(self, node):
        """Evalúa operaciones binarias (+, -, *, /)"""
        _, left, operator, right = node
        
        left_val = self.eval_expression(left)
        right_val = self.eval_expression(right)
        
        if operator == '++':
            return left_val + right_val
        elif operator == '--':
            return left_val - right_val
        elif operator == '**':
            return left_val * right_val
        elif operator == '\\\\':
            if right_val == 0:
                raise ZeroDivisionError("División por cero")
            return left_val / right_val
        else:
            raise RuntimeError(f"Operador binario desconocido: {operator}")
    
    def eval_comparison(self, node):
        """Evalúa operaciones de comparación"""
        _, left, operator, right = node
        
        left_val = self.eval_expression(left)
        right_val = self.eval_expression(right)
        
        if operator == '===':
            return left_val == right_val
        elif operator == '!=':
            return left_val != right_val
        elif operator == '>':
            return left_val > right_val
        elif operator == '<':
            return left_val < right_val
        elif operator == '>=':
            return left_val >= right_val
        elif operator == '<=':
            return left_val <= right_val
        else:
            raise RuntimeError(f"Operador de comparación desconocido: {operator}")
    
    def eval_logical_and(self, node):
        """Evalúa operador lógico AND (spoon)"""
        _, left, operator, right = node
        
        left_val = self.eval_expression(left)
        if not left_val:
            return False
        
        right_val = self.eval_expression(right)
        return bool(left_val and right_val)
    
    def eval_logical_or(self, node):
        """Evalúa operador lógico OR (fork)"""
        _, left, operator, right = node
        
        left_val = self.eval_expression(left)
        if left_val:
            return True
        
        right_val = self.eval_expression(right)
        return bool(left_val or right_val)
    
    def eval_logical_not(self, node):
        """Evalúa operador lógico NOT (unseasoned)"""
        _, operand = node
        
        operand_val = self.eval_expression(operand)
        return not bool(operand_val)
    
    def eval_inc_dec_prefix(self, node):
        """Evalúa incremento/decremento prefijo (++x, --x)"""
        _, operator, var_name = node
        
        current_value = self.get_variable(var_name)
        
        if operator == '++':
            new_value = current_value + 1
        else:  # '--'
            new_value = current_value - 1
        
        # Actualizar variable
        self.eval_assignment(('assignment', var_name, ('number', new_value)))
        
        return new_value
    
    def eval_inc_dec_postfix(self, node):
        """Evalúa incremento/decremento postfijo (x++, x--)"""
        _, var_name, operator = node
        
        current_value = self.get_variable(var_name)
        
        if operator == '++':
            new_value = current_value + 1
        else:  # '--'
            new_value = current_value - 1
        
        # Actualizar variable
        self.eval_assignment(('assignment', var_name, ('number', new_value)))
        
        return current_value  # Retorna el valor ANTES del incremento

# Función principal para ejecutar código
def run_food_language(code):
    """Ejecuta código de FoodLanguage"""
    try:
        # Lexer
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # Parser
        parser = CulinaryParser(tokens)
        ast = parser.parse()
        
        # Interpreter
        interpreter = CulinaryInterpreter()
        result = interpreter.interpret(ast)
        
        return result
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

# Ejemplos de uso
if __name__ == '__main__':
    # Ejemplo 1: Función simple
    code1 = """
    recipe saludar(ingredient nombre) {
        taste("¡Hola", nombre, "!")
        serve flavorless
    }
    
    saludar("Chef")
    """
    
    print("=== Ejemplo 1: Función simple ===")
    run_food_language(code1)
    
    # Ejemplo 2: Ciclo while
    code2 = """
    quantity i == 1
    cook_while (i <= 5) {
        taste("Número:", i)
        i == i ++ 1
    }
    """
    
    print("\n=== Ejemplo 2: Ciclo while ===")
    run_food_language(code2)
    
    # Ejemplo 3: Listas
    code3 = """
    menu numeros == [10, 20, 30, 40, 50]
    taste("Lista:", numeros)
    taste("Primer elemento:", numeros[0])
    
    numeros[2] == 99
    taste("Elemento modificado:", numeros[2])
    
    quantity suma == numeros[0] ++ numeros[1]
    taste("Suma:", suma)
    """
    
    print("\n=== Ejemplo 3: Listas ===")
    run_food_language(code3)
    
    # Ejemplo 4: Matrices
    code4 = """
    menu matriz == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    taste("Matriz:", matriz)
    taste("Elemento [0][0]:", matriz[0][0])
    taste("Elemento [1][2]:", matriz[1][2])
    
    matriz[1][1] == 100
    taste("Centro modificado:", matriz[1][1])
    """
    
    print("\n=== Ejemplo 4: Matrices ===")
    run_food_language(code4)
    
    # Ejemplo 5: If/else
    code5 = """
    quantity edad == 18
    
    if_has (edad >= 18) {
        taste("Eres mayor de edad")
    } otherwise {
        taste("Eres menor de edad")
    }
    """
    
    print("\n=== Ejemplo 5: If/else ===")
    run_food_language(code5)
    
    # Ejemplo 6: Función con retorno
    code6 = """
    recipe sumar(quantity a, quantity b) {
        quantity resultado == a ++ b
        serve resultado
    }
    
    quantity total == sumar(5, 3)
    taste("5 + 3 =", total)
    """
    
    print("\n=== Ejemplo 6: Función con retorno ===")
    run_food_language(code6)
    
    # Ejemplo 7: Ciclo for (stir)
    code7 = """
    taste("Contando del 1 al 5:")
    stir (quantity i == 1, i <= 5, i == i ++ 1) {
        taste("  Número:", i)
    }
    
    taste("Tabla del 3:")
    stir (quantity j == 1, j <= 10, j == j ++ 1) {
        quantity resultado == 3 ** j
        taste("  3 x", j, "=", resultado)
    }
    """
    
    print("\n=== Ejemplo 7: Ciclo for (stir) ===")
    run_food_language(code7)
    
    # Ejemplo 8: Factorial recursivo
    code8 = """
    recipe factorial(quantity n) {
        if_has (n <= 1) {
            serve 1
        }
        quantity resultado == n ** factorial(n -- 1)
        serve resultado
    }
    
    taste("Factorial de 5:", factorial(5))
    """
    
    print("\n=== Ejemplo 8: Factorial recursivo ===")
    run_food_language(code8)
    
    # Ejemplo 9: Switch (season)
    code9 = """
    quantity dia == 3
    
    season (dia) {
        with 1:
            taste("Lunes - Día de preparación")
        with 2:
            taste("Martes - Día de cocción")
        with 3:
            taste("Miércoles - Día de horneado")
        with 4:
            taste("Jueves - Día de fritura")
        with 5:
            taste("Viernes - Día de parrilla")
        default_flavor:
            taste("Fin de semana - Descanso")
    }
    
    ingredient opcion == "B"
    
    season (opcion) {
        with "A":
            taste("Seleccionaste: Aperitivo")
        with "B":
            taste("Seleccionaste: Plato principal")
            quantity precio == 15
            taste("Precio:", precio)
        with "C":
            taste("Seleccionaste: Postre")
        default_flavor:
            taste("Opción no válida")
    }
    """
    
    print("\n=== Ejemplo 9: Switch (season) ===")
    run_food_language(code9)
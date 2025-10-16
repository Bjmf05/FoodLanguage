from lexer import Lexer

class CulinaryParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None
        self.conditional_stack = []
        self.tree = None
        self.in_recipe = False
        self.recipe_name = ""
        self.already_main = False

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def expect(self, token_type, token_value=None):
        if self.current_token and self.current_token.type == token_type:
            if token_value is None or self.current_token.value.lower() == token_value.lower():
                self.advance()
                return True
            else:
                raise SyntaxError(
                    f"Se esperaba {token_type} con valor '{token_value}', pero se encontró {self.current_token}")
        else:
            raise SyntaxError(f"Se esperaba {token_type}, pero se encontró {self.current_token}")

    def parse(self):
        counter = 1
        self.tree = []
        while self.current_token is not None:
            print('Iteración del ciclo numero', counter)
            print('El current token que viene es ', self.current_token.type, self.current_token.value)
            
            if (self.current_token.type == 'FUNCTION' and 
                self.current_token.value.lower() == 'recipe'):
                self.tree.append(self.parse_recipe())
            elif (self.current_token.type == 'PRINT' and 
                  self.current_token.value.lower() == 'taste'):
                self.tree.append(self.parse_print())
            elif (self.current_token.type == 'INPUT' and 
                  self.current_token.value.lower() == 'add'):
                self.tree.append(self.parse_input())
            elif (self.current_token.type == 'IF' and 
                  self.current_token.value.lower() in ['if', 'if_has']):
                self.tree.append(self.parse_if())
            elif (self.current_token.type == 'ELSE' and 
                  self.current_token.value.lower() == 'otherwise'):
                self.tree.append(self.parse_else())
            elif (self.current_token.type == 'WHILE' and 
                  self.current_token.value.lower() == 'cook_while'):
                self.tree.append(self.parse_while())
            elif (self.current_token.type == 'FOR' and 
                  self.current_token.value.lower() == 'stir'):
                self.tree.append(self.parse_for())
            elif self.current_token.type in ['INT', 'FLOAT', 'STRING', 'LIST']:
                self.tree.append(self.parse_var_declaration())
            elif self.current_token.type == 'IDENTIFIER':
                self.tree.append(self.parse_assignment_or_call())
            elif (self.current_token.type == 'RETURN' and 
                  self.current_token.value.lower() == 'serve'):
                self.tree.append(self.parse_return())
            elif (self.current_token.type == 'BREAK' and 
                  self.current_token.value.lower() == 'stop_stirring'):
                self.tree.append(self.parse_break())
            elif (self.current_token.type == 'CONTINUE' and 
                  self.current_token.value.lower() == 'keep_stirring'):
                self.tree.append(self.parse_continue())
            else:
                raise SyntaxError(f"Token inesperado {self.current_token.type}:{self.current_token.value}")
            counter += 1
        return self.tree

    def parse_recipe(self):
        self.expect('FUNCTION', 'recipe')
        self.in_recipe = True
        
        # Nombre de la recipe (función)
        if self.current_token.type == 'IDENTIFIER':
            recipe_name = self.current_token.value
            self.recipe_name = recipe_name
            self.advance()
        else:
            raise SyntaxError(f"Se esperaba un nombre para la recipe, se encontró {self.current_token}")
        
        self.expect('DELIMETER', '(')
        parameters = self.parse_parameters()
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', '{')
        
        # Cuerpo de la recipe
        body = self.parse_recipe_body()
        self.expect('DELIMETER', '}')
        
        self.in_recipe = False
        self.recipe_name = ""
        return ('recipe', recipe_name, parameters, body)

    def parse_parameters(self):
        parameters = []
        # si el siguiente token es ')' no hay parámetros
        if self.current_token.type == 'DELIMETER' and self.current_token.value == ')':
            return parameters

        while True:
            # Tipo del parámetro
            if self.current_token.type in ['INT', 'FLOAT', 'STRING', 'LIST']:
                param_type = self.current_token.value
                self.advance()
            else:
                raise SyntaxError(f"Se esperaba tipo de parámetro, se encontró {self.current_token}")
            
            # Nombre del parámetro
            if self.current_token.type == 'IDENTIFIER':
                param_name = self.current_token.value
                self.advance()
                parameters.append((param_type, param_name))
            else:
                raise SyntaxError(f"Se esperaba nombre de parámetro, se encontró {self.current_token}")
            
            if (self.current_token.type == 'DELIMETER' and 
                self.current_token.value == ')'):
                break
            elif self.current_token.type == 'DELIMETER' and self.current_token.value == ',':
                self.advance()
            else:
                raise SyntaxError(f"Se esperaba ',' o ')', se encontró {self.current_token}")
        return parameters

    def parse_recipe_body(self):
        statements = []
        open_braces = 1
        
        while open_braces > 0 and self.current_token:
            if (self.current_token.type == 'DELIMETER' and 
                self.current_token.value == '}'):
                open_braces -= 1
                if open_braces == 0:
                    break
                self.advance()
            elif (self.current_token.type == 'DELIMETER' and 
                  self.current_token.value == '{'):
                open_braces += 1
                self.advance()
            else:
                statement = self.parse_statement()
                if statement:
                    statements.append(statement)
        
        return statements

    def parse_statement(self):
        if (self.current_token.type == 'PRINT' and 
            self.current_token.value.lower() == 'taste'):
            return self.parse_print()
        elif (self.current_token.type == 'INPUT' and 
              self.current_token.value.lower() == 'add'):
            return self.parse_input()
        elif (self.current_token.type == 'IF' and 
              self.current_token.value.lower() in ['if', 'if_has']):
            return self.parse_if()
        elif (self.current_token.type == 'WHILE' and 
              self.current_token.value.lower() == 'cook_while'):
            return self.parse_while()
        elif (self.current_token.type == 'FOR' and 
              self.current_token.value.lower() == 'stir'):
            return self.parse_for()
        elif self.current_token.type in ['INT', 'FLOAT', 'STRING', 'LIST']:
            return self.parse_var_declaration()
        elif self.current_token.type == 'IDENTIFIER':
            return self.parse_assignment_or_call()
        elif (self.current_token.type == 'RETURN' and 
              self.current_token.value.lower() == 'serve'):
            return self.parse_return()
        elif (self.current_token.type == 'BREAK' and 
              self.current_token.value.lower() == 'stop_stirring'):
            return self.parse_break()
        elif (self.current_token.type == 'CONTINUE' and 
              self.current_token.value.lower() == 'keep_stirring'):
            return self.parse_continue()
        else:
            raise SyntaxError(f"Declaración inesperada: {self.current_token}")

    def parse_var_declaration(self):
        var_type = self.current_token.value
        self.advance()
        
        if self.current_token.type == 'IDENTIFIER':
            var_name = self.current_token.value
            self.advance()
            
            if (self.current_token.type == 'ASSIGN' and 
                self.current_token.value == '=='):
                self.advance()
                value = self.parse_expression()
                return ('var_declaration', var_type, var_name, value)
            else:
                return ('var_declaration', var_type, var_name)
        else:
            raise SyntaxError(f"Se esperaba nombre de variable, se encontró {self.current_token}")

    def parse_assignment_or_call(self):
        identifier = self.current_token.value
        self.advance()
        
        # Acceso a índice de lista: identifier[index]
        if (self.current_token and self.current_token.type == 'DELIMETER' and 
            self.current_token.value == '['):
            self.advance()
            index = self.parse_expression()
            self.expect('DELIMETER', ']')
            
            # Asignación a elemento de lista: identifier[index] == value
            if (self.current_token and self.current_token.type == 'ASSIGN' and 
                self.current_token.value == '=='):
                self.advance()
                value = self.parse_expression()
                return ('list_assignment', identifier, index, value)
            else:
                # Solo acceso a elemento: identifier[index]
                return ('list_access', identifier, index)
        
        elif (self.current_token and self.current_token.type == 'ASSIGN' and 
            self.current_token.value == '=='):
            return self.parse_assignment(identifier)
        elif self.current_token and self.current_token.type == 'DELIMETER' and self.current_token.value == '(':
            return self.parse_function_call(identifier)
        elif (self.current_token and self.current_token.type in ['PLUS', 'MINUS'] and
              self.current_token.value in ['++', '--']):
            operator = self.current_token.value
            self.advance()
            
            # caso: x++ (postfix) o x++ <number> (extra)
            if self.current_token and self.current_token.type == 'NUMBER':
                right = self.parse_primary()
                return ('binary_op', ('variable', identifier), operator, right)
            else:
                return ('inc_dec_postfix', identifier, operator)
        else:
            raise SyntaxError(f"Se esperaba '==', '(', '[', '++' o '--', se encontró {self.current_token}")

    def parse_assignment(self, var_name):
        self.expect('ASSIGN', '==')
        value = self.parse_expression()
        return ('assignment', var_name, value)

    def parse_function_call(self, func_name):
        self.expect('DELIMETER', '(')
        arguments = self.parse_arguments()
        self.expect('DELIMETER', ')')
        return ('function_call', func_name, arguments)

    def parse_arguments(self):
        arguments = []
        # si inmediato hay ')', no hay argumentos
        if self.current_token.type == 'DELIMETER' and self.current_token.value == ')':
            return arguments

        while True:
            arg = self.parse_expression()
            # añadir aunque arg sea None (si permite expresiones vacías), pero normalmente arg no debe ser None
            arguments.append(arg)
            
            if (self.current_token.type == 'DELIMETER' and 
                self.current_token.value == ')'):
                break
            elif self.current_token.type == 'DELIMETER' and self.current_token.value == ',':
                self.advance()
            else:
                raise SyntaxError(f"Se esperaba ',' o ')', se encontró {self.current_token}")
        return arguments

    def parse_expression(self):      
        return self.parse_logical_or()
    
    def parse_logical_or(self):
        left = self.parse_logical_and()
        while (self.current_token and 
               self.current_token.type == 'OR'):
            operator = self.current_token.value
            self.advance()
            right = self.parse_logical_and()
            left = ('logical_or', left, operator, right)
        return left
    
    def parse_logical_and(self):
        left = self.parse_comparison()
        while (self.current_token and 
               self.current_token.type == 'AND'):
            operator = self.current_token.value
            self.advance()
            right = self.parse_comparison()
            left = ('logical_and', left, operator, right)
        return left
    
    def parse_comparison(self):
        left = self.parse_term()
        while (self.current_token and 
               self.current_token.type in ['GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL', 'EQUAL','NOT_EQUAL']):
            operator = self.current_token.value
            self.advance()
            right = self.parse_term()
            left = ('comparison', left, operator, right)
        return left
    

    def parse_term(self):
        left = self.parse_factor()
        while (self.current_token and 
               self.current_token.type in ['PLUS', 'MINUS']):
            operator = self.current_token.value
            self.advance()
            right = self.parse_factor()
            left = ('binary_op', left, operator, right)
        return left
    
    def parse_factor(self):
        left = self.parse_unary()
        while (self.current_token and 
               self.current_token.type in ['MULTIPLY', 'DIVIDE']):
            operator = self.current_token.value
            self.advance()
            right = self.parse_unary()
            left = ('binary_op', left, operator, right)
        return left
    
    def parse_inc_dec(self):
        if (self.current_token.type in ['PLUS', 'MINUS'] and
            self.current_token.value in ['++', '--']):
            operator = self.current_token.value
            self.advance()
            if self.current_token.type == 'IDENTIFIER':
                var_name = self.current_token.value
                self.advance()
                return ('inc_dec_pre', operator, var_name)
            else:
                raise SyntaxError(f"Se esperaba nombre de variable para incremento/decremento, se encontró {self.current_token}")

    def parse_unary(self):
        return self.parse_primary()

    def parse_primary(self):

        if (self.current_token and self.current_token.type in ['PLUS', 'MINUS'] and
            self.current_token.value in ['++', '--']):
            operator = self.current_token.value
            self.advance()
        
            if self.current_token and self.current_token.type == 'IDENTIFIER':
                identifier = self.current_token.value
                self.advance()
                return ('inc_dec_prefix', operator, identifier)
            else:
                raise SyntaxError(f"Se esperaba identificador después de {operator}")
        
        # Literal de lista: [1, 2, 3]
        elif (self.current_token and self.current_token.type == 'DELIMETER' and 
              self.current_token.value == '['):
            return self.parse_list_literal()
            
        elif self.current_token and self.current_token.type == 'IDENTIFIER':
            value = self.current_token.value
            self.advance()
            
            # Acceso a índice de lista: identifier[index]
            if (self.current_token and self.current_token.type == 'DELIMETER' and 
                self.current_token.value == '['):
                self.advance()
                index = self.parse_expression()
                self.expect('DELIMETER', ']')
                return ('list_access', value, index)
            
            if (self.current_token and self.current_token.type == 'DELIMETER' and 
                self.current_token.value == '('):
                return self.parse_function_call(value)
            
            if (self.current_token and self.current_token.type in ['PLUS', 'MINUS'] and
                self.current_token.value in ['++', '--']):
                operator = self.current_token.value
                self.advance()
                
                # caso: x++ (postfix) o x++ <number> (extra)
                if self.current_token and self.current_token.type == 'NUMBER':
                    right = self.parse_primary()
                    return ('binary_op', ('variable', value), operator, right)
                else:
                    return ('inc_dec_postfix', value, operator)
            return ('variable', value)
        
        elif self.current_token and self.current_token.type == 'NUMBER':
            if '.' in self.current_token.value:
                value = float(self.current_token.value)
            else:
                value = int(self.current_token.value)
            self.advance()
            return ('number', value)
        
        elif self.current_token and self.current_token.type == 'STRING_LITERAL':
            value = self.current_token.value.strip('"')
            self.advance()
            return ('string', value)
        
        elif self.current_token and self.current_token.type == 'CHAR':
            value = self.current_token.value.strip("'")
            self.advance()
            return ('char', value)
        
        elif self.current_token and self.current_token.type == 'TRUE':
            self.advance()
            return ('boolean', True)
        
        elif self.current_token and self.current_token.type == 'FALSE':
            self.advance()
            return ('boolean', False)
        
        elif self.current_token and self.current_token.type == 'NULL':
            self.advance()
            return ('null', None)
        
        # Expresión entre paréntesis
        elif (self.current_token and self.current_token.type == 'DELIMETER' and 
              self.current_token.value == '('):
            self.advance()
            expr = self.parse_expression()
            self.expect('DELIMETER', ')')
            return expr
        
        elif self.current_token and (self.current_token.type in ['PLUS', 'MINUS'] and
             self.current_token.value in ['++', '--']):
            return self.parse_inc_dec()
        
        else:
            raise SyntaxError(f"Expresión inválida: {self.current_token}")

    def parse_print(self):
        self.expect('PRINT', 'taste')
        self.expect('DELIMETER', '(')
        arguments = self.parse_arguments()
        self.expect('DELIMETER', ')')
        return ('print', arguments)

    def parse_input(self):
        self.expect('INPUT', 'add')
        self.expect('DELIMETER', '(')
        
        if self.current_token.type == 'STRING_LITERAL':
            prompt = self.current_token.value.strip('"')
            self.advance()
            self.expect('DELIMETER', ',')
        
        if self.current_token.type == 'IDENTIFIER':
            var_name = self.current_token.value
            self.advance()
            self.expect('DELIMETER', ')')
            return ('input', var_name, prompt if 'prompt' in locals() else None)
        else:
            raise SyntaxError(f"Se esperaba nombre de variable para input, se encontró {self.current_token}")

    def parse_if(self):
        self.advance()  # Consume 'if' o 'if_has'
        self.expect('DELIMETER', '(')
        condition = self.parse_expression()
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', '{')
        
        if_body = self.parse_recipe_body()
        self.expect('DELIMETER', '}')
        
        else_body = None
        if (self.current_token and self.current_token.type == 'ELSE' and 
            self.current_token.value.lower() == 'otherwise'):
            self.advance()
            self.expect('DELIMETER', '{')
            else_body = self.parse_recipe_body()
            self.expect('DELIMETER', '}')
        
        return ('if', condition, if_body, else_body)

    def parse_else(self):
        self.expect('ELSE', 'otherwise')
        self.expect('DELIMETER', '{')
        else_body = self.parse_recipe_body()
        self.expect('DELIMETER', '}')
        return ('else', else_body)

    def parse_while(self):
        self.expect('WHILE', 'cook_while')
        self.expect('DELIMETER', '(')
        condition = self.parse_expression()
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', '{')
        while_body = self.parse_recipe_body()
        self.expect('DELIMETER', '}')
        return ('while', condition, while_body)
    
    def parse_for(self):
        self.expect('FOR', 'stir')
        self.expect('DELIMETER', '(')
        
        # Parse initialization
        if self.current_token.type in ['INT', 'FLOAT']:
            var_type = self.current_token.value
            self.advance()
        else:
            raise SyntaxError(f"Se esperaba tipo de variable en for, se encontró {self.current_token}")
        
        if self.current_token.type == 'IDENTIFIER':
            var_name = self.current_token.value
            self.advance()
        else:
            raise SyntaxError(f"Se esperaba nombre de variable en for, se encontró {self.current_token}")
        
        self.expect('ASSIGN', '==')
        start_value = self.parse_expression()
        self.expect('DELIMETER', ',')
        
        # Parse condition
        condition = self.parse_expression()
        self.expect('DELIMETER', ',')
        
        # Parse increment
        increment = self.parse_expression()
        self.expect('DELIMETER', ')')
        self.expect('DELIMETER', '{')
        
        for_body = self.parse_recipe_body()
        self.expect('DELIMETER', '}')
        
        return ('for', var_type, var_name, start_value, condition, increment, for_body)

    def parse_return(self):
        self.expect('RETURN', 'serve')
        if (self.current_token.type == 'DELIMETER' and 
            self.current_token.value == ';'):
            self.advance()
            return ('return', None)
        else:
            value = self.parse_expression()
            return ('return', value)

    def parse_break(self):
        self.expect('BREAK', 'stop_stirring')
        return ('break',)

    def parse_continue(self):
        self.expect('CONTINUE', 'keep_stirring')
        return ('continue',)
    
    def parse_list_literal(self):
        """Parse una lista literal: [elem1, elem2, ...]"""
        self.expect('DELIMETER', '[')
        elements = []
        
        # Lista vacía
        if (self.current_token and self.current_token.type == 'DELIMETER' and 
            self.current_token.value == ']'):
            self.advance()
            return ('list', elements)
        
        # Lista con elementos
        while True:
            element = self.parse_expression()
            elements.append(element)
            
            if (self.current_token and self.current_token.type == 'DELIMETER' and 
                self.current_token.value == ']'):
                self.advance()
                break
            elif (self.current_token and self.current_token.type == 'DELIMETER' and 
                  self.current_token.value == ','):
                self.advance()
            else:
                raise SyntaxError(f"Se esperaba ',' o ']' en lista, se encontró {self.current_token}")
        
        return ('list', elements)

# Ejemplo de uso

if __name__ == '__main__':
    test_cases = [
        # Prueba de recipe
        """
        recipe calcularTotal(quantity precio, quantity cantidad) {
            quantity total == precio ** cantidad ++ 5 -- 2 \\\\ 3
            taste("Total: ", total)
            serve total
        }
        """,
        # Prueba de ciclo while
        """
        cook_while (x > 0 spoon y < 10 fork z === 5) {
            taste("Cocinando...")
            taste(x)
            x--
            y++
            z == z ++ 1
        }
        """,
        # Prueba de if/else
        """
        if_has (x > 5) {
            taste("Mayor que 5")
        } otherwise {
            taste("No es mayor que 5")
        }
        """,
        # Prueba de for
        """
        stir (quantity i == 0, i < 10, i++ ) {
            taste(i)
        }
        """,
        # Prueba de booleanos
        """
        recipe pruebaBooleanos() {
            readyVar == ready
            rawVar == raw
            taste(readyVar)
            taste(rawVar)
            serve readyVar
        }
        """,
        # Prueba de listas (menu)
        """
        recipe pruebaListas() {
            menu miMenu == [1, 2, 3, 4, 5]
            taste("Lista completa: ", miMenu)
            quantity primerElemento == miMenu[0]
            taste("Primer elemento: ", primerElemento)
            miMenu[1] == 10
            taste("Segundo elemento modificado: ", miMenu[1])
            menu listaVacia == []
            menu listaStrings == ["pizza", "pasta", "ensalada"]
            serve miMenu
        }
        """,
        # Prueba de lista con expresiones
        """
        recipe pruebaListaExpresiones() {
            quantity x == 5
            quantity y == 10
            menu numeros == [x, y, x ** 2, 100]
            taste(numeros[0])
            taste(numeros[2])
            quantity suma == numeros[0] ++ numeros[1]
            taste("Suma: ", suma)
            serve numeros
        }
        """
    ]

    for idx, code in enumerate(test_cases, 1):
        print(f"\n--- Prueba #{idx} ---")
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = CulinaryParser(tokens)
        try:
            ast = parser.parse()
            print("AST resultante:", ast)
        except Exception as e:
            print("Error:", e)
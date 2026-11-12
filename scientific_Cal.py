import math
import re

operators = {
    "+" : 1 ,
    "-" : 1 ,
    "*" : 2 ,
    "/" : 2 ,
    "%" : 2 ,
    "u-" : 3 ,
    "^" : 4 ,
}

functions = {
    "sqrt" : math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log10,
    "ln": math.log,
    "abs": abs,
    "ceil": math.ceil,
    "floor": math.floor,
    "exp": math.exp,
    "fact" : math.factorial,
    "sind": lambda x: math.sin(math.radians(x)),
    "cosd": lambda x: math.cos(math.radians(x)),
    "tand": lambda x: math.tan(math.radians(x)),
    "asin": lambda x: math.degrees(math.asin(x)),
    "acos" : lambda x:math.degrees(math.acos(x)),
    "atan" :lambda x: math.degrees(math.atan(x)),
}

def calc_banner():
    print("╔══════════════════════════════════════╗")
    print("║          C A L C U L A T O R         ║")
    print("║     Scientific Terminal Calculator   ║")
    print("╠══════════════════════════════════════╣")
    print("║ Type 'menu' to see all Calc-Commands ║")
    print("╚══════════════════════════════════════╝")

def menu():
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║                  C A L C U L A T O R                     ║
║                  SCIENTIFIC EDITION                      ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  ABOUT                                                   ║
║  Scientific Calculator is a command-line                 ║
║  calculator designed to perform basic arithmetic and     ║
║  advanced mathematical calculations using expressions.   ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  1. BASIC ARITHMETIC                                     ║
║     +   Addition                                         ║
║     -   Subtraction                                      ║
║     *   Multiplication                                   ║
║     /   Division                                         ║
║     %   Modulus (Remainder)                              ║
║     ^   Exponentiation (Power)                           ║
║                                                          ║
║  2. MATHEMATICAL FUNCTIONS                               ║
║     sqrt(x)   Square Root                                ║
║     abs(x)    Absolute Value                             ║
║     fact(x)   Factorial                                  ║
║     log(x)    Logarithm (Base 10)                        ║
║     ln(x)     Natural Logarithm                          ║
║     exp(x)    Exponential (e^x)                          ║
║     ceil(x)   Round Up                                   ║
║     floor(x)  Round Down                                 ║
║                                                          ║
║  3. TRIGONOMETRIC FUNCTIONS                              ║
║     sin(x)    Sine (Radians)                             ║
║     cos(x)    Cosine (Radians)                           ║
║     tan(x)    Tangent (Radians)                          ║
║     sind(x)   Sine (Degrees)                             ║
║     cosd(x)   Cosine (Degrees)                           ║
║     tand(x)   Tangent (Degrees)                          ║
║     asin(x)   Inverse Sine (Degrees)                     ║
║     acos(x)   Inverse Cosine (Degrees)                   ║
║     atan(x)   Inverse Tangent (Degrees)                  ║
║                                                          ║
║  4. EXPRESSION SUPPORT                                   ║
║     - Operator precedence                                ║
║     - Parentheses and nested expressions                 ║
║     - Negative numbers                                   ║
║     - Multiple functions in one expression               ║
║     - Exponentiation with right associativity            ║
║                                                          ║
║  5. ERROR HANDLING                                       ║
║     - Invalid mathematical expressions                   ║
║     - Incorrect bracket placement                        ║
║     - Division by zero                                   ║
║     - Invalid function names                             ║
║     - Mathematical domain errors                         ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  EXAMPLE CALCULATIONS                                    ║
║     5 + 3 * 2                 = 11                       ║
║     sqrt(25) + 5              = 10                       ║
║     2 ^ 3 ^ 2                 = 512                      ║
║     abs(-10) * 2              = 20                       ║
║     sind(30) + cosd(60)       = 1                        ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  COMMANDS                                                ║
║     menu    Display this menu                            ║
║     exit    Exit the calculator                          ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  NOTE                                                    ║
║     - Parentheses are required for functions.            ║
║     - Spaces around mathematical operators are optional. ║
║     - Trigonometric functions sin, cos and tan use       ║
║       radians; sind, cosd and tand use degrees.          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
def tokenize(expression):
    pattern = r'\d+\.?\d*|[a-zA-Z]+|[+\-*/%^()]'
    tokens = re.findall(pattern, expression)
    return tokens

def is_number(token) :
    try :
        float(token)
        return True
    except ValueError :
        return False
          

def validate_operators(tokens) :
    expecting = "number"
    bracket_count = 0

    for token in tokens :
        if is_number(token) :
            if expecting != "number" :
                print("Error! Number received when operator was expected")              
                return False
            expecting = "operator"
        elif token in operators :
            if token == "-" and expecting == "number":
                continue

            elif token in operators:
                if expecting != "operator":
                    print("Error! Operator received when number was expected")
                    return False

                expecting = "number"
        elif token in functions :
            if expecting != "number" :
                print("Error ! Wrong position of Expression ")
                return False
            expecting = "bracket"
        elif token == "(" :
            if expecting not in ("number" , "bracket") :
                print("Error ! Opening bracket in wrong position ")
                return False
            bracket_count += 1
            expecting = "number"
        elif token == ")" :
            if expecting != "operator":
                print("Error ! Closing bracket in wrong position")
                return False
            if bracket_count == 0 :
                print("Error ! missing opening brakets in expression ")
                return False
            bracket_count -= 1
            expecting = "operator"
        else:
            print(f"Invalid '{token}' Operator Entered")
            return False
    if expecting == "number" :
        print("Error ! Expression cannot end with an operator ")
        return False
    if bracket_count != 0:
        print("Error! Missing closing bracket")
        return False
    return True
        

def infix_to_postfix(tokens):
    output = []
    stack = []

    for i, token in enumerate(tokens):
        # check if token is a number
        if is_number(token):
            output.append(token)

        #opening braket 
        elif token == "(" :
            stack.append(token)

        elif token in functions:
            stack.append(token)

        #closing braket
        elif token == ")" :
            while stack and stack[-1] != "(" :
                output.append(stack.pop())
            stack.pop() 

            #for functions   
            if stack and stack[-1] in functions:
                output.append(stack.pop())

        # otherwise it is an operator
        else:
            if token == "-" and (i == 0 or tokens[i - 1] in operators or tokens[i - 1] == "(" ):
                token = "u-"

            while stack and stack[-1] in operators and (
                operators[stack[-1]] > operators[token] or
                (operators[stack[-1]] == operators[token] and token not in ("^", "u-"))
                ):
                output.append(stack.pop())

            stack.append(token)
                                     
    while stack :
        popped = stack.pop()
        output.append(popped)

    return output

def postfix_evaluation(postfix) :
    stack = []

    for exp in postfix :
        if is_number(exp) :
            stack.append(float(exp))
        elif exp in functions:
            value = stack.pop()

            if exp == "fact":
                if not value.is_integer():
                    raise ValueError("Factorial requires a whole number")

                if value < 0:
                    raise ValueError("Factorial cannot be negative")

                value = int(value)

            result = functions[exp](value)
            stack.append(result)
        else :
            if exp == "u-":
                stack.append(-stack.pop())
                continue
            b = stack.pop()
            a = stack.pop()
            if exp == "+" :
                stack.append(a+b)
            if exp == "-" :
                stack.append(a-b)
            if exp == "*" :
                stack.append(a*b)
            if exp == "/" :
                stack.append(a/b)
            if exp == "%" :
                stack.append(a%b)
            if exp == "^" :
                stack.append(a**b)
    return stack.pop() 

def main():
    calc_banner()

    while True:
        cmd_input = input("Calc >> ")
        if cmd_input.lower().strip() == "exit":
            print("Exiting Scientific calculator byiiii !")
            break
        if cmd_input.lower().strip() == "menu":
            menu()
            continue
        try :
            tokens = tokenize(cmd_input)

            if not validate_operators(tokens):
                continue

            postfix = infix_to_postfix(tokens)
            postfix_eval = postfix_evaluation(postfix)

            print("Answer : ",postfix_eval)

        except ZeroDivisionError:
            print("Error: Cannot divide by zero.")

        except IndexError:
            print("Error: Invalid / Incomplete expression")

        except KeyError:
            print("Error: Unknown operator") 
        
        except ValueError as e:
            print("Error:", e)
        
if __name__ == "__main__":
    main()
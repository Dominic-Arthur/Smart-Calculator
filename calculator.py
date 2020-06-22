from collections import deque
from string import ascii_letters
import re

variable_dict = {}  # used in the eval() function
numbers = [str(i) for i in range(1001)]
letters_words = ascii_letters


def get_operator(operator):
    """This function handles concatenated operators. Example: it convert '---' to '-' and '--+' to '+' """
    minus = operator.count("-")
    if minus % 2 != 0:
        return "-"
    else:
        return "+"


def infix_to_postfix(expression):
    """This function converts infix notation to postfix notation"""
    global numbers, letters_words
    operator_stack = deque()
    postfix = []
    operators = {
        '-': 1,
        '+': 1,
        '*': 2,
        '/': 2,
        '^': 3
    }  # dictionary values are in the oder of operator precedence from lowest to highest.
    for item in expression:
        if item in letters_words or item in numbers:
            postfix.append(item)
        elif item in operators:
            if not operator_stack or operator_stack[-1] == '(':  # checks if stack is empty or top
                operator_stack.append(item)  # item is left parenthesis
            elif operator_stack[-1] != '(' and operators[item] > operators[operator_stack[-1]]:
                operator_stack.append(item)
            elif operator_stack[-1] != '(' and operators[item] <= operators[operator_stack[-1]]:
                postfix.append(operator_stack.pop())
                while len(operator_stack):
                    if operator_stack[-1] != '(' and operators[item] <= operators[operator_stack[-1]]:
                        postfix.append(operator_stack.pop())
                    else:
                        break
                operator_stack.append(item)
        elif item == '(':
            operator_stack.append(item)
        elif item == ')':
            while len(operator_stack):
                top_item = operator_stack.pop()
                if top_item != '(':
                    postfix.append(top_item)
                else:
                    break
    while len(operator_stack):
        postfix.append(operator_stack.pop())

    if '(' not in postfix and ')' not in postfix:
        return postfix
    else:
        return None


def process_input_for_postfix_conversion(user_input):
    """This function process math expression for desired form for conversion to postfix"""
    pattern1 = re.compile(r'^\s*[-/+*]+|[/*]{2,10}|([-+]\s*[/*]{1,10})|[-/+*]+\s*$')
    if user_input.count('(') != user_input.count(')'):  # checks for number of left and right parenthesis
        return None
    elif pattern1.search(user_input):  # checks for in valid operator combinations
        return None
    else:
        pattern = re.compile(r'(\w+)|(\+*)|(\**)|(/*)|(-*)|(\()|(\))')
        match = pattern.split(user_input)
        expression = []
        for i in match:
            if i == '' or i is None:
                continue
            elif i.strip() == '':
                continue
            elif '-' in i or '+' in i:
                expression.append(get_operator(i))
            else:
                expression.append(i)
        return expression


def set_variables(user_input):
    """This function allow user to set variables to be used in calculations"""
    global variable_dict, letters_words
    statement = process_var_assignment_input(user_input)
    if statement is None:
        print('Invalid assigment')
    else:
        pattern = re.compile(r'^[0-9]*[a-zA-Z]*[0-9]')  # variable name cannot have digits
        if pattern.fullmatch(statement[0]):
            print('Invalid variable')
        elif statement[-1] == '=':
            print('Invalid assignment')
        elif statement[0] not in variable_dict:
            try:
                variable_dict[statement[0]] = int(statement[2])
                letters_words += statement[0]
            except ValueError:
                if statement[2] in variable_dict:
                    variable_dict[statement[0]] = variable_dict[statement[2]]
                    letters_words += statement[0]
                else:
                    print('Invalid assignment')
        elif statement[0] in variable_dict:
            try:
                variable_dict[statement[0]] = int(statement[2])
            except ValueError:
                if statement[2] in variable_dict:
                    variable_dict[statement[0]] = variable_dict[statement[2]]
                else:
                    print('Invalid assignment')


def process_var_assignment_input(user_input):
    """This function read and interprets user input and process it to desired output for further operations"""
    if user_input.count('=') > 1:
        return None
    else:
        tem_list = user_input.split('=')
        statement = [item.strip() for item in tem_list]
        statement.insert(1, '=')  # insert back the equal sign in the middle
        return statement  # this function particularly deals with spacing issues.


def get_value_for_input_variable(user_input):
    """It prints the value associated to an input variable name"""
    global variable_dict
    key = user_input.strip()  # removes white spaces.
    if key in variable_dict:
        return variable_dict[key]
    else:
        return 'Unknown variable'


def evaluate_postfix(user_input):
    """This function evaluates expression in postfix notation"""
    global numbers, letters_words
    if '=' in user_input:
        return 'Invalid expression'
    if process_input_for_postfix_conversion(user_input) is not None:
        input_list = process_input_for_postfix_conversion(user_input)
        postfix = infix_to_postfix(input_list)
        char_stack = deque()
        operators = ['/', '-', '+', '*']
        if postfix is not None:
            for item in postfix:
                if item in letters_words or item in numbers:
                    char_stack.append(item)
                elif item in operators:
                    top_item = char_stack.pop()
                    next_item = char_stack.pop()
                    temp_value = calculate(next_item, top_item, item)
                    if temp_value is None:  # checks if calculate() returns a number
                        return 'Unknown variable'
                    else:
                        char_stack.append(temp_value)
            return int(char_stack[0])
        else:
            return "Invalid expression"
    else:
        return "Invalid expression"


def calculate(num2, num1, sign):  # num1 for top item on stack
    """This function evaluates the arguments passed with the sign given"""
    global variable_dict
    try:
        result = eval(f'{num2}{sign}{num1}', variable_dict)  # built_in eval() function allow to work with strings
    except NameError:
        return None
    else:
        return result


def calculator():
    pattern1 = re.compile(r'\s*\w+\s*', re.A)  # matches a variable name.
    pattern2 = re.compile(r'\w+\s*[-/+*]+\s*\w+', re.A)  # matches a general mathematical expression
    pattern3 = re.compile(r'\s*\w+\s*=\s*\w+', re.A)  # matches a variable assignment statement
    pattern4 = re.compile(r'\s*[-+]*\d+', re.A)  # matches a number
    while True:
        user_input = input()
        if user_input.startswith("/"):
            if user_input == "/exit":
                print("Bye!")
                break
            elif user_input == "/help":
                print("""
The program can perform the following operations:
addition, subtraction, multiplication and division on both predefine variables and numbers
""")
            else:
                print("Unknown command")
        elif user_input.strip() == '':  # in the event user inputs nothing
            continue
        elif user_input.count('=') > 1:
            print('Invalid expression')
        elif pattern1.fullmatch(user_input):
            print(get_value_for_input_variable(user_input))
        elif pattern2.search(user_input):
            print(evaluate_postfix(user_input))
        elif pattern3.search(user_input):
            set_variables(user_input)
        elif pattern4.fullmatch(user_input):
            print(user_input)
        else:
            print('Invalid expression')

# calculator()

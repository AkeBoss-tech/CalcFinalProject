from sympy import Integral, sqrt, symbols, pprint, sin, cos, Derivative, log, E, ln, oo, Rational, tan, Sum, pi

from color import printf, inputf, randomColor

from sympy.concrete.summations import Sum
from time import sleep

x_var, n_var, C = symbols('x n C')
C = symbols('C', integer=True)

letters = ['a', 'b', 'c', 'd', 'e', 'f']

def pretty(text) -> None:
    #with open('debug.txt', 'w') as file:
    #    print(text, '\n', file=file) # DEBUG
    pprint(eval(text), mat_symbol_style='bold')

def in_derivative(text):
    return f'Derivative({text}, x_var)'

def in_integral(text, bounds=None):
    if bounds is None:
        return f"Integral({text}, x_var)"
    else:
        return f"Integral({text}, (x_var, {bounds[0]}, {bounds[1]}))"

def in_sum(text, bounds=(0, oo)):
    text = text.replace('x_var', 'n_var')
    return f"Sum({text}, (n_var, {bounds[0]}, {bounds[1]}))"

letters = 'abcdefghijklmnopqrstuvwxyz'
letters = [letter for letter in letters]
def getAnswer(start = 1, end = 4):
    while True:
        inp = input('> ').strip()
        if inp.isnumeric():
            if start <= int(inp) <= end:
                return int(inp)
        if inp.lower() == 'exit':
            return None
        
        if inp in letters:
            if start <= letters.index(inp) + 1 <= end:
                return int(letters.index(inp) + 1)
        print('answer not accepted')



def printDerivativeQuestion(equation, questions, question_num=''):
    printf(f'^R{question_num} What is ')
    pretty(in_derivative(equation.pprint))
    printf('*e')
    print()
    sleep(2)
    a = True
    b = {
        True: '^r',
        False: '^G'
    }
    # print(questions) DEBUG
    for i in range(len(questions)):
        printf(f'{b[a]}{letters[i]}.\n')
        pretty(questions[i].pprint)
        printf('^e\n')
        a = not a

def printSetUpQuestion(start, end, equation, choices, text, question_num=''):
    printf(f'^R{question_num} What is the {text} from {start} to {end} of this function?\n')
    pretty(equation.pprint)
    printf('*e')
    print()
    sleep(2)
    a = True
    b = {
        True: '^r',
        False: '^G'
    }
    # print(questions) DEBUG
    for i in range(len(choices)):
        printf(f'{b[a]}{letters[i]}.\n')
        pretty(choices[i])
        printf('^e\n')
        a = not a

def printConvergenceQuestion(series, question_num=''):
    printf(f'^R{question_num} Does this converge?')
    pretty(series.pprint)
    printf('*e')
    print()
    
    printf('^ra. Converges*e')
    printf('^Gb. Diverges*e')

def printIntegralQuestion(equation, questions, question_num=''):
    printf(f'^R{question_num} What is ')
    pretty(in_integral(equation.pprint))
    printf('*e')
    print()
    sleep(2)
    tracker = True
    things = {
        True: '^r',
        False: '^G'
    }
    for i in range(len(questions)):
        printf(f'{things[tracker]}{letters[i]}.\n')
        a = questions[i].pprint
        b = a.split('+')
        t = ''
        for item in b:
            if not isinstance(eval(item), Rational):
                t += f'{item} + '

        # print(t)

        pretty(t + 'C')
        printf('^e\n')
        tracker = not tracker
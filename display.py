from sympy import Integral, sqrt, symbols, pprint, sin, cos, Derivative, log, E, ln, oo, Rational, tan

from color import printf, inputf, randomColor

from sympy.concrete.summations import Sum

x_var, n_var, C = symbols('x n C')
C = symbols('C', integer=True)



def pretty(text) -> None:
    with open('debug.txt', 'w') as file:
        print(text, '\n', file=file) # DEBUG
    pprint(eval(text), mat_symbol_style='bold')

def in_derivative(text):
    return f'Derivative({text}, x_var)'

def in_integral(text, bounds=None):
    if bounds is None:
        return f"Integral({text}, x_var)"
    else:
        return f"Integral({text}, (x_var, {bounds[0]}, {bounds[1]}))"

letters = 'abcdefghijklmnopqrstuvwxyz'
letters = [letter for letter in letters]
def getAnswer(start = 1, end = 4):
    while True:
        inp = input('> ').strip()
        if inp.isnumeric():
            if start <= int(inp) <= end:
                return int(inp)
        if inp in letters:
            if start <= letters.index(inp) + 1 <= end:
                return int(letters.index(inp) + 1)
        print('answer not accepted')

def printDerivativeQuestion(equation, questions):
    printf('^RWhat is ')
    pretty(in_derivative(equation.pprint))
    printf('*e')
    print()
    a = True
    b = {
        True: '^r',
        False: '^G'
    }
    # print(questions) DEBUG
    for i in range(len(questions)):
        printf(f'{b[a]}{i+1}.\n')
        pretty(questions[i].pprint)
        printf('^e\n')
        a = not a

def printConvergenceQuestion(series):
    printf('^RDoes this converge?')
    pretty(series.pprint)
    printf('*e')
    print()
    
    printf('^r1. Converges*e')
    printf('^G2. Diverges*e')

def printIntegralQuestion(equation, questions):
    printf('^RWhat is ')
    pretty(in_integral(equation.pprint))
    printf('*e')
    print()
    a = True
    b = {
        True: '^r',
        False: '^G'
    }
    for i in range(len(questions)):
        printf(f'{b[a]}{i+1}.\n')
        pretty(questions[i].pprint + ' + C')
        printf('^e\n')
        a = not a
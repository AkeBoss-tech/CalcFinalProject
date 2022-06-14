print('Getting Imports ...')
from calculus import *
from display import *
from generate import *

from util import yesOrNo

# a = Addition([Multiply([Constant(2), Polynomial(3), Polynomial(5)]), Multiply([Constant(-3), Polynomial(1), Polynomial(-2)])])
from sympy import init_printing
from random import choice
print('Done')

generateIntegralTest()
print('Initializing printer ...')
init_printing()
print('Done')

"""
a = Divide(Sin(), Polynomial(1))

from sympy import Integral, sqrt, symbols, pprint, sin, cos, Derivative, log, E
x_var, e, __ = symbols('x e z')

print(a.pprint)
pprint(eval(a.pprint))
b = a.derivative
pprint(eval(b.pprint))

print('\n'*8)

random = generateRandomPowerRule()

pprint(eval(in_derivative(random.pprint)))
pprint(eval(random.derivative.pprint))
print()
print()
print('Hello ')
pretty(in_integral(random.pprint))
print('Hello ', sep='', end='')
pretty(random.integral.pprint)"""


print('Question loop')
while True:
    questions = {
        'Derivative': [# generateRandomPowerRule, generateRandomConstantRule,  generateRandomCompositeRule, generateLinearExpression, generateRandomAdditionRule, generateRandomTrig, generateRandomLN
        generateQuotientRule, generateRandomExponential,],
        'Integral': [# generateRandomConstantRule, generateRandomPowerRule, 
        generateRandomCompositeRule,generateRandomExponential, # generateLinearExpression, 
        # generateRandomTrig
        ],
        #'Series': [generatePSeries, generateGeoSeries]
    }
    
    a = choice(list(questions.keys()))
    random = choice(questions[a])
    print(random)
    choices, answer = None, None
    if a == 'Derivative':
        t = random()
        choices, answer = generateDerivativeQuestion(t)
        printDerivativeQuestion(t, choices)
    elif a == 'Integral':
        choices, answer = None, None
        if random == generateRandomCompositeRule:
            special = 'Composite'
            equation = [0,0]
            while equation[1] == 0:
                t = random()
                if not isinstance(t, Composite):
                    special = False
                    equation = t.derivative
                    break

                equation = [t, t.derivative]
            
            choices, answer = generateIntegralQuestion(equation, special=special)
            random = t.derivative
            t = t.derivative
        else:
            t = random()
            choices, answer = generateIntegralQuestion(t)
        printIntegralQuestion(t, choices)
    elif a == 'Series':
        sum = random()
        answer = 0 if sum.convergence else 1
        printConvergenceQuestion(sum)
        
    u_answer = getAnswer()
    if u_answer == answer + 1:
        print('You got it right!')
    else:
        print('Wrong')
    print('\n')
    
    print(f'The answer was {answer + 1}')
    if not yesOrNo('Continue?'):
        break

# pprint(Integral(x_var, x_var))
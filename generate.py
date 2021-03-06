from random import randint, shuffle, choice as chooser
from calculus import Constant, Divide, Polynomial, Multiply, P_Series, Geometric_Series, Addition, Exponential, Sin, Cos, Tan, LN, Composite, e_to_the_x
from display import in_integral, pretty, in_sum
from sympy import *

# TODO Add PDF converter
# TODO add average value of a function

def generateRandomPowerRule():
    constant = 0
    while constant == 0:
        constant = randint(-5, 10)

    constant = Constant(constant)

    power = 0
    while power == 0:
        power = randint(-5, 10)

    power = Polynomial(power)

    function = Multiply([constant, power])
    return function

def generateRandomTrig():
    trig = [Sin, Cos, Tan]
    constant = 0
    while constant == 0:
        constant = randint(-5, 5)
    choice = chooser(trig)()
    return Multiply([Constant(constant), choice])

def generateRandomLN():
    constant = 0
    while constant == 0:
        constant = randint(-5, 5)
    choice = LN()
    return Multiply([Constant(constant), choice])

def generateRandomConstantRule():
    constant = 0
    while constant == 0:
        constant = randint(-100, 100)

    constant = Constant(constant)
    
    return constant

def generateDerivativeQuestion(equation):
    answer = equation.derivative
    incorrect = [equation.w_derivative_1(), equation.w_derivative_2(), equation.w_derivative_3()]
    answers = incorrect + [answer]

    r_positions = [0,1,2,3]
    shuffle(r_positions)
    r_answers = [answers[i] for i in r_positions]

    # return answers and position of correct answer
    return r_answers, r_positions.index(3)

def generateIntegralQuestion(equation, special=False):
    # equation is different if it is composite
    # list of function and derivative
    # [og function, derivative]
    answer, incorrect = None, None
    if special == 'Composite':
        if isinstance(equation[0], Addition):
            funcs = []
            for func in equation[0].functions:
                if not isinstance(func, Constant):
                    funcs.append(func)
            equation[0] = Addition(funcs)
        answer = equation[0]
        incorrect = [equation[0].f, answer.derivative, Multiply([equation[0].f, equation[0].g.derivative])]
    else:
        answer = equation.integral
        incorrect = [equation.w_integral_1(), equation.w_integral_2(), equation.w_integral_3()]
    answers = incorrect + [answer]

    r_positions = [0,1,2,3]
    shuffle(r_positions)
    r_answers = [answers[i] for i in r_positions]

    # return answers and position of correct answer
    return r_answers, r_positions.index(3)

def generateSetUpQuestion(answers):
    # right answer first and the rest after
    r_positions = [0,1,2,3]
    shuffle(r_positions)
    r_answers = [answers[i] for i in r_positions]

    # return answers and position of correct answer
    return r_answers, r_positions.index(0)

def generateFraction(add=2):
    denom = randint(2, 6)
    num = randint(1, denom+add)
    sign = chooser(['-', ''])
    return f'{sign}{num}/{denom}'

def generatePSeries():
    if chooser([True, False]):
        num = randint(-5, 5)
    else:
        num = generateFraction(-1)

    n = Constant(num)
    return P_Series(n)

def generateGeoSeries():
    num = generateFraction(6)

    n = Constant(num)
    return Geometric_Series(n)
    
def generateLinearExpression():
    constant = randint(-5, 5)
    coeff = randint(1, 5)
    return Addition([Multiply([Constant(coeff), Polynomial(1)]), Constant(constant)])



def generateRandomCompositeRule():
    funcs = [
        Polynomial,
        Exponential,
        Sin,
        Cos,
        LN,
        generateLinearExpression,
    ]

    a = chooser(funcs)
    chosen = False
    if a == Polynomial:
        num = 0
        while num == 0:
            num = randint(-10, 10)
        a = a(num)
    elif a == Exponential:
        if chooser([True, False]):
            a = a('e')
        else:
            num = 0
            while num == 0:
                num = randint(1, 3)
            a = a(num)
        
    elif a == generateLinearExpression:
        a = a()
        chosen = True
    else:
        a = a()
    
    b = chooser(funcs)
    
    
    if b == Polynomial:
        num = 0
        while num == 0:
            num = randint(-10, 10)
        b = b(num)
    elif b == Exponential:
        if chooser([True, False]):
            b = b('e')
        else:
            num = 0
            while num == 0:
                num = randint(1, 3)
            b = b(num)
    elif b == generateLinearExpression and not chosen:
        b = b()
    else:
        b = b()
    
    if chosen:
        return a.replace(b) 
    
    if chooser([True, True, False]):
        return Composite(a, b)
        

    c = chooser(funcs)
    if c == Polynomial:
        num = 0
        while num == 0:
            num = randint(-10, 10)
        c = c(num)
    elif c == Exponential:
        if chooser([True, False]):
            c = c('e')
        else:
            num = 0
            while num == 0:
                num = randint(1, 3)
            c = c(num)

    elif c == generateLinearExpression and chosen:
        if chooser([True, False]):
            c = c('e')
        else:
            num = 0
            while num == 0:
                num = randint(1, 3)
            c = c(num)
    
    else:
        c = c()


    return Composite(c, Composite(a, b))

def generateRandomAdditionRule():
    length = randint(2, 4)
    types = [generateRandomPowerRule, generateRandomConstantRule, Sin, LN, Cos, e_to_the_x]
    problems = []
    for i in range(length):
        problems.append(chooser(types)())

    return Addition(problems)

deriv_funcs = [generateRandomPowerRule, generateLinearExpression, generateRandomAdditionRule, generateRandomTrig, generateRandomLN]
def generateQuotientRule():
    deriv_funcs = [generateRandomPowerRule, generateLinearExpression, generateRandomTrig, generateRandomLN, generateRandomExponential]
    a = deriv_funcs
    numerator = chooser(a)
    a.remove(numerator)
    numerator = numerator()
    denominator = chooser(a)()
    return Divide(numerator, denominator)

def generateRandomExponential():
    if chooser([True, False, False, False]):
        return Exponential('e')
    
    frac = randint(2, 10)
    
    return Exponential(frac)

def generateArcLength():
    start = randint(2, 10)
    end = start + randint(2, 7)
    equation = chooser(deriv_funcs)()
    return equation, start, end

def generateVolume():
    start = randint(2, 10)
    end = start + randint(2, 7)
    equation = chooser(deriv_funcs)()
    return equation, start, end

def generateAverageValue():
    start = randint(2, 10)
    end = start + randint(2, 7)
    equation = chooser(deriv_funcs)()
    return equation, start, end

int_funcs = [generateRandomPowerRule, generateRandomCompositeRule, generateLinearExpression, generateRandomTrig]

x_var, n_var, C = symbols('x n C')
C = symbols('C', integer=True)

def generateIntegralTest():
    start = randint(0, 5)
    end = oo
    equation = chooser(int_funcs)()
    # return equation
    print('What is the convergence of')
    summ = in_sum(equation.pprint, (start, end))
    pretty(summ)
    
    result = eval(f'({summ}).doit()')
    print(result)
    print('Converges' if result != oo else 'Diverges')


from display import *
from generate import *


class Question:
    def __init__(self) -> None:
        self.name = 'name'
        self.type = 'type'
        self.generator = lambda x: x

    def getUserAnswer(self):
        u_answer = getAnswer()
        if u_answer == self.answer + 1:
            a = True
        else:
            a = False
        # correct or not, user answer, correct answer, question
        return a, u_answer, self.answer + 1, self
    
    def generateQuestion(self):
        if self.type == 'Derivative':
            self.equation = self.generator()
            self.choices, self.answer = generateDerivativeQuestion(self.equation)
        elif self.type == 'Integral':
            self.equation = self.generator()
            self.choices, self.answer = generateIntegralQuestion(self.equation)
        elif self.type == 'Series':
            self.series = self.generator()
            self.answer = 0 if sum.convergence else 1
        return None

    def askQuestion(self):
        if self.type == 'Derivative':
            printDerivativeQuestion(self.equation, self.choices)
        elif self.type == 'Integral':
            printIntegralQuestion(self.equation, self.choices)
        elif self.type == 'Series':
            printConvergenceQuestion(self.sum)   
        pass

class PowerRuleDerivativeQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Power Rule'
        self.type = 'Derivative'
        self.generator = generateRandomPowerRule

class ConstantDerivativeQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Constant'
        self.type = 'Derivative'
        self.generator = generateRandomConstantRule

class CompositeDerivativeQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Composite'
        self.type = 'Derivative'
        self.generator = generateRandomCompositeRule

class LinearDerivativeQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Linear Expression'
        self.type = 'Derivative'
        self.generator = generateLinearExpression

class AdditionDerivativeQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Addition'
        self.type = 'Derivative'
        self.generator = generateRandomAdditionRule

class TrigDerivativeQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Trignometry'
        self.type = 'Derivative'
        self.generator = generateRandomTrig

class ExponentialDerivativeQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Exponential'
        self.type = 'Derivative'
        self.generator = generateRandomExponential

class NaturalLogDerivativeQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Natural Log'
        self.type = 'Derivative'
        self.generator = generateRandomLN

# Integrals
class CompositeIntegralQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Composite'
        self.type = 'Integral'
        self.generator = generateRandomCompositeRule
    
    def generateQuestion(self):
        equation = [0,0]
        while equation[1] == 0:
            t = self.generator()
            equation = [t, t.derivative]
        
        self.choices, self.answer = generateIntegralQuestion(equation, special='Composite')
        self.answer = t.derivative

    def askQuestion(self):
        printIntegralQuestion(self.equation, self.choices)

class TrigIntegralQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Trignometry'
        self.type = 'Integral'
        self.generator = generateRandomTrig

class PowerRuleIntegralQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Power Rule'
        self.type = 'Integral'
        self.generator = generateRandomPowerRule

class ExponentialIntegralQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Exponential'
        self.type = 'Integral'
        self.generator = generateRandomExponential

class ConstantIntegralQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Constant'
        self.type = 'Integral'
        self.generator = generateRandomConstantRule

class CompositeIntegralQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Composite'
        self.type = 'Integral'
        self.generator = generateRandomCompositeRule

class LinearIntegralQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Linear Expression'
        self.type = 'Integral'
        self.generator = generateLinearExpression

class PSeriesQuestion(Question):
    def __init__(self) -> None:
        self.name = 'P-Series'
        self.type = 'Series'
        self.generator = generatePSeries

class GeometricSeriesQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Geometric Series'
        self.type = 'Series'
        self.generator = generateGeoSeries
    
class IntegralTestQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Integral Test'
        self.type = 'Series'
        self.generator = generatePSeries


class ArcLengthQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Arc Length'
        self.type = 'Set up but do not solve'
        self.generator = generateArcLength

    def c_answer(self):
        return in_integral(f'sqrt(({self.equation.derivative.pprint})**2 + 1)', bounds=(self.start, self.end))

    def w_answer_1(self):
        return in_integral(f'sqrt(({self.equation.pprint})**2 + 1)', bounds=(self.start, self.end))

    def w_answer_2(self):
        return in_integral(f'sqrt({self.equation.derivative.pprint})', bounds=(self.start, self.end))

    def w_answer_3(self):
        return in_integral(f'({self.equation.derivative.pprint})**2', bounds=(self.start, self.end))

    def generateQuestion(self):
        self.equation, self.start, self.end = self.generator()
        self.shuffled_answers, self.answer = generateSetUpQuestion([
            self.c_answer(),
            self.w_answer_1(),
            self.w_answer_2(),
            self.w_answer_3()
        ])

    def askQuestion(self):
        printSetUpQuestion(self.start, self.end, self.equation, self.shuffled_answers, 'arc length')

class VolumeQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Volume Disk Method'
        self.type = 'Set up but do not solve'
        self.generator = generateVolume

    def c_answer(self):
        return "Rational('pi') * " + in_integral(f'({self.equation.pprint})**2', bounds=(self.start, self.end))

    def w_answer_1(self):
        return in_integral(f'({self.equation.pprint})**2', bounds=(self.start, self.end))

    def w_answer_2(self):
        return "Rational('pi') * " + in_integral(f'({self.equation.pprint})', bounds=(self.start, self.end))

    def w_answer_3(self):
        return "Rational('pi') * " + in_integral(f'({self.equation.pprint})**2 + {self.equation.pprint}', bounds=(self.start, self.end))

    def generateQuestion(self):
        self.equation, self.start, self.end = self.generator()
        self.shuffled_answers, self.answer = generateSetUpQuestion([
            self.c_answer(),
            self.w_answer_1(),
            self.w_answer_2(),
            self.w_answer_3()
        ])

    def askQuestion(self):
        printSetUpQuestion(self.start, self.end, self.equation, self.shuffled_answers, 'volume revolved around the x-axis')

class AreaQuestion(Question):
    def __init__(self) -> None:
        self.name = 'Area Under Curve'
        self.type = 'Set up but do not solve'
        self.generator = generateVolume

    def c_answer(self):
        return in_integral(f'{self.equation.pprint}', bounds=(self.start, self.end))

    def w_answer_1(self):
        return in_integral(f'({self.equation.pprint})**2', bounds=(self.start, self.end))

    def w_answer_2(self):
        return "Rational('pi') * " + in_integral(f'({self.equation.pprint})', bounds=(self.start, self.end))

    def w_answer_3(self):
        return in_integral(f'({self.equation.pprint})**2 + {self.equation.pprint} + 1', bounds=(self.start, self.end))

    def generateQuestion(self):
        self.equation, self.start, self.end = self.generator()
        self.shuffled_answers, self.answer = generateSetUpQuestion([
            self.c_answer(),
            self.w_answer_1(),
            self.w_answer_2(),
            self.w_answer_3()
        ])

    def askQuestion(self):
        printSetUpQuestion(self.start, self.end, self.equation, self.shuffled_answers, 'area under the curve')

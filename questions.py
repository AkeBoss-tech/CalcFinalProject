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
    

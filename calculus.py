import math
from random import randint, shuffle, choice as chooser
from copy import deepcopy

# Base Class
class Function:
    def __init__(self, func):
        self.func = func
    
    def evaluate(self, x):
        return self.func(x)

    @property
    def derivative(self):
        pass

    @property
    def integral(self):
        pass

    def simplify(self):
        pass

# Operations
class Addition:
    def __init__(self, functions):
        # a list
        self.functions = functions
        self.simplify()
        if len(self.functions) == 1:
            func = self.functions[0]
            self.__dict__ = func.__dict__
            self.__class__ = func.__class__
            return

        for function in self.functions:
            if isinstance(function, Addition):
                self.functions.remove(function)
                self.functions.extend(function.functions)

    def simplify(self):
        # remove zero
        a = self.functions
        b = []
        
        for func in a:
            if not func == Constant(0):
                b.append(func)
                
        self.functions = b

    def evaluate(self, x):
        summ = 0
        for function in self.functions:
            summ += function.evaluate(x)

        return summ

    # replace Polynomial(1) with another function for composite functions
    def replace(self, function):
        functions = []
        for func in self.functions:
            if isinstance(func, Polynomial) and function.num == 1:
                functions.append(function)
            elif isinstance(func, Multiply):
                functions.append(func.replace(function))
            else:
                functions.append(func)

        return Addition(functions)

    @property
    def derivative(self):
        derivatives = []
        for function in self.functions:
            derivatives.append(function.derivative)
        return Addition(derivatives)

    @property
    def integral(self):
        integrals = []
        for function in self.functions:
            integrals.append(function.integral)
        return Addition(integrals)


    def w_derivative_1(self):
        derivatives = []
        for function in self.functions[:-1]:
            derivatives.append(function.derivative)
        return Addition(derivatives)

    def w_derivative_2(self):
        derivatives = []
        for function in self.functions:
            derivatives.append(Multiply([function.derivative, function]))
        return Addition(derivatives)

    def w_derivative_3(self):
        derivatives = []
        i = 2
        for function in self.functions:
            derivatives.append(Multiply([function.derivative, Constant(i)]))
            i += 1
        return Addition(derivatives)

    def w_integral_1(self):
        return self

    def w_integral_2(self):
        return self.derivative

    def w_integral_3(self):
        integrals = []
        i = 2
        for function in self.functions:
            integrals.append(Multiply([function.integral, Constant(i)]))
            i += 1
        return Addition(integrals)
    
    def __repr__(self):
        a = ''
        for func in self.functions[:-1]:
            a += str(func.__repr__())
            a += " + "
        a += str(self.functions[-1].__repr__())
        return a

    @property
    def pprint(self):
        a = ''
        for func in self.functions[:-1]:
            a += str(func.pprint)
            a += " + "
        a += str(self.functions[-1].pprint)
        return a

class Multiply:
    def __init__(self, functions):
        # a list
        # check if there is a zero
        
        for function in functions:
            if isinstance(function, Constant) and function == Constant(0):
                zero = Constant(0)
                self.__dict__ = zero.__dict__
                self.__class__ = zero.__class__
                return
            if isinstance(function, Multiply):
                functions.remove(function)
                functions.extend(function.functions)
        else:
            self.functions = functions

        self.cons = None
        self.poly = None
        self.other = None
        for function in functions:
            if isinstance(function, Constant):
                self.cons = function
            

            elif isinstance(function, Polynomial):
                self.poly = function
            else:
                self.other = function

            if self.cons != None and self.poly != None:
                break

        self.simplify()
        if len(self.functions) == 1:
            func = self.functions[0]
            self.__dict__ = func.__dict__
            self.__class__ = func.__class__
        elif len(self.functions) == 0:
            func = Constant(1)
            self.__dict__ = func.__dict__
            self.__class__ = func.__class__

    def simplify(self):
        # combine constants
        a = self.functions
        b = []
        constant = 1
        for func in a:
            if isinstance(func, Constant):
                constant = constant * func.num
            else:
                b.append(func)
        if constant != 1:
            b.append(Constant(constant))
            self.constant = b[-1]
        else:
            self.constant = Constant(1)
        self.functions = b
        
        # combine powers
        a = self.functions
        b = []
        powers = 0
        for func in a:
            if isinstance(func, Polynomial):
                powers = powers + func.power
            else:
                b.append(func)
        if powers != 0:
            self.poly = Polynomial(powers)
            b.append(Polynomial(powers))
        self.functions = b

        self.not_constant = deepcopy(self.functions)
        for thing in self.not_constant:
            if isinstance(thing, Constant):
                self.not_constant.remove(thing)
                break

    def replace(self, function):
        functions = []
        for func in self.functions:
            if isinstance(func, Polynomial) and func.power == 1:
                functions.append(function)
            elif isinstance(func, Addition):
                functions.append(func.replace(function))
            else:
                functions.append(func)
            
        return Multiply(functions)

    def evaluate(self, x):
        product = 1
        for function in self.functions:
            product *= function.evaluate(x)

        return product

    @property
    def derivative(self):
        derivatives = []
        for i in range(len(self.functions)):
            l = []
            a = self.functions[i].derivative
            l.append(a)
            for func in self.functions[:i] + self.functions[i+1:]:
                l.append(func)
            derivatives.append(Multiply(l))
        return Addition(derivatives)

    
    def w_derivative_1(self):
        if len(self.functions) == 2 and not  self.cons is None and not self.poly is None:
            
            return Multiply([self.cons, self.poly.w_derivative_1()])
        else:
            derivatives = []
            for i in range(len(self.functions)):
                l = []
                a = self.functions[i].w_derivative_1()
                l.append(a)
                for func in self.functions[:i] + self.functions[i+1:]:
                    l.append(func)
                derivatives.append(Multiply(l))
            return Addition(derivatives)

    def w_integral_1(self):
        if len(self.functions) == 2 and not self.cons is None and not self.poly is None:
            
            return Multiply([self.cons, self.poly.w_integral_1()])
        elif len(self.functions) == 2 and not self.cons is None:
            return Multiply([self.cons, self.other.w_integral_1()])
            

    def w_integral_2(self):
        if len(self.functions) == 2 and not  self.cons is None and not self.poly is None:
            
            return Multiply([self.cons, self.poly.w_integral_2()])
        elif len(self.functions) == 2 and not self.cons is None:
            return Multiply([self.cons, self.other.w_integral_2()])

    def w_integral_3(self):
        if len(self.functions) == 2 and not  self.cons is None and not self.poly is None:
            
            return Multiply([self.cons, self.poly.w_integral_3()])
        elif len(self.functions) == 2 and not self.cons is None:
            return Multiply([self.cons, self.other.w_integral_3()])

    
    def w_derivative_2(self):
        if len(self.functions) == 2 and self.cons != None and self.poly != None:
            
            return Multiply([self.cons, self.poly.w_derivative_2()])
        else:
            derivatives = []
            for i in range(len(self.functions)):
                l = []
                a = self.functions[i].w_derivative_2()
                l.append(a)
                for func in self.functions[:i] + self.functions[i+1:]:
                    l.append(func)
                derivatives.append(Multiply(l))
            return Addition(derivatives)

    
    def w_derivative_3(self):
        if len(self.functions) == 2 and self.cons != None and self.poly != None:
            
            return Multiply([self.cons, self.poly.w_derivative_3()])
        else:
            derivatives = []
            for i in range(len(self.functions)):
                l = []
                a = self.functions[i].w_derivative_3()
                l.append(a)
                for func in self.functions[:i] + self.functions[i+1:]:
                    l.append(func)
                derivatives.append(Multiply(l))
            return Addition(derivatives)

    @property
    def integral(self):
        # maybe impossible TODO
        if len(self.not_constant) == 1:
            return Multiply([self.constant, self.not_constant[0].integral])
        return False

    def __repr__(self):
        a = ''
        for func in self.functions[:-1]:
            a += str(func.__repr__())
            a += " * "
        a += str(self.functions[-1].__repr__())
        return a

    @property
    def pprint(self):
        a = ''
        for func in self.functions[:-1]:
            a += str(func.pprint)
            a += " * "
        a += str(self.functions[-1].pprint)
        return a          

class Divide:
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def evaluate(self, x):
        quotient = self.numerator(x) / self.denominator(x)

        return quotient

    @property
    def derivative(self):
        # lo di hi minus hi di lo over lo lo
        ldh = Multiply([self.denominator, self.numerator.derivative])
        hdl = Multiply([Constant(-1), self.denominator.derivative, self.numerator])
        numerator = Addition([ldh, hdl])
        denominator = Composite(Polynomial(2), self.denominator)
        return Divide(numerator, denominator)

    # TODO w_derivative_1
    def w_derivative_1(self):
        ldh = Multiply([self.denominator.derivative, self.numerator])
        hdl = Multiply([Constant(-1), self.denominator, self.numerator.derivative])
        numerator = Addition([ldh, hdl])
        denominator = Composite(Polynomial(2), self.denominator)
        return Divide(numerator, denominator)

    def w_derivative_2(self):
        ldh = Multiply([self.denominator, self.numerator.derivative])
        hdl = Multiply([self.denominator.derivative, self.numerator])
        numerator = Addition([ldh, hdl])
        denominator = Composite(Polynomial(2), self.denominator)
        return Divide(numerator, denominator)

    def w_derivative_3(self):
        return Divide(self.numerator.derivative, self.denominator.derivative)

    def integrals(self):
        # maybe impossible TODO
        return False

    def __repr__(self):
        return '(' + str(self.numerator.__repr__()) + ')' + " / " + str(self.denominator.__repr__())

    @property
    def pprint(self):
        return '(' + str(self.numerator.pprint) + ')' + " / (" + str(self.denominator.pprint) + ")"

class Composite:
    def __init__(self, f, g):
        # f(g(x))
        self.f = f
        self.g = g

        if isinstance(self.f, Constant):
            zero = Constant(self.f.num)
            self.__dict__ = zero.__dict__
            self.__class__ = zero.__class__
            return
        
        if isinstance(self.g, Constant):
            zero = Constant(self.__repr__())
            self.__dict__ = zero.__dict__
            self.__class__ = zero.__class__
            return

        if isinstance(f, Polynomial) and isinstance(g, Polynomial):
            power = f.power * g.power
            poly = Polynomial(power)
            self.__dict__ = poly.__dict__
            self.__class__ = poly.__class__

    def evaluate(self, x):
        return self.f(self.g(x))

    @property
    def derivative(self):
        return Multiply([Composite(self.f.derivative, self.g), self.g.derivative])

    def __repr__(self):
        b = str(self.f.__repr__())
        b = b.replace('x', str(self.g.__repr__()))
        return b

    def w_derivative_1(self):
        return Multiply([Composite(self.f.w_derivative_1(), self.g), self.g.derivative])

    def w_integral_1(self):
        return self

    def w_integral_2(self):
        return Constant(2)

    def w_integral_3(self):
        return Constant(- 1) 
    
    def w_derivative_2(self):
        return Composite(self.f.derivative, self.g.derivative)
    
    def w_derivative_3(self):
        return Multiply([Composite(self.f.derivative, self.g), self.g.w_derivative_1()])

    @property
    def pprint(self):
        b = str(self.f.pprint)
        b = b.replace('x_var', str(self.g.pprint))
        return b

# Basic Stuff
class Constant(Function):
    def __init__(self, num):
        self.num = num
        if self.num == 'log(e)':
            self.num = 1
        elif self.num == '':
            self.num = 1
    
    def evaluate(self, x=0):
        return eval(str(self.num))

    @property
    def derivative(self):
        return Constant(0)

    
    def w_derivative_1(self):
        return self

    def w_integral_1(self):
        return self

    def w_integral_2(self):
        if self.num != 1:
            return Polynomial(self.num)
        return Constant(self.num + 1)

    def w_integral_3(self):
        return Constant(self.num - 1) 
    
    def w_derivative_2(self):
        return Multiply([Constant(self.num), Polynomial(1)])

    
    def w_derivative_3(self):
        return Multiply([self, Constant(-1)])

    @property
    def integral(self):
        return Multiply([Constant(self.num), Polynomial(1)])

    def simplify(self):
        return self

    def __eq__(self, other):
        if isinstance(other, Constant) and self.num == other.num:
            return True
        return False
    
    def __multi__(self, other):
        pass

    def __div__(self, other):
        pass

    def __repr__(self):
        return str(self.num)

    @property
    def pprint(self):
        if isinstance(self.num, str) and 'log' in self.num:
            return self.num
        elif isinstance(self.num, str) and self.num == 'e':
            return 'E'
        return f"Rational('{self.num}')"
              
class Polynomial(Function):
    def __init__(self, power):
        self.power = power

        constant = Constant(1)
        if self.power == 0:
            self.__class__ = constant.__class__
            self.__dict__ = constant.__dict__
    
    def evaluate(self, x):
        return x ** self.power

    @property
    def derivative(self):
        
        return Multiply([Constant(self.power), Polynomial(self.power - 1)])

    
    def w_derivative_1(self):
        return Multiply([Constant(self.power - 2), Polynomial(self.power - 1)])

    def w_integral_1(self):
        return Multiply([Constant(self.power), Polynomial(self.power - 1)])
 
    def w_derivative_2(self):
        return Polynomial(self.power - 1)

    def w_integral_2(self):
        return Divide(Polynomial(self.power), Constant(self.power + 1))

    def w_integral_3(self):
        if self.power != -1:
            return LN()
        return Divide(Polynomial(self.power+1), Constant(self.power + 2))
    
    def w_derivative_3(self):
        if self.power == -1:
            return LN()
        return Divide(Polynomial(self.power + 1), Constant(self.power + 1))

    @property
    def integral(self):
        if self.power == -1:
            return LN()
        return Divide(Polynomial(self.power + 1), Constant(self.power + 1))

    def simplify(self):
        return self

    def __sub__(self, other):
        pass
    
    def __multi__(self, other):
        pass

    def __div__(self, other):
        pass

    def __repr__(self):
        if self.power == 1:
            return 'x'
        return f'x^{self.power}'

    @property
    def pprint(self):
        return f'(x_var)**{self.power}'

# Series
class P_Series:
    def __init__(self, power):
        self.power = power

    @property
    def convergence(self) -> bool:
        if self.power.evaluate() < -1:
            return True
        return False

    def __repr__(self):
        return f'1/x^{self.power.num}'
    
    @property
    def pprint(self):
        return f'Sum(n_var**({self.power.pprint}), (n_var, 1, oo))'

class Geometric_Series:
    def __init__(self, base):
        self.base = base

    @property
    def convergence(self) -> bool:
        if -1 < self.base.evaluate() < 1:
            return True
        return False

    def __repr__(self):
        return f'{self.base.num}^n'

    @property
    def pprint(self):
        return f'Sum(({self.base.pprint})**n_var, (n_var, 1, oo))'

# Trig 
class Sin(Function):
    def __init__(self):
        pass
    
    def evaluate(self, x):
        return math.sin(x)

    @property
    def derivative(self):
        return Cos()

    def w_derivative_1(self):
        return self

    def w_derivative_2(self):
        return Multiply([Constant(-1), Cos()])

    def w_derivative_3(self):
        return Multiply([Constant(-1), Sin()])

    @property
    def integral(self):
        return Multiply([Constant(-1), Cos()])

    def w_integral_1(self):
        return self

    def w_integral_2(self):
        return Cos()

    def w_integral_3(self):
        return Multiply([Constant(-1), Sin()])

    def simplify(self):
        return self

    def __sub__(self, other):
        pass
    
    def __multi__(self, other):
        pass

    def __div__(self, other):
        pass

    def __repr__(self):
        return f'sin(x)'

    @property
    def pprint(self):
        return f'sin(x_var)'

class Cos(Function):
    def __init__(self):
        pass
    
    def evaluate(self, x):
        return math.cos(x)

    @property
    def derivative(self):        
        return Multiply([Constant(-1), Sin()])

    @property
    def integral(self):
        return Sin()

    def w_derivative_1(self):
        return self

    def w_derivative_2(self):
        return Multiply([Constant(-1), Cos()])

    def w_derivative_3(self):
        return Multiply([Constant(-1), Sin()])

    def w_integral_1(self):
        return self

    def w_integral_2(self):
        return Cos()

    def w_integral_3(self):
        return Multiply([Constant(-1), Sin()])

    def simplify(self):
        return self

    def __sub__(self, other):
        pass
    
    def __multi__(self, other):
        pass

    def __div__(self, other):
        pass

    def __repr__(self):
        return f'cos(x)'

    @property
    def pprint(self):
        return f'cos(x_var)'

class Tan(Function):
    def __init__(self):
        pass
    
    def evaluate(self, x):
        return math.tan(x)

    @property
    def derivative(self):        
        return Composite(Polynomial(-2), Cos())

    @property
    def integral(self):
        return Composite(LN(), Cos())

    def w_derivative_1(self):
        return Divide(Cos(), Sin())

    def w_derivative_2(self):
        return Divide(Cos(), Multiply([Constant(-1), Sin()]))

    def w_derivative_3(self):
        return Composite(Polynomial(-2), Sin())

    def w_integral_1(self):
        return Composite(LN(), Sin())

    def w_integral_2(self):
        return Cos()

    def w_integral_3(self):
        return Divide(Cos(), Sin())

    def simplify(self):
        return self

    def __sub__(self, other):
        pass
    
    def __multi__(self, other):
        pass

    def __div__(self, other):
        pass

    def __repr__(self):
        return f'tan(x)'

    @property
    def pprint(self):
        return f'tan(x_var)'

# Exponents and Logs
class LN(Function):
    def __init__(self):
        pass
    
    def evaluate(self, x):
        return math.ln(x)

    @property
    def derivative(self):
        return Polynomial(-1)

    @property
    def integral(self):
        return Addition([Multiply([Polynomial(1), LN()]), Multiply([Constant(-1), Polynomial(1)])])

    def w_derivative_1(self):
        return self

    def w_derivative_2(self):
        return Multiply([Constant(-1), Polynomial(-1)])

    def w_derivative_3(self):
        return Addition([Multiply([Polynomial(1), LN()]), Multiply([Constant(-1), Polynomial(1)])])

    def w_integral_1(self):
        return self

    def w_integral_2(self):
        return Polynomial(-1)

    def w_integral_3(self):
        return Multiply([Constant(-1), Polynomial(-1)])
    
    def simplify(self):
        return self

    def __sub__(self, other):
        pass
    
    def __multi__(self, other):
        pass

    def __div__(self, other):
        pass

    def __repr__(self):
        return f'ln(x)'
        
    @property
    def pprint(self):
        return f'log(x_var, E)'

class Exponential(Function):
    def __init__(self, base):
        self.base = base

        if self.base == 1:
            a = Constant(1)
            self.__class__ = a.__class__
            self.__dict__ = a.__dict__
        elif self.base == 0:
            a = Constant(0)
            self.__class__ = a.__class__
            self.__dict__ = a.__dict__
    
    def evaluate(self, x):
        return self.base ** x

    @property
    def derivative(self):
        if self.base == 'e':
            return Exponential('e')
        return Multiply([Constant(f'log(Rational({self.base}), E)'), Exponential(self.base)])

    @property
    def integral(self):
        if self.base == 'e':
            return Exponential('e')
        return Divide(Exponential(self.base), Constant(f'log(Rational({self.base}), E)'))

    def w_derivative_1(self):
        if self.base == 'e':
            return Multiply([Constant(f'log(Rational(2), E)'), Exponential(2)])
        return Exponential('e')
        
    def w_derivative_2(self):
        if self.base == 'e':
            return Multiply([Constant('e'), Exponential('e')])
        return self

    def w_derivative_3(self):
        if self.base == 'e':
            return Exponential('e')
        return Divide(Exponential(self.base), Constant(f'log(Rational({self.base}), E)'))

    def w_integral_1(self):
        if self.base == 'e':
            return Exponential('e')
        return Multiply([Constant(f'log(Rational({self.base}), E)'), Exponential(self.base)])
        
    def w_integral_2(self):
        return Polynomial(-1)

    def w_integral_3(self):
        if self.base == 'e':
            return Multiply([Constant('e'), Exponential('e')])
        return self

    def simplify(self):
        return self

    def __sub__(self, other):
        pass
    
    def __multi__(self, other):
        pass

    def __div__(self, other):
        pass

    def __repr__(self):
        return f'{self.base}^x'
        
    @property
    def pprint(self):
        if self.base == 'e':
            return f'E**(x_var)'
        return f'Rational({self.base})**(x_var)'

class e_to_the_x(Exponential):
    def __init__(self):
        e = Exponential('e')
        self.__class__ = e.__class__
        self.__dict = e.__dict__

# I used repl.it to write this program
from util import *

# Imports
from random import randint
from random import choice as chooser
from time import perf_counter
# importing random package for random integer generation and choosing a random thing in a list
# imporing perf_counter to measure time

# Constants
ADD_MAX = 15
MULTI_MAX = 10
X_BOUND = 10
SCALE_MAX = 5
NEGATIVE = True

def generateAddition():
    expression = [randint(0, ADD_MAX), randint(0, ADD_MAX)]
    total = sum(expression)
    return f"{expression[0]} + {expression[1]}", total

def generateSubtraction():
    expression = [randint(0, ADD_MAX), randint(0, ADD_MAX)]
    expression = sorted(expression)
    if randint(0, 1) == 1 and NEGATIVE:
        result = expression[0] - expression[1]
        return f"{expression[0]} - {expression[1]}", result
    else:
        result = expression[1] - expression[0]
        return f"{expression[1]} - {expression[0]}", result

def generateMultiplication():
    expression = [randint(0, MULTI_MAX), randint(0, MULTI_MAX)]
    result = expression[0] * expression[1]
    return f"{expression[0]} * {expression[1]}", result

def generateDivision():
    expression = [randint(1, MULTI_MAX), randint(1, MULTI_MAX)]
    result = expression[0] * expression[1]
    return f"{result} / {expression[1]}", expression[0]

def generateEquation():
    # Generate the Answer
    if NEGATIVE:
        x = randint(-X_BOUND, X_BOUND)
    else:
        x = randint(1, X_BOUND)

    # Generate a scalar to multiply the equation by
    if NEGATIVE:
        scale = randint(-SCALE_MAX, SCALE_MAX)
    else:
        scale = randint(1, SCALE_MAX)
    
    # make sure it is not 0
    while scale == 0:
        if NEGATIVE:
            scale = randint(-SCALE_MAX, SCALE_MAX)
        else:
            scale = randint(1, SCALE_MAX)

    # save the equation
    equation = [f'{scale}x', f'{scale * x}']

    if randint(0, 1) == 1:
        # Add or Subtract
        num = randint(-SCALE_MAX, SCALE_MAX)
        
        # check if the number is positive or negative
        if num == abs(num):
            # add it to both sides of the equation
            equation[0] = equation[0] + f" + {num}"
            equation[1] = equation[1] + f" + {num}"
            equation[1] = str(eval(equation[1]))
        else:
            equation[0] = equation[0] + f" - {abs(num)}"
            equation[1] = equation[1] + f" - {abs(num)}"
            equation[1] = str(eval(equation[1]))

    else:
        # Divide
        fraction = randint(1, 10)
        equation[0] = equation[0] + f" / {fraction}"
        equation[1] = equation[1] + f" / {fraction}"

        # Simplify if it is not a decimal
        LHS = eval(equation[1])
        if int(LHS) == float(LHS):
            equation[1] = str(int(LHS))

    # flip sides randomly
    if randint(0, 1) == 1:
        equation = list(reversed(equation))

    # return the equation list, string, and answer
    return f"{equation[0]} = {equation[1]}", x

def configureQuiz():
    # Generate Quiz
    # store 
    # time-add-sub-multi-div-equations-max-negative
    config = []
    # Welcome User
    print(
        """
    Welcome to the Customizable Math Quiz!

    To start, select the time limit for your test.
          """
    )
    while True:
        choices = [
            '30 seconds',
            '1 minute',
            '2 minutes',
            'Custom'
        ]
        
        user_choice = choice_input(choices)
        if user_choice == 0:
            config.append(30)
        elif user_choice == 1:
            config.append(60)
        elif user_choice == 2:
            config.append(120)
        elif user_choice == 3:
            seconds = getSeconds()
            if seconds == -1:
                continue
            config.append(seconds)
        
        questions = [
            'Would you like addition in the quiz?',
            'Would you like subtraction in the quiz?',
            'Would you like multiplication in the quiz?',
            'Would you like division in the quiz?',
            'Would you like simple equations in the quiz?',
        ]

        print('Now select the question types you want')
        for question in questions:
            config.append(yesOrNo(question))
        
        if yesOrNo('Would you like a maximum number of questions?'):
            config.append(abs(getIntInput('Enter the Maximum', int)))
        else:
            config.append(0)
            
        # Quiz Loop
        questionGenerator = []
        
        if config[1] == True:
            questionGenerator.append(generateAddition)
        if config[2] == True:
            questionGenerator.append(generateSubtraction)
        if config[3] == True:
            questionGenerator.append(generateMultiplication)
        if config[4] == True:
            questionGenerator.append(generateDivision)
        if config[5] == True:
            questionGenerator.append(generateEquation)

        # restart if no questions selected
        if len(questionGenerator) == 0:
            print("No Questions")
            continue

        if not yesOrNo('Would you like negative numbers?'):
            config.append(False)
            global NEGATIVE
            NEGATIVE = False
        else:
            config.append(True)

        return questionGenerator, config

def startQuiz(questionGenerator, config):
    # question, correct, time, answer, user answer
    problems = []
    print('\n'*8)
    input("Enter to start your quiz\n")

    # get starting time
    start = perf_counter()
    while True:
        print('\n'*3)
        func = chooser(questionGenerator)
        
        expression, answer = func()
        
        question = f"{len(problems) + 1}. {expression}"
        user_given = perf_counter()
        if user_given - start >= config[0]:
            break
        user_answer = mathInput(question)
        if user_answer is False:
            break
        
        user_answered = perf_counter()
        if user_answered - start >= config[0]:
            break
    
        time_to_solve = user_answered - user_given
        # question, correct boolean, time, correct answer, user answer
        if user_answer == answer:
            print("Correct")
            problems.append([question, True, time_to_solve, answer, user_answer])
        else:
            print("Incorrect")
            problems.append([question, False, time_to_solve, answer, user_answer])
        print(f'{round(config[0] - user_answered + start, 2)} seconds left')
            
        if config[6] != 0 and len(problems) == config[6]:
            break
    

    # Calculate Stats  
    score = sum([generateScore(i[1], i[2]) for i in problems])
    # Print Answers
    print(f'You got a score of {round(score, 2)}')
    num_correct = 0
    num_incorrect = 0
    for i in problems:
        if i[1] == True:
            num_correct += 1
        else:
            num_incorrect += 1

    print(f'You got {num_correct} out of {len(problems)}')
    print(f'With an accuracy of {round(100 * num_correct / len(problems))}%\n')
    
    if num_incorrect != 0:
        input('Enter to view problems wrong')
        print('Here are the problems you got wrong')
        for i in problems:
            if i[1] == False:
                print(i[0])
                print(f'Answer {i[3]}')
                print(f'You answered {i[4]}')
                print(f'Time spent {round(i[2], 2)} seconds \n')

    # find fastest problem solved
    fastest = [0,0,config[0],0]
    for problem in problems:
        # check if correct and if its faster
        if problem[1] and problem[2] < fastest[2]:
            fastest = problem

    input('Enter for overview of solve times')
    print(f'Fastest Problem solved in {round(fastest[2], 5)} seconds')
    print(f'Average Speed {sum([i[2] for i in problems]) / len(problems)}')
    # each problem in problems has 
    # the problem, boolean if correct, solve time, correct answer, user answer
    answerBooleans = [problem[1] for problem in problems] # problem[1] is the boolean if the answer is correct
    print(f'Longest correct answer streak of {calculateLongestStreak(answerBooleans, True)} problems\n')
    print(f'Longest incorrect answer streak of {calculateLongestStreak(answerBooleans, False)} problems\n')
    
    print('Problems in order of time spent')
    for problem in sorted(problems, key=lambda x: x[2]):
        print(problem[0].split('.')[1], 'solved in', round(problem[2],5), 'seconds', 'Correct' if problem[1] else 'Incorrect')

    input('Enter to print problems')
    for i in problems:
        a = 'Correctly' if i[1] else 'Incorrectly'
        print(f'{i[0]} answer is {i[3]} you answered {i[4]} {a} in {round(i[2], 2)} seconds')

if __name__ == '__main__':
    while True:
        questionGenerator, config = configureQuiz()
        startQuiz(questionGenerator, config)
        while yesOrNo('Play again with same config?'):
            startQuiz(questionGenerator, config)
    
        if yesOrNo('Play again?'):
            pass
        else:
            break
    print(config)
    
    input('Good Job!\nEnter to exit\n') #h
print('Booting Up...')
# I used repl.it to write this program
from util import *
from questions import *

question_types = [
    PowerRuleDerivativeQuestion,
    ConstantDerivativeQuestion,
    CompositeDerivativeQuestion,
    LinearDerivativeQuestion,
    AdditionDerivativeQuestion,
    TrigDerivativeQuestion,
    ExponentialDerivativeQuestion, 
    NaturalLogDerivativeQuestion,
    CompositeIntegralQuestion,
    TrigIntegralQuestion,
    PowerRuleIntegralQuestion,
    ExponentialIntegralQuestion,
    ConstantIntegralQuestion,
    CompositeIntegralQuestion,
    LinearIntegralQuestion,
    PSeriesQuestion,
    GeometricSeriesQuestion,
    ArcLengthQuestion,
    VolumeQuestion,
    AreaQuestion
]

# Imports
from random import randint
from random import choice as chooser
from time import perf_counter
# importing random package for random integer generation and choosing a random thing in a list
# imporing perf_counter to measure time

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
            '1 minute',
            '2 minutes',
            '4 minutes',
            'Custom'
        ]
        
        user_choice = choice_input(choices)
        if user_choice == 0:
            config.append(60)
        elif user_choice == 1:
            config.append(120)
        elif user_choice == 2:
            config.append(240)
        elif user_choice == 3:
            seconds = getSeconds()
            if seconds == -1:
                continue
            config.append(seconds)

        print('Now select the question types you want')
        questionGenerator = []
        for question in question_types:
            answer = yesOrNo(question().askToInclude)
            if answer:
                questionGenerator.append(question)
            config.append(answer)
        
        if yesOrNo('Would you like a maximum number of questions?'):
            config.append(abs(getIntInput('Enter the Maximum', int)))
        else:
            config.append(0)

        # restart if no questions selected
        if len(questionGenerator) == 0:
            print("No Questions")
            continue

        if yesOrNo('Would you like to print some questions before you start?'):
            num = abs(getIntInput('How many questions would you like to print?', int))
            
            letters = ['a', 'b', 'c', 'd', 'e', 'f']
            for i in range(num):
                while True:
                    try:
                        question = chooser(questionGenerator)()
                        question.generateQuestion()
                        question.askQuestion()
                        print(f'\nThe Answer was {question.answer + 1} or {letters[question.answer]}')
                        sleep(2)
                        break
                    except:
                        continue

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
        question = None
        while True:
            try:
                question = chooser(questionGenerator)()
                question.generateQuestion()
                break
            except:
                continue
        
        question.askQuestion()
        user_given = perf_counter()
        if user_given - start >= config[0]:
            break
        correct, u_ans, c_ans, _ = question.getUserAnswer()
        if u_ans is None:
            break
        
        user_answered = perf_counter()
        if user_answered - start >= config[0]:
            break
    
        time_to_solve = user_answered - user_given
        # question, correct boolean, time, correct answer, user answer
        if correct:
            print("Correct")
            problems.append([question, True, time_to_solve, c_ans, u_ans])
        else:
            print("Incorrect")
            problems.append([question, False, time_to_solve, c_ans, u_ans])
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

    if len(problems) > 0:
        print(f'You got {num_correct} out of {len(problems)}')
        print(f'With an accuracy of {round(100 * num_correct / len(problems))}%\n')
    else:
        print('Well that is embarassing')
        return
    
    if num_incorrect != 0:
        input('Enter to view problems wrong')
        print('Here are the problems you got wrong')
        for i in problems:
            if i[1] == False:
                i[0].askQuestion()
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
    for i in range(len(problems)):
        thing = problems[i]
        a = 'Correctly' if thing[1] else 'Incorrectly'
        print(f'Answer is {thing[3]} you answered {thing[4]} {a} in {round(thing[2], 2)} seconds')

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
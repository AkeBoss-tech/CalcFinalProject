print('Booting Up...')
# I used repl.it to write this program
from util import *
from questions import *

DEBUG = False

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
    LinearIntegralQuestion,
    PSeriesQuestion,
    GeometricSeriesQuestion,
    ArcLengthQuestion,
    VolumeQuestion,
    AreaQuestion,
    AverageValueQuestion
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
    printf(
        """
    *b^vWelcome to the Customizable Calculus Quiz!*e

    To start, select the ^Ytime limit*e for your test.
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

        printf('Now select the ^gquestion types^e you want')
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
                if not DEBUG:
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
                else:
                    question = chooser(questionGenerator)()
                    question.generateQuestion()
                    question.askQuestion()
                    print(f'\nThe Answer was {question.answer + 1} or {letters[question.answer]}')
                    sleep(2)

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
        if not DEBUG:
            while True:
                try:
                    question = chooser(questionGenerator)()
                    question.generateQuestion()
                    break
                except:
                    continue
        else:
            question = chooser(questionGenerator)()
            question.generateQuestion()
            
        
        question.askQuestion(f'{len(problems) + 1}.')
        user_given = perf_counter()
        if user_given - start >= config[0]:
            printf('You answered ^Rtoo late^e')
            break
        correct, u_ans, c_ans, _ = question.getUserAnswer()
        if u_ans is None:
            printf('^rExiting^e')
            break
        
        user_answered = perf_counter()
        if user_answered - start >= config[0]:
            break
    
        time_to_solve = user_answered - user_given
        # question, correct boolean, time, correct answer, user answer
        if correct:
            printf("^GCorrect^e")
            problems.append([question, True, time_to_solve, c_ans, u_ans])
        else:
            printf("^RIncorrect^e")
            problems.append([question, False, time_to_solve, c_ans, u_ans])
        printf(f'*b^R{round(config[0] - user_answered + start, 2)} seconds*e left')
            
        if config[-1] != 0 and len(problems) == config[-1]:
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
        printf(f'You got *s{num_correct} out of {len(problems)}*e')
        printf(f'With an accuracy of *s{round(100 * num_correct / len(problems))}%*e\n')
    else:
        print('Well that is embarassing')
        return
    
    if num_incorrect != 0:
        input('Enter to view problems wrong')
        printf('Here are the problems you got ^rwrong^e')
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
    printf(f'Fastest Problem solved in *s{round(fastest[2], 5)} seconds*e')
    print(f'Average Speed {sum([i[2] for i in problems]) / len(problems)}')
    # each problem in problems has 
    # the problem, boolean if correct, solve time, correct answer, user answer
    answerBooleans = [problem[1] for problem in problems] # problem[1] is the boolean if the answer is correct
    printf(f'Longest correct answer streak of ^G{calculateLongestStreak(answerBooleans, True)} problems*e\n')
    printf(f'Longest incorrect answer streak of ^r{calculateLongestStreak(answerBooleans, False)} problems*e\n')
    
    print('Problems in order of time spent')
    for problem in sorted(problems, key=lambda x: x[2]):
         print(problem[0].printSimple(), 'solved in', round(problem[2],5), 'seconds', 'Correct' if problem[1] else 'Incorrect')

    input('Enter to print problems')
    for i in range(len(problems)):
        thing = problems[i]
        a = 'Correctly' if thing[1] else 'Incorrectly'
        print(f'{i+1}. {thing[0].printSimple()} Answer is {thing[3]} you answered {thing[4]} {a} in {round(thing[2], 2)} seconds')

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
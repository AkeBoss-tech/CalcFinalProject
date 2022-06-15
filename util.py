from random import randint
from random import choice as chooser
from time import perf_counter
from color import printf

class Operation:
    def __init__(self):
        pass


# Define Functions


# function copied from a project I previously made on replit
def getIntInput(text, check):
    while True:
        print(text)
        inp = input("> ").strip()
        try:
            return check(inp)       
        except:
            print("Answer not accepted")

# reused this function from other programs i made on replit
def choice_input(choices):
    while True:
        print()
        # print all of the choices
        for num, thing in enumerate(choices):
            if thing:
                print(f"{num + 1}. {thing}")

        print()
        inp = input("> ")
        # check if it is acceptable
        try:
            if int(inp) > 0 and int(inp) < len(choices) + 1:    return int(inp) - 1
            print("Number not in range")
            
        except ValueError:
            print("Answer not accepted")
            print("Please input a number")

# copied from an old project on replit
def getSeconds():
    conversions = {
        'Minutes': 60,
        'Hours': 60 * 60,
    }
    print('\nTime to seconds')
    units = ['Seconds', 'Minutes', 'Hours']
    things = []
    
    print('Please print the values for the times')
    for unit in units:
        inp = input(f'Please enter {unit}\n> ')
        try:
            things.append(int(inp))
        except ValueError:
            print("Exiting")
            return -1
    
    seconds = 0
    for key, value in reversed(list(conversions.items())):
        try:
            index = units.index(key)
            seconds += things[index] * value
        except:
            continue
    seconds += things[0]
    return seconds

# yes or no user input
# copied from something I've previously made on replit
def yesOrNo(text):
	while True:
		# loop untill acceptable input
		printf(f'{text} (y,n)')
		a = input('> ').strip().upper()
	
		# Depending on answer stop or run again
		if len(a) == 0:
			return True
        
		if a[0] == 'Y':
			return True
		elif a[0] == 'N':
			return False
		else:
			print(f'Input {a} not accepted please try again. ')

def mathInput(text):
    while True:
        print(text)
        inp = input("> ").strip()
        if inp == 'exit':
            return False
        
        allowableCharacters = '1234567890/.-'
        a = False
        for char in inp:
            if char not in allowableCharacters:
                print('Answer not Accepted. Please Try Again')
                a = True
                break
        if a:
            continue

        try:
            return eval(inp)
        except:
            print('Answer not accepted please try again')

def generateScore(correct, time):
    if correct:
        if time < 5:
            return 10-time
        return 3
    else:
        return -1

def calculateLongestStreak(answers, correct):
    # create variables
    streaks = []
    currentStreak = 0

    # loop throught the list and count answer streaks
    for answer in answers:
        if answer == correct:
            currentStreak += 1
        else:
            if currentStreak != 0:
                streaks.append(currentStreak)
            currentStreak = 0
    
    if currentStreak != 0:
        streaks.append(currentStreak)

    maxStreak = 0
    for streak in streaks:
        if streak > maxStreak:
            maxStreak = streak

    return maxStreak
from random import choice

# color codes copied from stack overflow
END      = '\33[0m'
BOLD     = '\33[1m'
ITALIC   = '\33[3m'
URL      = '\33[4m'
BLINK    = '\33[5m'
BLINK2   = '\33[6m'
SELECTED = '\33[7m'
# add short codes that corrispond to styles
modifier_short = {
    "*e": END,
    "*b": BOLD,
    "*i": ITALIC,
    "*u": URL,
    "*l": BLINK,
    "*s": SELECTED
}

BLACK  = '\33[30m'
RED    = '\33[31m'
GREEN  = '\33[32m'
YELLOW = '\33[33m'
BLUE   = '\33[34m'
VIOLET = '\33[35m'
BEIGE  = '\33[36m'
WHITE  = '\33[37m'

GREY    = '\33[90m'
RED2    = '\33[91m'
GREEN2  = '\33[92m'
YELLOW2 = '\33[93m'
BLUE2   = '\33[94m'
VIOLET2 = '\33[95m'
BEIGE2  = '\33[96m'
WHITE2  = '\33[97m'

# short codes that corrispond to colors
color_short = {
    "^e": END,
    "^D": BLACK,
    "^R": RED,
    "^G": GREEN,
    "^y": YELLOW,
    "^b": BLUE,
    "^V": VIOLET,
    "^W": WHITE2,
    "^d": GREY,
    "^r": RED2,
    '^g': GREEN2,
    '^Y': YELLOW2,
    '^B': BLUE2,
    '^v': VIOLET2,
}

BLACKBG  = '\33[40m'
REDBG    = '\33[41m'
GREENBG  = '\33[42m'
YELLOWBG = '\33[43m'
BLUEBG   = '\33[44m'
VIOLETBG = '\33[45m'
BEIGEBG  = '\33[46m'
WHITEBG  = '\33[47m'

GREYBG    = '\33[100m'
REDBG2    = '\33[101m'
GREENBG2  = '\33[102m'
YELLOWBG2 = '\33[103m'
BLUEBG2   = '\33[104m'
VIOLETBG2 = '\33[105m'
BEIGEBG2  = '\33[106m'
WHITEBG2  = '\33[107m'

# i figured out that if you set the color before you turn on select mode it also works for background colors
# so i don't need to make shortcuts for this

# not used but can be used to color any text with any style, color, or background
def colorText(text, color):
    return color + text + END

# replace the shortcuts with color codes
def getText(text):
    while "*" in text: # loop until we get all of the style codes
        index = text.index('*')
        if index <= len(text) - 2: # check to make sure a leter is infront of it
            short = text[index:index+2] # make a substring with the code
            if short in modifier_short: # check if it is a valid code
                # replace it with the code
                text = text.replace(short, modifier_short[short])
            else:
                # if we dont know get rid of it
                text = text.replace(short, '')
        else:
            # no letter in front
            break

    # same as above except with different first character and shorcut list
    # i could have made a big list and only one loop
    # its fine i dont wanna do this anymore
    while "^" in text:
        index = text.index('^')
        if index <= len(text) - 2:
            short = text[index:index+2]
            if short in color_short:
                text = text.replace(short, color_short[short])
            else:
                text = text.replace(short, '')
        else:
            break
    
    return text

# the new printing function
def printf(text):
    print(getText(text))

# the new input function
def inputf(text):
    return input(getText(text))

def randomColor():
    return choice(list(color_short.keys()))
from turtle import *
from random import randint, choice
import time

sw = 720
sh = 850
s = getscreen()
s.setup(sw, sh)
s.bgcolor('#32EFEF')

t1=getturtle()
t1.speed(0)
t1.width(int(sw*0.05))
t1.hideturtle()

#we need to make another turtle
tWriter = Turtle()
tWriter.hideturtle()
#Let's Make One for Wrong Letters, too
tBadLetters = Turtle()
tBadLetters.hideturtle()

#variables to play the game -- Global
fontS = int(sh*0.04)

def displayText(newText):
	tWriter.clear()
	tWriter.penup()
	tWriter.goto(-int(sw*0.40), -int(sh*0.40))
	tWriter.write( newText, font=("Arial", fontS, "bold"))

def displayBadLetters(newText):
	tBadLetters.clear()
	tBadLetters.penup()
	tBadLetters.goto(-int(sw*0.40), int(sh*0.36)) 
	tBadLetters.write( newText, font=("Arial", fontS, "bold"))

leg_angle = 33
arm_angle = 45

# dictionary to record turtle position
turtle_position = {}

def drawGallows():
    t1.hideturtle()
    t1.pensize(7)
    t1.speed(10)
    t1.color("Black")
    t1.forward(120)
    t1.forward(-40)
    t1.left(90)
    t1.forward(150)
    t1.left(90)
    t1.forward(100)
    t1.left(90)
    t1.forward(30)
    t1.right(90)
    turtle_position['noose_end'] = t1.position()
    # change the pen width for drawing hangman
    t1.pensize(3)

def draw_head():
	t1.hideturtle()
	t1.circle(15)
	t1.circle(15, 180) # draw a semicircle
	t1.right(90)
	turtle_position['head_end'] = t1.position()

def draw_torso():
	t1.hideturtle()
	# position turtle to head_end 
	t1.setposition(turtle_position['head_end'])
	t1.setheading(270)
	t1.forward(45)
	turtle_position['torso_end'] = t1.position()

def draw_arms():
	t1.penup()
	t1.setposition(turtle_position['head_end'])
	t1.setheading(270)
	t1.pendown()
	t1.forward(20)
	t1.setheading(90)
	t1.left(arm_angle)
	t1.forward(20)
	t1.forward(-20)
	t1.setheading(90)
	t1.right(arm_angle)
	t1.forward(20)
	t1.forward(-20)

def draw_legs():
	# position turtle to torso_end
	t1.penup()
	t1.setposition(turtle_position['torso_end'])
	t1.setheading(270)
	t1.pendown()
	t1.right(leg_angle)
	t1.forward(35)
	t1.forward(-35)
	t1.setheading(270)
	t1.left(leg_angle)
	t1.forward(35)
	t1.forward(-35)

def draw_eyes():
	t1.penup()
	t1.setposition(turtle_position['noose_end'])
	t1.setheading(270)
	# Move to left eye
	t1.forward(10)
	t1.right(90)
	t1.forward(6)
	t1.pendown()
	t1.circle(2)
	# Retreat to Noose and draw right eye
	t1.penup()
	t1.setposition(turtle_position['noose_end'])
	t1.setheading(270)
	# Move to right eye
	t1.forward(10)
	t1.left(90)
	t1.forward(6)
	t1.right(180)
	t1.pendown()
	t1.circle(2)

def draw_mouth():
	t1.penup()
	t1.setposition(turtle_position['noose_end'])
	t1.setheading(270)
	# Move to left eye
	t1.forward(20)
	t1.left(90)
	t1.forward(4)
	t1.setheading(270)
	t1.pendown()
	t1.circle(-4, 180)

def draw_hangman(step):	
	if step == 0:
		t1.reset()
		drawGallows()
	elif step == 1:
		draw_head()
	elif step == 2:
		draw_torso()
	elif step == 3:
		draw_arms()	
	elif step == 4:
		draw_legs()
	elif step == 5:
		draw_eyes()
	elif step == 6:
		draw_mouth()
	else:
		t1.hideturtle()

def pickSecretWord():
	global secretWord
	wordList = "election democrat republic senate congress midterm".split()
	secretWord = choice(wordList)

def getGuess():
	boxTitle = "Letters Used: " + lettersWrong
	guess = s.textinput(boxTitle, "Enter a Guess type $$ to guess the word")
	return guess 

def makeWordString():
	global displayWord, secretWord, lettersCorrect

	displayWord = ['_'] * len(secretWord)
	# turn on correctly guessed chars in displayWord
	for correct_char in lettersCorrect:
		for i, c in enumerate(secretWord):
			if c == correct_char:
				displayWord[i] = correct_char
	# convert list into string
	displayWord = '  '.join(displayWord)

def checkWordGuess():
	global secretWord, gameDone, displayWord

	displayText("Please guess the word")
	theGuessWord = getGuess()
	if theGuessWord.lower() == secretWord.lower():
		displayText("You Rock! \nThe secret word is: " + secretWord)
		gameDone = True
	else:
		displayText("Sorry, guess again")
		time.sleep(2)
		displayText(displayWord)

def playGame():
	global gameDone, fails, alpha, secretWord, lettersCorrect, lettersWrong
	global failMax

	while gameDone == False and fails > 0:
		# get input
		theGuess = getGuess()
		if theGuess is None:
			# press Cancel button to exit game
			break
		elif theGuess == "$$":
			print("Let them guess word")
			checkWordGuess() ###NEW
		elif len(theGuess) > 1 or theGuess == "":
			displayText("Sorry I need a letter, guess again")
			time.sleep(1)
			displayText(displayWord)
		elif theGuess not in alpha:
			displayText(theGuess + " is not a letter, guess again.")
			time.sleep(1)
			displayText(displayWord)
		elif theGuess.lower() in secretWord.lower():
			lettersCorrect += theGuess.lower()
			makeWordString()
			displayText(displayWord)
			# ur_answer = ''.join(displayWord.split())
			# if ur_answer == secretWord:
			# 	displayText(displayWord + "\nYou Won!")
			# 	gameDone = True
			# 	break
		else:
			if theGuess.lower() not in lettersWrong:
				lettersWrong += theGuess.lower() + ", "
				fails -= 1
				displayText(theGuess + " is not in the word")
				time.sleep(1)
				draw_hangman(failMax - fails)
				displayText(displayWord)
				displayBadLetters("Not in word: [" + lettersWrong + "]")
			else:
				displayText(theGuess + " was already guessed. Try again")
				time.sleep(1)
				displayText(displayWord)

		if "_" not in displayWord:
			displayText("YES!!! You Won-Word is:" + secretWord)
			gameDone = True

		if fails <= 0:
			displayText("Sorry Out of Guess-Word is " + secretWord)
			gameDone = True

		if gameDone == True:
			restartGame()

	

def restartGame():
	global fails, failMax, lettersCorrect, lettersWrong, gameDone
	boxTitle = "Want to play again"
	guess = s.textinput(boxTitle, 'Input "yes" to play again')

	if guess.lower() == 'y' or guess.lower() == 'yes':
		lettersCorrect = ""
		lettersWrong = ""
		t1.clear()
		t1.penup()
		t1.home()
		t1.pendown()
		drawGallows()
		pickSecretWord()
		displayText("Guess a Letter..")
		displayBadLetters("Not in word: [" + lettersWrong + "]")
		time.sleep(1)
		makeWordString()
		displayText(displayWord)
		fails = 6
		gameDone = False
	else:
		displayBadLetters("Ok, see you later")
		time.sleep(5)


#actual game setup
alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
lettersWrong = "" # startting as empty strings
lettersCorrect = ""
secretWord = ""
displayWord = ""
failMax = 6
fails = failMax #how many wrong guesses you have left
gameDone = False

#actual game setup
t1.clear()
drawGallows()
pickSecretWord()
displayText("Guess a Letter..")
displayBadLetters("Not in word: [" + lettersWrong + "]")
time.sleep(1)
makeWordString()
displayText(displayWord)
playGame()
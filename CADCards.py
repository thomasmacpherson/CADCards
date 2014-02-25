import pifacecad
import random
from time import sleep
import sys

len(sys.argv)

cardBack = pifacecad.LCDBitmap([0b11111,0b10001,0b10001,0b10001,0b10001,0b10001,0b10001,0b11111])
card1 = pifacecad.LCDBitmap([0b00000,0b11111,0b10001,0b10001,0b10001,0b10001,0b11111,0b00000])
card2 = pifacecad.LCDBitmap([0b00000,0b00000,0b11111,0b10001,0b10001,0b11111,0b00000,0b00000])
card3 = pifacecad.LCDBitmap([0b00000,0b00000,0b00000,0b11111,0b11111,0b00000,0b00000,0b00000])



images = [[0x1f, 0x11, 0xa, 0x4, 0xa, 0x11, 0x1f, 0x0],
		  [0x2,0x3,0x2,0x2,0xe,0x1e,0xc,0x0],
		  [0x4,0xe,0xe,0xe,0x1f,0x0,0x4,0x0],
		  [0x0,0xa,0x1f,0x1f,0x1f,0xe,0x4,0x0],
		  [0x0,0x1,0x3,0x16,0x1c,0x8,0x0,0x0],
		  [0x0,0x1b,0xe,0x4,0xe,0x1b,0x0,0x0],
		  [0x0,0xe,0x15,0x17,0x11,0xe,0x0,0x0],
		  [0b00000,0b01010,0b00100,0b11111,0b10101,0b11111,0b10101,0b11111],
		  [0b00000,0b00100,0b10101,0b01110,0b11111,0b01110,0b10101,0b00100],
		  [0b00000,0b01010,0b00000,0b00100,0b00000,0b01010,0b01110,0b00000]]

if len(sys.argv) == 2 and int(sys.argv[1]) <= len(images) and int(sys.argv[1]) > 1:
	cardTypeNumber = int(sys.argv[1])
else:
	cardTypeNumber = len(images)

cardImages = []
for i in range(0,cardTypeNumber):
	cardImages.append(pifacecad.LCDBitmap(images[i]))
f = open('CADCardsHighScores','r')

previousHighScore = 100

lines = f.readlines()

previousHighScore = int(lines[cardTypeNumber-2].replace("\n",""))

f.close()
print("Previous high score")
print(previousHighScore)

cardNumber=0
previousCardImage = None
previousCardPos = [0,0]
turns = 0

cad = pifacecad.PiFaceCAD()
cad.lcd.backlight_on()
cad.lcd.cursor_off()
cad.lcd.write("Turns:")
cad.lcd.store_custom_bitmap(0,cardBack)
cad.lcd.store_custom_bitmap(1,card1)
cad.lcd.store_custom_bitmap(2,card2)
cad.lcd.store_custom_bitmap(3,card3)
cad.lcd.set_cursor(0,1)
cad.lcd.write(str(turns))

gameOver = False


cad.lcd.set_cursor(16-len(cardImages),0)
for i in range (16-len(cardImages),16):
	cad.lcd.write_custom_bitmap(0)

cad.lcd.set_cursor(16-len(cardImages),1)
for i in range (16-len(cardImages),16):
	cad.lcd.write_custom_bitmap(0)

cards = []
for i, x in enumerate(cardImages):
	cards.append(i)
	cards.append(i)

placedCards = []
for card in range(0,len(cards)):
	index = random.randint(0,len(cards)-1)
	placedCards.append(cards[index])
	del cards[index]

cad.lcd.set_cursor(16-len(cardImages),0)

def checkDifferent(x,y):
	global previousCardPos
	if x == previousCardPos[0] and y == previousCardPos[1]:
		return 0
	else:
		return 1

def left(event):
	x, y = cad.lcd.get_cursor()
	while True:
		if x > 16-len(cardImages):
			x -=1
			if placedCards[(x-(16-len(cardImages)))+(y*len(cardImages))] != -1 and checkDifferent(x,y):
				cad.lcd.set_cursor(x,y)
				cad.lcd.blink_on()
				break
		else:
			x = 15
			y = (y+1)%2
			if placedCards[(x-(16-len(cardImages)))+(y*len(cardImages))] != -1 and checkDifferent(x,y):
				cad.lcd.set_cursor(x,y)
				cad.lcd.blink_on()
				break


def right(event):
	x, y = cad.lcd.get_cursor()
	while True:
		if x < 15:
			x +=1
			if placedCards[(x-(16-len(cardImages)))+(y*len(cardImages))] != -1 and checkDifferent(x,y):
				cad.lcd.set_cursor(x,y)
				cad.lcd.blink_on()
				break
		else:
			x = 16-len(cardImages)
			y = (y+1)%2
			if placedCards[(x-(16-len(cardImages)))+(y*len(cardImages))] != -1 and checkDifferent(x,y):
				cad.lcd.set_cursor(x,y)
				cad.lcd.blink_on()
				break

def rowSwitch(event):
	x, y = cad.lcd.get_cursor()
	y = (y+1)%2
	#print(placedCards)
	#print((x-(16-len(cardImages)))+(y*len(cardImages)))
	if placedCards[(x-(16-len(cardImages)))+(y*len(cardImages))] != -1 and checkDifferent(x,y):
		cad.lcd.set_cursor(x,y)
		cad.lcd.blink_on()


def flipCard(coordinateList):
	for pos in coordinateList:
		cad.lcd.set_cursor(pos[0],pos[1])
		cad.lcd.write_custom_bitmap(1)	

	for pos in coordinateList:
		cad.lcd.set_cursor(pos[0],pos[1])
		cad.lcd.write_custom_bitmap(2)	

	for pos in coordinateList:
		cad.lcd.set_cursor(pos[0],pos[1])
		cad.lcd.write_custom_bitmap(3)	

	for pos in coordinateList:
		cad.lcd.set_cursor(pos[0],pos[1])
		cad.lcd.write_custom_bitmap(2)	

	for pos in coordinateList:
		cad.lcd.set_cursor(pos[0],pos[1])
		cad.lcd.write_custom_bitmap(1)	
	

def checkWin():
	global gameOver
	global placedCards
	gameOver = True
	for card in placedCards:
		if card != -1:
			gameOver = False
			break

def enter(event):
	global cardNumber
	global previousCardImage
	global previousCardPos
	global turns

	cad.lcd.blink_off()
	x,y = cad.lcd.get_cursor()

	if checkDifferent(x,y):
		cardIndex = (x-(16-len(cardImages)))+(y*len(cardImages))
		cardImageIndex =placedCards[cardIndex]
		cad.lcd.store_custom_bitmap(4+cardNumber,cardImages[cardImageIndex])
		flipCard([[x,y]])
		cad.lcd.set_cursor(x,y)
		cad.lcd.write_custom_bitmap(4+cardNumber)

		if not cardNumber:
			previousCardImage = cardImageIndex
			cardNumber+=1
			previousCardPos = [x,y]
			cad.lcd.set_cursor(x,y)
		else:
			sleep(1)
			cardNumber = 0
			cad.lcd.set_cursor(0,1)
			turns += 1
			cad.lcd.write(str(turns))

			if cardImageIndex == previousCardImage:
				cad.lcd.set_cursor(x,y)
				cad.lcd.write(" ")
				placedCards[(x-(16-len(cardImages)))+(y*len(cardImages))] = -1
				cad.lcd.set_cursor(previousCardPos[0],previousCardPos[1])
				cad.lcd.write(" ")
				cad.lcd.set_cursor(x,y)
				placedCards[(previousCardPos[0]-(16-len(cardImages)))+(previousCardPos[1]*len(cardImages))] = -1
				checkWin()

			else:
				flipCard([[x,y],previousCardPos])
				cad.lcd.set_cursor(x,y)	
				cad.lcd.write_custom_bitmap(0)
				cad.lcd.set_cursor(previousCardPos[0],previousCardPos[1])	
				cad.lcd.write_custom_bitmap(0)
				cad.lcd.set_cursor(x,y)
				cad.lcd.blink_on()
			previousCardPos = [0,0]

					


listener = pifacecad.SwitchEventListener(cad)
listener.register(6, pifacecad.IODIR_FALLING_EDGE, left)
listener.register(7, pifacecad.IODIR_FALLING_EDGE, right)
listener.register(4, pifacecad.IODIR_FALLING_EDGE, exit)
listener.register(3, pifacecad.IODIR_FALLING_EDGE, enter)
listener.register(5, pifacecad.IODIR_FALLING_EDGE, rowSwitch)
listener.activate()


while not gameOver:
	pass
print("Game over!")
listener.deactivate()
cad.lcd.clear()
cad.lcd.write("Game over!")
cad.lcd.set_cursor(0,1)
cad.lcd.write("{} Turns taken".format(turns))
sleep(2)
cad.lcd.clear()
cad.lcd.write("Previous \nhighscore {}".format(previousHighScore))
sleep(2)
cad.lcd.clear()
if turns < previousHighScore:
	cad.lcd.write("Congratulations\nnew highscore!")
	f = open('CADCardsHighScores','w')
	lines[cardTypeNumber-2] = "{}\n".format(turns)
	f.writelines(lines)
elif turns == previousHighScore:
	cad.lcd.write("Congratulations\non highscore!")
else:
	cad.lcd.write("Unlucky try\nagain!")


sleep(2)
cad.lcd.clear()
cad.lcd.backlight_off()

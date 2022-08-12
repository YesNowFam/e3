import random
import time
import pygame
import matplotlib.pyplot
from matplotlib import style
import matplotlib.animation
#matplotlib.use("agg")
style.use("bmh")
figure = matplotlib.pyplot.figure()
axis = figure.add_subplot(1,1,1)


rounds = 1
amountFood = 20
numCreatures = 20
OgEnvironment = [["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],["X", "X", "X", "X", "X", "X", "X", "X", "X", "X"]]
def VisEnvironment(OgEnvironment):
    for i in range(0, 10):
        for j in range(0, 10):
            if (OgEnvironment[i][j])[0] == "X":
                pygame.draw.rect((screen), (0, 0, 0), (j * 50, i * 50, 50, 50))
            elif (OgEnvironment[i][j])[0] == "F":
                pygame.draw.rect((screen), (10, 200, 50), (j * 50, i * 50, 50, 50))
            elif (OgEnvironment[i][j])[0] == "C":
                for k in range (len(OgEnvironment[i][j])):
                    if (OgEnvironment[i][j])[k] == "H":
                        strHealth = ((OgEnvironment[i][j])[k + 1] + (OgEnvironment[i][j])[k + 2])
                        health = int(strHealth)

                pygame.draw.rect((screen), (200, health+100, 50), (j * 50, i * 50, 50, 50))
    pygame.display.flip()
    VisEnvLs = ["", "", "", "", "", "", "", "", "", ""]
    for i in range(0, 10):
        for j in range(0, 10):
            if (OgEnvironment[i][j])[0] == "X":
                VisEnvLs[i] += "□"
            elif (OgEnvironment[i][j])[0] == "F":
                VisEnvLs[i] += "🍖"
            elif (OgEnvironment[i][j])[0] == "C":
                VisEnvLs[i] += "▣"
    for i in range(0, 10):
        print(VisEnvLs[i])
    print("-------------------------------------------")

def initWindowVis():
    while True:
        bgColour = (255, 255, 255)
        (width, height) = (500, 500)
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Environment")
        screen.fill(bgColour)
        pygame.display.flip()
        running = True
        """while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False"""
    return(screen)

def foodPlot(OgEnvironment,foodRounds, roundTimes):
    foodTotal = 0
    for i in range(0, 10):
        for j in range(0, 10):
            if (OgEnvironment[i][j])[0] == "F":
                foodTotal += 1
    foodRounds.append(foodTotal)
    print(roundTimes,"---------", foodRounds)
    return (roundTimes, foodRounds)

def aPlot(i):
    axis.clear()
    axis.plot([i],[i])


#determining interaction. pos are coords not item
def analyse(OgEnvironment, currentPosX, currentPosY, destPosX,destPosY):
    print(currentPosX, currentPosY, destPosX,destPosY)
    #function will return a result and
    #x an dy in terms of direction, meaning y comes before x within the array
    currentItem = OgEnvironment[currentPosY][currentPosX]
    destItem = OgEnvironment[destPosY][destPosX]
    print("Dest:",destItem,"Current:",currentItem)
    if destItem[0] == "X":
        #creature has found empty space. no result
        return("Blank", 0)
    elif destItem[0] == "F":
        #creature has found food. scanning for a nutrients value, default at 50 if not found
        nutrients = 50
        for i in range ((len(destItem))):
            if destItem[i] == "N":
                strNutrients = (destItem[i+1]+destItem[i+2])
                nutrients = int(strNutrients)
        return("Food",nutrients)
    elif destItem[0] == "C":
        #unfinished random combat
        loserChoice = random.choice (("1","2"))
        if loserChoice == "1":
            loser = (currentPosY, currentPosX)
        else:
            loser = (destPosY,destPosX)
        damage = (0-(random.randint(40,60)))
        print("In analysis:",OgEnvironment[loser[0]][loser[1]])
        return("Creature", loser, damage)

def move(OgEnvironment, currentPosX, currentPosY, destPosX, destPosY, analysis):
    currentItem = OgEnvironment[currentPosY][currentPosX]
    destItem = OgEnvironment[destPosY][destPosX]
    if analysis[0] == "Blank":
        #Moving Into free space
        OgEnvironment[currentPosY][currentPosX] = destItem
        OgEnvironment[destPosY][destPosX] = currentItem
        return(OgEnvironment)
    if analysis[0] == "Food":
        done = False
        count = 0
        #Eating Food
        nutrients = analysis[1]
        for i in range ((len(currentItem))):
            #find H. Count/Done is to add attributes after modification is done.
            if done == True:
                count+= 1
            elif count == 3:
                updateItem = updateItem + currentItem[i]
            elif currentItem[i] == "H":
                strHealth = (currentItem[i+1]+currentItem[i+2])
                health = int(strHealth)
                #food added to health
                newHealth = health + nutrients
                if newHealth > 99:
                    newHealth = 99
                #put into new string
                half = currentItem.split("H")
                newHealth = str(newHealth)
                print("Half:",half[0])
                updateItem = half[0]+"H"+newHealth
                done = True

        OgEnvironment[currentPosY][currentPosX] = "X"
        OgEnvironment[destPosY][destPosX] = updateItem
        return(OgEnvironment)
    if analysis[0] == "Creature":
        #Fight a creature
        done = False
        count= 0
        loserCoords = analysis[1]
        loser = OgEnvironment[loserCoords[0]][loserCoords[1]]
        print("Loser:",loser)
        for i in range ((len(loser))):
            #find H. Count/Done is to add attributes after modification is done.
            if done == True:
                count+= 1
            elif count == 3:
                updateItem = updateItem + loser[i]
            elif loser[i] == "H":
                strHealth = (loser[i+1]+loser[i+2])
                health = int(strHealth)
                newHealth = health + (analysis[2])
                if newHealth <= 0:
                    OgEnvironment[loserCoords[0]][loserCoords[1]] = "X"
                    print("Creature at",loserCoords,"was killed.")
                    return(OgEnvironment)
                newHealth = str(newHealth)
                if int(newHealth) <= 9:
                    newHealth = "0"+newHealth
                half = loser.split("H")
                updateItem = half[0] + "H" + newHealth
                done = True

        print(done)
        print("Updated creature:",updateItem)
        OgEnvironment[loserCoords[0]][loserCoords[1]] = updateItem
        return(OgEnvironment)



def makeMoves(OgEnvironment,moves):
    for i in range (len(moves)):
        jUnmod = moves[i][0]
        iUnmod = moves[i][1]
        jMod = moves[i][2]
        iMod = moves[i][3]
        analysis = analyse(OgEnvironment, jUnmod, iUnmod, jMod, iMod)
        print("!!!", analysis)
        if analysis[0] == "Creature":
            print(OgEnvironment[analysis[1][0]][analysis[1][1]])
        move(OgEnvironment, jUnmod, iUnmod, jMod, iMod, analysis)





#food seeding
for i in range (0,amountFood):
    OgEnvironment[random.randint(0,9)][random.randint(0,9)] = "F"
print(OgEnvironment)
#creature seeding
for i in range (0,numCreatures):
    health = random.randint(80,99)
    health = str(health)
    entryString = ("C"+"H"+health)
    OgEnvironment[random.randint(0,9)][random.randint(0,9)] = entryString
print(OgEnvironment)


clock = pygame.time.Clock()

#creature movement
while True:
    bgColour = (255, 255, 255)
    (width, height) = (500, 500)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Environment")
    screen.fill(bgColour)

    startTime = time.clock()
    roundTimes = [0]
    foodRounds = [0]
    VisEnvironment(OgEnvironment)
    """pygame.display.flip()"""
    while True:
        moves = []
        clock.tick(1)
        #cycle through all items
        for i in range(0,10):
            for j in range(0,10):
                #for every creature item, let it move
                if (OgEnvironment[i][j])[0] == "C":
                    # directions: 1=up 2=right 3=down 4=left 5=stay
                    #i is vertical, j is horizontal
                    direction = random.randint(1,5)
                    print(direction)
                    if direction == 1 and i != 0:
                        thisMove = [j, i, j, i-1]
                        moves.append(thisMove)
                    elif direction == 2 and j != 9:
                        thisMove = [j, i, j+1, i]
                        moves.append(thisMove)
                    elif direction == 3 and i != 9:
                        thisMove = [j, i, j, i + 1]
                        moves.append(thisMove)
                    elif direction == 4 and j != 0:
                        thisMove = [j, i, j-1, i]
                        moves.append(thisMove)
        currentTime = time.clock()
        roundTime = round(currentTime - startTime,3)
        roundTimes.append(roundTime)

        foodPlotVar = foodPlot(OgEnvironment, foodRounds, roundTimes)
        foodRounds = foodPlotVar[1]
        print(foodPlotVar)
        fp = matplotlib.animation.FuncAnimation(figure, aPlot, interval=1000)
        #gets this fdar
        matplotlib.pyplot.show()
        print("done")

        makeMoves(OgEnvironment,moves)
        VisEnvironment(OgEnvironment)

    """VisEnvironment(OgEnvironment)"""


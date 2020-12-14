import os.path
import itertools
import math
import statistics
########################## what if the file is wrong?????????????????????????????????????????
########################## delete it and restart.
def getVariableLetters(fullLayer, StaticLetters):
    # This extracts the non-fix letters for the first layer.
    variableLetters='' 
    j=0
    while j < len(fullLayer):
        if not fullLayer[j] in StaticLetters:
            variableLetters += fullLayer[j]
        j+=1
    return variableLetters

def getBigramList(letters, n_gramLength, txtFile, bigTxtFile):
    pureBigramArray = []
    bigramImportance = []
    absoluteBigramCount = []

    bigTxtFile = './bigram_dictionaries/' + bigTxtFile
    txtFile = './other input & output/' + txtFile
    previouslettersFile = './other input & output/' + 'previousletters.txt'
    previousBigTxtFile = './other input & output/' + 'previousBigTxtFileName.txt'
    updateTxtFile = False

    if os.path.exists(previouslettersFile):
        with open(previouslettersFile, 'r') as file:
            if file.readline() == letters:
                print('Remember to take breaks if something hurts of thinking starts getting hard. :)')
            else:
                updateTxtFile = True
                with open(previouslettersFile, 'w') as file:
                    file.write(letters)
    else:
        with open(previouslettersFile, 'w') as file:
            file.write(letters)
        updateTxtFile = True
    
    if os.path.exists(previousBigTxtFile):
        with open(previousBigTxtFile, 'r') as file:
            if file.readline() == bigTxtFile:
                print('Still working on that one language ...')
            else:
                updateTxtFile = True
                with open(previousBigTxtFile, 'w') as file:
                    file.write(bigTxtFile)
    else:
        with open(previousBigTxtFile, 'w') as file:
            file.write(bigTxtFile)
        updateTxtFile = True


    if os.path.exists(txtFile) & (updateTxtFile == False): # If smaller textfile does not exist, read from big textfile
        with open(txtFile, 'r') as file:
            bigrams = file.read()
                    
        with open(txtFile, 'r') as file:
            for line in file:
                pureBigramArray.append(''.join(line[0:n_gramLength]))

        with open(txtFile, 'r') as file:
            for line in file:
                bigramImportance.append(int(line[n_gramLength+1:]))
        
    else:
        bigrams = ''
        for k in itertools.permutations(letters, n_gramLength):
            pureBigramArray.append(''.join(k).upper())
        for l in letters:
            pureBigramArray.append(l+l)

        for currentBigram in pureBigramArray:
            with open(bigTxtFile, 'r') as bbl:
                for line in bbl:
                    if currentBigram == line[0:n_gramLength]:
                        bigrams += line
                        bigramImportance.append(int(line[n_gramLength+1:]))
        with open(txtFile, 'w') as file:
            file.write(bigrams)

    with open(bigTxtFile, 'r') as file:
            for line in file:
                absoluteBigramCount.append(int(line[n_gramLength+1:]))

    absoluteBigramCount = sum(absoluteBigramCount)
    return bigrams, pureBigramArray, bigramImportance, absoluteBigramCount

def capitalizeList(list):
    if len(list) != 0:
        j=0
        # while j < len(firstLayerLetters):
        while j < len(list):
            list[j] = list[j].upper()
            j+=1
        return list

def prepareAsciiArray(firstLayerLetters, staticLetters):
    # This initializes the ascii-array.
    # It also creates the variable "emptySlots", which tells us what slots aren't filled by static letters.
    asciiArray = [255]*256
    emptySlots = [0]*8
    letterPlacement = 0
    j=0
    while letterPlacement < len(firstLayerLetters):
        if staticLetters[letterPlacement]:
            currentLetter = staticLetters[letterPlacement]
            asciiArray[ord(currentLetter)] = letterPlacement
        else:
            emptySlots[j] = letterPlacement
            j+=1
        letterPlacement += 1
    return asciiArray, emptySlots

def showDataInTerminal(layoutList, goodScoresList, badScoresList, sumOfALLbigrams, showData, showGeneralStats, showTopLayouts, showBottomLayouts):
    if showData:
        # Order the layouts. [0] is the worst layout, [nrOfLayouts] is the best.
        nrOfLayouts = len(layoutList)
        orderedLayouts = [layoutList for _,layoutList in sorted(zip(goodScoresList,layoutList))]
        sumOfBigramImportance = goodScoresList[0] + badScoresList[0]

        orderedGoodScores = goodScoresList.copy()
        orderedGoodScores.sort()

        orderedBadScores = badScoresList.copy()
        orderedBadScores.sort(reverse=True)

        if showTopLayouts != 0:
            j=nrOfLayouts-1
            print('\n')
            print('#######################################################################################################################')
            print('#######################################################################################################################')
            if showTopLayouts == 1:
                print('                                                       The King:')
            else:
                print('                                                The top', showTopLayouts, 'BEST layouts:')

            while j > nrOfLayouts-showTopLayouts-1:
                i = j
                print('\nLayout', layoutList.index(orderedLayouts[i])+1)
                print(orderedLayouts[i])

                print('Good bigrams:', orderedGoodScores[i], 'out of', sumOfBigramImportance,
                '  ~%.2f' % float(100*orderedGoodScores[i]/sumOfBigramImportance), '%')
                print('Bad  bigrams:', orderedBadScores[i], 'out of', sumOfBigramImportance, 
                '  ~%.2f' % float(100*orderedBadScores[i]/sumOfBigramImportance), '%')
                
                print('Layout-placing:', nrOfLayouts-i)
                j-=1

        if showBottomLayouts != 0:
            j=0
            print('#######################################################################################################################')
            print('#######################################################################################################################')
            if showBottomLayouts == 1:
                print('                                                   The WORST layout:')
            else:
                print('                                                The top', showBottomLayouts, 'WORST layouts:')
            while j < showBottomLayouts:
                i = showBottomLayouts-j
                print('\nLayout', layoutList.index(orderedLayouts[i])+1)
                print(orderedLayouts[i])

                print('Good bigrams:', orderedGoodScores[i], 'out of', sumOfBigramImportance,
                '  ~%.2f' % float(100*orderedGoodScores[i]/sumOfBigramImportance), '%')
                print('Bad  bigrams:', orderedBadScores[i], 'out of', sumOfBigramImportance, 
                '  ~%.2f' % float(100*orderedBadScores[i]/sumOfBigramImportance), '%')

                print('Layout-placing:', nrOfLayouts+1-i)
                j+=1

        if showGeneralStats:
            if (showTopLayouts == 0) & (showBottomLayouts == 0):
                print('\n')
                
            print('#######################################################################################################################')
            print('#######################################################################################################################')
            print('                                                    General Stats:')
            print('Number of Layouts tested:', nrOfLayouts)
            print('Number of Bigrams possible with this layout (regardless of Fluidity):',
                    sumOfBigramImportance, ' (', '~%.2f' % float(100*sumOfBigramImportance/sumOfALLbigrams), '%)')
            print('Sum of ALL Bigrams, if a whole keyboard was being used:', sumOfALLbigrams)
            print('"Average" Layout:', ' Good Bigrams:~%.2f' % float(100*statistics.mean(goodScoresList)/sumOfBigramImportance), '%',
                    '\n                   Bad Bigrams: ~%.2f' % float(100*statistics.mean(badScoresList)/sumOfBigramImportance), '%')
        print('#######################################################################################################################')
        print('########################################### 8vim Keyboard Layout Calculator ###########################################')
        print('#######################################################################################################################')

###########################################################################################
########################################## start ##########################################

# define the letters you want to use
firstLayerLetters = 'enirtsah'.upper() # All letters for the first cycle of calculation, including e (or whatever you put in >staticLetters<)
secondLayerLetters = 'dulcgmob'.upper() # All letters for the second cycle of calculation
thirdLayerLetters = ''.upper() # All letters for the second cycle of calculation

staticLetters = ['e', '', '', '', '', '', '', ''] # the positions go clockwise. 'e' is on the bottom left. 
staticLetters = capitalizeList(staticLetters)
variableLetters = getVariableLetters(firstLayerLetters, staticLetters)

# define bigram-stuff
n_gramLength = 2
tempTxtName = 'bigrams.txt'
bigBigramList = 'german_bigrams.txt'

# define what placement-combinations have a "good flow"
# 0 (the middle of this array) is assumed to be the position of the first letter. IT'S ASSUMED TO BE EVEN!!!
# +1 is one step clockwise. +2 is two steps clockwise. -1 is one step counterclockwise. -2 is two steps counterclockwise.
# Place the boolean values in a way that reflects how well the second letter follows after the first one.
#                  -7     -6     -5    -4     -3    -2    -1   ~0~     1      2      3     4      5     6     7
evenNumberFlow = [False, False, True, False, True, True, True, True, False, False, True, False, True, True, True]
oddNumberFlow = evenNumberFlow.copy()
oddNumberFlow.reverse()

# Define what information you want to recieve.
showData = False
showGeneralStats = False
nrOfTopLayouts = 1
nrOfBottomLayouts = 0

# create the asciiArray
asciiArray, emptySlots = prepareAsciiArray(firstLayerLetters, staticLetters)

# Get the bigram-lists
bigramList, pureBigramLetters, pureBigramImportance, sumOfALLbigrams = getBigramList(firstLayerLetters, n_gramLength, tempTxtName, bigBigramList)

nrOfPossibleLayouts = math.factorial(len(firstLayerLetters)-1)

goodgramList = [0]*nrOfPossibleLayouts
badgramList = [0]*nrOfPossibleLayouts

layoutList = ['']*nrOfPossibleLayouts
layoutIteration=0
for letterCombination in itertools.permutations(variableLetters): # try every layout
    i=0
    for letter in letterCombination:
        asciiArray[ord(letter)] = emptySlots[i]
        i+=1
    k=0
    for bigram in pureBigramLetters: # go through every bigram
        firstLetterPlacement = asciiArray[ord(bigram[0])]
        secondLetterPlacement = asciiArray[ord(bigram[1])]
        #if firstLetterPlacement+secondLetterPlacement > 63:
        #    print('Hhiiiiiiiiiiiiiiiiiiii', asciiArray)
        #print(asciiArray)

        if (firstLetterPlacement % 2) == 0: # if first letter of the bigram is EVEN, check the flowsWellArray
            flowsWell = evenNumberFlow[secondLetterPlacement - firstLetterPlacement + 7]
        else: # if it's ODD, check the reversed flowsWellArray
            flowsWell = oddNumberFlow[secondLetterPlacement - firstLetterPlacement + 7]

        if flowsWell: # if the bigram flows well, add it to the number of good-flowing-bigrams. Otherwise add it to the bad ones.
            goodgramList[layoutIteration] += pureBigramImportance[k]
        else:
            badgramList[layoutIteration] += pureBigramImportance[k]
        k+=1
    
    letterPlacement = 0
    m=0
    while letterPlacement < len(firstLayerLetters):
        if staticLetters[letterPlacement]:
            layoutList[layoutIteration] += staticLetters[letterPlacement]
        else:
            layoutList[layoutIteration] += letterCombination[m]
            m+=1
        letterPlacement += 1
    
    layoutIteration+=1
    ###  Un-comment this if you want only a certain number of tested layouts
    #if layoutIteration>1700:
    #    del layoutList[(layoutIteration - nrOfPossibleLayouts):nrOfPossibleLayouts]
    #    del badgramList[(layoutIteration - nrOfPossibleLayouts):nrOfPossibleLayouts]
    #    del goodgramList[(layoutIteration - nrOfPossibleLayouts):nrOfPossibleLayouts]
    #    break


showDataInTerminal(layoutList, goodgramList, badgramList, sumOfALLbigrams, showData, showGeneralStats, nrOfTopLayouts, nrOfBottomLayouts)

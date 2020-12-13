import os.path
import itertools
import math
import statistics
########################## what if the file is wrong?????????????????????????????????????????
########################## delete it and restart.
def getBigramList(firstLayerLetters, n_gramLength, txtFile, bigTxtFile):
    pureBigramArray = []
    bigramImportance = []
    absoluteBigramCount = []

    bigTxtFile = './bigram_dictionaries/' + bigTxtFile
    txtFile = './other input & output/' + txtFile
    previousFirstLayerLettersFile = './other input & output/' + 'previousFirstLayerLetters.txt'
    previousBigTxtFile = './other input & output/' + 'previousBigTxtFileName.txt'
    updateTxtFile = False

    if os.path.exists(previousFirstLayerLettersFile):
        with open(previousFirstLayerLettersFile, 'r') as file:
            if file.readline() == firstLayerLetters:
                print('Remember to take breaks if something hurts of thinking starts getting hard. :)')
            else:
                updateTxtFile = True
                with open(previousFirstLayerLettersFile, 'w') as file:
                    file.write(firstLayerLetters)
    else:
        with open(previousFirstLayerLettersFile, 'w') as file:
            file.write(firstLayerLetters)
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
        for k in itertools.permutations(firstLayerLetters, n_gramLength):
            pureBigramArray.append(''.join(k).upper())
        for l in firstLayerLetters:
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
        while j < len(firstLayerLetters):
            list[j] = list[j].upper()
            j+=1
        return list

def prepareAsciiArray(firstLayerLetters, firstLayerStaticLetters):
    asciiArray = [255]*256
    emptySlots = [0]*8
    letterPlacement = 0
    j=0
    while letterPlacement < len(firstLayerLetters):
        if firstLayerStaticLetters[letterPlacement]:
            currentLetter = firstLayerStaticLetters[letterPlacement]
            asciiArray[ord(currentLetter)] = letterPlacement
        else:
            emptySlots[j] = letterPlacement
            j+=1
        letterPlacement += 1
    return asciiArray, emptySlots

def showDataInTerminal(layoutList, goodScoresList, badScoresList, layoutNumber, showData, showGeneralStats, numberOfTopLayouts, numberOfBottomLayouts, numberOfALLbigrams):
    if showData:
        # Order the layouts. [0] is the worst layout, [layoutNumber] is the best.
        orderedLayouts = [layoutList for _,layoutList in sorted(zip(goodScoresList,layoutList))]
        sumOfBigramImportance = goodScoresList[0] + badScoresList[0]

        orderedGoodScores = goodScoresList.copy()
        orderedGoodScores.sort()

        orderedBadScores = badScoresList.copy()
        orderedBadScores.sort(reverse=True)

        if numberOfBottomLayouts != 0:
            print('\n')
            j=layoutNumber-1
            print('#######################################################################################################################')
            print('                                            The top', numberOfTopLayouts, 'BEST layouts:')
            while j > layoutNumber-numberOfTopLayouts-1:
                i = j
                print('\nLayout', layoutList.index(orderedLayouts[i])+1)
                print(orderedLayouts[i])

                print('Good bigrams:', orderedGoodScores[i], 'out of', sumOfBigramImportance,
                '  ~%.2f' % float(100*orderedGoodScores[i]/sumOfBigramImportance), '%')
                print('Bad  bigrams:', orderedBadScores[i], 'out of', sumOfBigramImportance, 
                '  ~%.2f' % float(100*orderedBadScores[i]/sumOfBigramImportance), '%')
                
                print('Layout-placing:', layoutNumber-i)
                j-=1

        if numberOfBottomLayouts != 0:
            j=0
            print('#######################################################################################################################')
            print('#######################################################################################################################')
            print('                                            The top', numberOfBottomLayouts, 'WORST layouts:')
            while j < numberOfBottomLayouts:
                i = numberOfBottomLayouts-j
                print('\nLayout', layoutList.index(orderedLayouts[i])+1)
                print(orderedLayouts[i])

                print('Good bigrams:', orderedGoodScores[i], 'out of', sumOfBigramImportance,
                '  ~%.2f' % float(100*orderedGoodScores[i]/sumOfBigramImportance), '%')
                print('Bad  bigrams:', orderedBadScores[i], 'out of', sumOfBigramImportance, 
                '  ~%.2f' % float(100*orderedBadScores[i]/sumOfBigramImportance), '%')

                print('Layout-placing:', layoutNumber-i)
                j+=1

        if showGeneralStats:
            if (numberOfTopLayouts == 0) & (numberOfBottomLayouts == 0):
                print('\n')
                
            print('#######################################################################################################################')
            print('#######################################################################################################################')
            print('                                                  General Stats:')
            print('Number of Layouts tested:', layoutNumber)
            print('Number of Bigrams possible with this layout (regardless of Fluidity):',
                    sumOfBigramImportance, ' (', '~%.2f' % float(100*sumOfBigramImportance/numberOfALLbigrams), '%)')
            print('Sum of ALL Bigrams, if a whole keyboard was being used:', numberOfALLbigrams)
            print('"Average" Layout:', ' Good Bigrams:~%.2f' % float(100*statistics.mean(goodScoresList)/sumOfBigramImportance), '%',
                    '\n                   Bad Bigrams: ~%.2f' % float(100*statistics.mean(badScoresList)/sumOfBigramImportance), '%')
            print('#######################################################################################################################')
            print('######################################### 8vim Keyboard Layout Calculator #############################################')
            print('#######################################################################################################################')

###########################################################################################
########################################## start ##########################################

# define the letters you want to use
firstLayerLetters = 'enirtsah'.upper() # All letters for the first cycle of calculation, including e (or whatever you put in >firstLayerStaticLetters<)
secondLayerLetters = 'dulcgmob'.upper() # All letters for the second cycle of calculation
thirdLayerLetters = ''.upper() # All letters for the second cycle of calculation

firstLayerStaticLetters = ['e', '', '', '', '', '', '', ''] # the positions go clockwise. 'e' is on the bottom left. 
firstLayerStaticLetters = capitalizeList(firstLayerStaticLetters)

variableLetters='' # This extracts the non-fix letters for the first layer.
j=0
while j < len(firstLayerLetters):
    if not firstLayerLetters[j] in firstLayerStaticLetters:
        variableLetters += firstLayerLetters[j]
    j+=1

# define bigram-stuff
n_gramLength = 2
tempTxtName = 'bigrams.txt'
bigBigramList = 'german_bigrams.txt'

# define what placement-combinations have a "good flow"
# 0 (the middle of this array) is assumed to be the position of the first letter. IT'S ASSUMED TO BE EVEN!!!
# +1 is one step clockwise. +2 is two steps clockwise. -1 is one step counterclockwise. -2 is two steps counterclockwise.
# Place the boolean values in a way that reflects how well the second letter follows after the first one.
#                      -7     -6     -5    -4     -3    -2    -1   ~0~     1      2      3     4      5     6     7
evenNumberFlow = [False, False, True, False, True, True, True, True, False, False, True, False, True, True, True]
oddNumberFlow = evenNumberFlow.copy()
oddNumberFlow.reverse()

# Define what information you want to recieve.
showData = False
showGeneralStats = True
numberOfTopLayouts = 3
numberOfBottomLayouts = 2

# create the asciiArray
asciiArray, emptySlots = prepareAsciiArray(firstLayerLetters, firstLayerStaticLetters)

# Get the bigram-lists
bigramList, pureBigramLetters, pureBigramImportance, numberOfALLbigrams = getBigramList(firstLayerLetters, n_gramLength, tempTxtName, bigBigramList)

numberOfPossibleLayouts = math.factorial(len(firstLayerLetters)-1)

goodgramList = [0]*numberOfPossibleLayouts
badgramList = [0]*numberOfPossibleLayouts

bestLayouts = ['']*10
bestScores = [0]*10
worstLayouts = ['']*5
worstScores = []*5

layoutList = ['']*numberOfPossibleLayouts
allScoresList = []*numberOfPossibleLayouts
layoutNumber=0
for variableLetterCombination in itertools.permutations(variableLetters): # try every layout
    i=0
    for letter in variableLetterCombination:
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
            goodgramList[layoutNumber] += pureBigramImportance[k]
        else:
            badgramList[layoutNumber] += pureBigramImportance[k]
        k+=1
    
    letterPlacement = 0
    m=0
    while letterPlacement < len(firstLayerLetters):
        if firstLayerStaticLetters[letterPlacement]:
            layoutList[layoutNumber] += firstLayerStaticLetters[letterPlacement]
        else:
            layoutList[layoutNumber] += variableLetterCombination[m]
            m+=1
        letterPlacement += 1
    
    layoutNumber+=1
    ### Un-comment this if you want only a certain number of tested layouts
    #if layoutNumber>1700:
    #    del layoutList[(layoutNumber - numberOfPossibleLayouts):numberOfPossibleLayouts]
    #    del allScoresList[(layoutNumber - numberOfPossibleLayouts):numberOfPossibleLayouts]
    #    del badgramList[(layoutNumber - numberOfPossibleLayouts):numberOfPossibleLayouts]
    #    del goodgramList[(layoutNumber - numberOfPossibleLayouts):numberOfPossibleLayouts]
    #    break


showDataInTerminal(layoutList, goodgramList, badgramList, layoutNumber, showData, showGeneralStats, numberOfTopLayouts, numberOfBottomLayouts, numberOfALLbigrams)

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
    if os.path.exists(txtFile): # If smaller textfile does not exist, read from big textfile
        with open(txtFile, 'r') as file:
            bigrams = file.read()
                    
        with open(txtFile, 'r') as file:
            for line in file:
                pureBigramArray.append(''.join(line[0:n_gramLength]))

        with open(txtFile, 'r') as file:
            for line in file:
                bigramImportance.append(int(line[n_gramLength+1:]))

        with open(bigTxtFile, 'r') as file:
            for line in file:
                absoluteBigramCount.append(int(line[n_gramLength+1:]))
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
                        print(currentBigram, line[n_gramLength+1:])
                    absoluteBigramCount.append(int(line[n_gramLength+1:]))
        with open(txtFile, 'w') as file:
            file.write(bigrams)

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

def flowsssssssssssssssWell(layout, bigram): # currently not in use
    n=0
    for letter in layout:
        if bigram[0] == letter:
            l1_placement = n
        elif bigram[1] == letter:
            l2_placement = n

    print(layout)

    if (l1_placement % 2) == 0: # if FIRST LETTER of the bigram is EVEN
        print('1')
        if (l2_placement % 2) != 0: # and if FIRST LETTER of the bigram is ODD
            #if
            print('2')
            return True
        #elif 

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
            print('"Average" Layout:', ' Good Bigrams:~%.2f' % float(statistics.mean(goodScoresList)/sumOfBigramImportance), '%',
                    '\n                   Bad Bigrams: ~%.2f' % float(statistics.mean(badScoresList)/sumOfBigramImportance), '%')
            print('#######################################################################################################################')
            print('######################################### 8vim Keyboard Layout Calculator #############################################')
            print('#######################################################################################################################')

###########################################################################################
########################################## start ##########################################

# define the letters you want to use
firstLayerLetters = 'etaoinsr'.upper() # All letters for the first cycle of calculation, including e (or whatever you put in >firstLayerStaticLetters<)
secondLayerLetters = 'dulcgmob'.upper() # All letters for the second cycle of calculation
thirdLayerLetters = ''.upper() # All letters for the second cycle of calculation
thirdLayerLetters = capitalizeList(thirdLayerLetters)

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
bigBigramList = 'english_bigrams.txt'

# define what placement-combinations have a "good flow"
# 0 (the middle of this array) is assumed to be the position of the first letter. IT'S ASSUMED TO BE EVEN!!!
# +1 is one step clockwise. +2 is two steps clockwise. -1 is one step counterclockwise. -2 is two steps counterclockwise.
# Place the boolean values in a way that reflects how well the second letter follows after the first one.
#                      -7     -6     -5    -4     -3    -2    -1   ~0~     1      2      3     4      5     6     7
evenNumberFlow = [False, False, True, False, True, True, True, True, False, False, True, False, True, True, True]
oddNumberFlow = evenNumberFlow.copy()
oddNumberFlow.reverse()

# Define what information you want to recieve.
showData = True
showGeneralStats = True
numberOfTopLayouts = 3
numberOfBottomLayouts = 2

# create the asciiArray
asciiArray, emptySlots = prepareAsciiArray(firstLayerLetters, firstLayerStaticLetters)
# asciiArray = [255]*256
# emptySlots = [0]*8
# letterPlacement = 0
# m=0
# while letterPlacement < len(firstLayerLetters):
#     if firstLayerStaticLetters[letterPlacement]:
#         currentLetter = firstLayerStaticLetters[letterPlacement]
#         asciiArray[ord(currentLetter)] = letterPlacement
#     else:
#         emptySlots[m] = letterPlacement
#         m+=1
#     letterPlacement += 1

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
        if (firstLetterPlacement % 2) == 0:
            # if first letter of the bigram is EVEN, check the flowsWellArray
            flowsWell = evenNumberFlow[secondLetterPlacement - firstLetterPlacement + 7]
        else: # check the reversed flowsWellArray
            flowsWell = oddNumberFlow[secondLetterPlacement - firstLetterPlacement + 7]
        # print(bigramList, flowsWell)
        #bigramPositionInFile = bigramList.find(bigram)
        #print(bigramPositionInFile)
        if flowsWell:
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
    
    #print('Layout', layoutNumber+1)
    #print(layoutList[layoutNumber])
    #print('Good bigrams:', goodgramList[layoutNumber], 'out of', sumOfBigramImportance, '  ~%.2f' % float(100*goodgramList[layoutNumber]/sumOfBigramImportance), '%')
    #print('Bad  bigrams:', badgramList[layoutNumber], 'out of', sumOfBigramImportance,  '  ~%.2f' % float(100*badgramList[layoutNumber]/sumOfBigramImportance), '%', '\n')

    layoutNumber+=1
    ### Un-comment this if you want only a certain number of tested layouts
    #if layoutNumber>1700:
    #    del layoutList[(layoutNumber - numberOfPossibleLayouts):numberOfPossibleLayouts]
    #    del allScoresList[(layoutNumber - numberOfPossibleLayouts):numberOfPossibleLayouts]
    #    del badgramList[(layoutNumber - numberOfPossibleLayouts):numberOfPossibleLayouts]
    #    del goodgramList[(layoutNumber - numberOfPossibleLayouts):numberOfPossibleLayouts]
    #    break


showDataInTerminal(layoutList, goodgramList, badgramList, layoutNumber, showData, showGeneralStats, numberOfTopLayouts, numberOfBottomLayouts, numberOfALLbigrams)
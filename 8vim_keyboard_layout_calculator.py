import os.path
import itertools
import math
#import statistics
import time
start_time = time.time()


def main():
    global n_gramLength
    global bigramTxt
    global debugMode

    global nrOfLettersInEachLayer
    global nrOfLayers
    global nrOfBestPermutations

    global flow_evenNumbers_L1
    global flow_oddNumbers_L1
    global flow_evenNumbers_L2
    global flow_oddNumbers_L2

    # Define the letters you want to use
    layer1letters = 'enirtsah'.lower() # All letters for the first cycle of calculation, including 'e' (or whatever you put in >staticLetters<)
    layer2letters = 'dulcgmob'.lower() # All letters for the second cycle of calculation
    layer3letters = ''.lower() # All letters for the second cycle of calculation

    # Define how which of the above letters are interchangeable (variable) between adjacent layers.
    # This has a drastic effect on performance. Time for computation skyrockets.
    # This is where the "======>  2 out of X cycles" come from.
    varLetters_L1_L2 = 'ahdu'.lower()
    varLetters_L2_L3 = ''.lower()


    # For layer 1, define that a certain Letter ('e') doesn't change.
    # Just pick the most common one in your language.
    # You can set it to other letters as well, it doesn't change anything about the quality of the layouts though.
    # IF 'e' IS NOT IN YOUR INNERMOST LAYER, PUT ANOTHER LETTER WHERE 'e' IS!!
    staticLetters = ['e', '', '', '', '', '', '', ''] # the positions go clockwise. 'e' is on the bottom left. 

    # Define how many layers the layouts you recieve should contain.
    nrOfLayers = 2
    # Define how many of the best layer-versions should be. This has a HUGE impact on how long this program will take, so be careful.
    nrOfBestPermutations = 2

    # Define what information you want to recieve.
    showData = True
    showGeneralStats = True
    nrOfTopLayouts = 2
    nrOfBottomLayouts = 0

    # Define bigram-stuff
    n_gramLength = 2
    bigramTxt = './bigram_dictionaries/german_bigrams.txt' # <- This is the main thing you want to change. Name it whatever your bigram is called.


    # Define what placement-combinations have a "good flow"
    # 0 (the middle of this array) is assumed to be the position of the first letter. IT'S ASSUMED TO BE EVEN!!!
    # ( = where the 'e' is in the current Layout)
    # +1 is one step clockwise. +2 is two steps clockwise. -1 is one step counterclockwise. -2 is two steps counterclockwise.
    # Place the boolean values in a way that reflects how well the second letter follows after the first one.
    #                       -7     -6     -5    -4     -3    -2    -1   ~0~     1      2      3     4      5     6     7
    flow_evenNumbers_L1 = [False, False, True, False, True, True, True, True, False, False, True, False, True, True, True]

    #                        -7     -6     -5    -4     -3    -2    -1   ~0~     1      2      3     4      5     6     7
    flow_evenNumbers_L2 = [False, True, False, False, True, False, True, True, False, True, False, False, True, False, True]



    # Unless you're trying out a super funky layout with more (or less) than 4 sectors, this should be 8.
    nrOfLettersInEachLayer = 8

    # Ignore this variable:
    debugMode = False


    ###########################################################################################################################
    ###########################################################################################################################
    ################################################### Start of the script ###################################################
    ###########################################################################################################################
    ############################## (There's no need to read or change anything after that line) ###############################
    ###########################################################################################################################
    ###########################################################################################################################

    staticLetters = lowercaseList(staticLetters)
    flow_evenNumbers_L1, flow_oddNumbers_L1 = getFlow(flow_evenNumbers_L1)
    flow_evenNumbers_L2, flow_oddNumbers_L2 = getFlow(flow_evenNumbers_L2)

    # Get the letters for the layers possible with the letters you specified.
    firstLayers, secondLayers = getLayers(layer1letters, layer2letters, varLetters_L1_L2)
    #secondLayers, thirdLayers = getLayers(layer2letters, layer3letters, varLetters_L2_L3)

    # Prepare variables for later.
    finalLayoutList = []
    finalGoodgramList = []
    finalBadgramList = []

    x=0
    for layer1letters in firstLayers:
        layer2letters = secondLayers[x]
        x+=1
        print ('\n======> ', x, 'out of', len(firstLayers), 'cycles')

        # create the asciiArray
        asciiArray, emptySlots = prepareAsciiArray(layer1letters, staticLetters)
        # get the letters in layer 1 that can actually move.
        varLetters = getVariableLetters(layer1letters, staticLetters)


        # Get all layouts for each Layer with the current layer-letters.
        layouts_L1, layouts_L2, layouts_L3 = getLayouts(varLetters, staticLetters, layer2letters, layer3letters)

        # Get the bigrams (two-letter-combinations) for Layer 1
        bigrams_L1, bigramFrequency_L1 = getBigramList(layer1letters)

        # Get the best layouts for layer 1
        bestLayouts_L1, bestScores_L1, WORSTSCORES_L1 = getBestPermutations(layouts_L1, asciiArray, bigrams_L1, bigramFrequency_L1, [], [], staticLetters, emptySlots)
        
        print("\n------------------------ %s seconds --- Got best layouts for layer 1" % round((time.time() - start_time), 2))
        if debugMode:
            print('\nBest Layouts of Layer 1:')
            for j in range(len(bestLayouts_L1)):
                print(j)
                print(bestLayouts_L1[j])
                print(bestScores_L1[j])
        
        
        # If the user says so, calculate the second layer.
        if nrOfLayers > 1:

            # Combine the layouts of layer 1 and layer 2 to all possible variants
            layouts_L1_L2 = combinePermutations(bestLayouts_L1, layouts_L2)

            # Combine the Letters for the layer 1 and layer 2
            lettersInL1_L2 = layer1letters + layer2letters
            if debugMode:
                print(lettersInL1_L2)

            # Get the bigrams for layer 1 & 2
            bigrams_L1_L2, bigramFrequency_L1_L2 = getBigramList(lettersInL1_L2)
            bigrams_L1_L2, bigramFrequency_L1_L2 = filterBigrams(layer2letters, bigrams_L1_L2, bigramFrequency_L1_L2)

            # Get the BEST LAYOUTS for the combined layouts of layer 1 and layer2
            bestlayouts_L1_L2, bestScores_L1_L2, WORSTSCORES_L1_L2 = getBestPermutations(layouts_L1_L2, asciiArray, bigrams_L1_L2, bigramFrequency_L1_L2, bestScores_L1, WORSTSCORES_L1)

            print("------------------------ %s seconds --- Got best layouts for layer 2" % round((time.time() - start_time), 2))            
            if debugMode:
                print('\nBest Layouts of Layer 1 and Layer 2:')
                for j in range(len(bestlayouts_L1_L2)):
                    print(j)
                    print(bestlayouts_L1_L2[j])
                    print(bestScores_L1_L2[j])


            # If the user says so, calculate the third layer.
            if nrOfLayers > 2:
                pass
            else:
                layoutList, goodgramList, badgramList = bestlayouts_L1_L2, bestScores_L1_L2, WORSTSCORES_L1_L2
        else:
            layoutList, goodgramList, badgramList = bestLayouts_L1, bestScores_L1, WORSTSCORES_L1

        for j in  range(len(layoutList)):
            # Add the found layouts to the list (which will later be displayed)
            finalLayoutList.append(layoutList[j])
            finalGoodgramList.append(goodgramList[j])
            finalBadgramList.append(badgramList[j])
            
    print("------------------------ %s seconds --- Done computing" % round((time.time() - start_time), 2))

    # Display the data in the terminal.
    sumOfALLbigrams = getAbsoluteBigramCount()
    showDataInTerminal(finalLayoutList, finalGoodgramList, finalBadgramList, sumOfALLbigrams, showData, showGeneralStats, nrOfTopLayouts, nrOfBottomLayouts)


def getLayers(layer1letters, layer2letters, varLetters_L1_L2):
    # This creates all possible layer-combinations with the letters you specified.
    # This includes "varLetters_L1_L2" and "varLetters_L2_L3"
    # It always returns a List (of strings).

    if varLetters_L1_L2: # Only do all this stuff if there actually exist variable letters.

        L1_Layers = []
        L2_Layers = []

        nrVarLetters_L1 = int(round(len(varLetters_L1_L2)/2))
        nrVarLetters_L2 = len(varLetters_L1_L2) - nrVarLetters_L1

        j=0
        for combination in itertools.permutations(varLetters_L1_L2): # Go through every combination of (variable) letters
            addCombination = True

            combination = ''.join(combination)
            varLetters_L1 = sorted(combination[:nrVarLetters_L1])
            varLetters_L1 = ''.join(varLetters_L1)

            for prevCombination in L1_Layers: # Scan for whether there already exists a versions of the same layer.
                if varLetters_L1 == prevCombination[-nrVarLetters_L1:]:
                    addCombination = False
                    break

            if addCombination: # Only add letter-combinations that are new.
                L1_LayerLetters = layer1letters[:-nrVarLetters_L1] + varLetters_L1 
                L2_LayerLetters = combination[nrVarLetters_L1:]+layer2letters[nrVarLetters_L2:]

                L1_Layers.append(L1_LayerLetters)
                L2_Layers.append(L2_LayerLetters)
                
                if debugMode:
                    print(L1_Layers[j], L2_Layers[j])

                j+=1
        return L1_Layers, L2_Layers

    else: # if there are no variable letters between layer 1 and 2, do nothing.
        return [layer1letters], [layer2letters]

def getVariableLetters(fullLayer, staticLetters):
    # This extracts the non-fix letters for the first layer.
    if staticLetters:
        varLetters='' 
        j=0
        while j < len(fullLayer):
            if not fullLayer[j] in staticLetters:
                varLetters += fullLayer[j]
            j+=1
    else:
        varLetters = fullLayer
    return varLetters

def getFlow(flowList):
    # This prepares the fow-list and its reverse for the rest of the program.

    flowList = enlargeList(flowList)

    reverseFlowList = flowList[:] # The flow-list for the letters at the odd positions (see beginning of program) is just the
    reverseFlowList.reverse()     # same thing, but reversed.

    return flowList, reverseFlowList

def enlargeList(flowList):
    # This makes the flowList larger, in accordance to the number of layers
    
    flowList_end = len(flowList)

    firstSlots_flowList = flowList[:nrOfLettersInEachLayer]
    lastslots_flowList = flowList[flowList_end-nrOfLettersInEachLayer:]
    
    j=0
    while j < nrOfLayers:
        flowList =  firstSlots_flowList + flowList + lastslots_flowList
        j+=1
    return flowList

def getBigramList(letters):
    # This opens the bigram-list (the txt-file) and returns the letters and the frequencies of the required bigrams.

    bigramArray = []
    bigramFrequency = []
    
    # Prepare the bigram-letters
    for bigram in itertools.permutations(letters, n_gramLength):
        bigramArray.append(''.join(bigram))
    for letter in letters:
        bigramArray.append(letter+letter)

    # Read the file for the frequencies of the bigrams.
    for currentBigram in bigramArray:
        with open(bigramTxt, 'r') as bbl:
            for line in bbl:
                line = line.lower()
                if currentBigram == line[0:n_gramLength]:
                    bigramFrequency.append(int(line[line.find(' ')+1:]))

    return bigramArray, bigramFrequency

def getAbsoluteBigramCount():
    # This returns the total number of all bigram-frequencies, even of those with letters that don't exist in the calculated layers.
    bigramFrequencies = []

    with open(bigramTxt, 'r') as file:
        for line in file:
            bigramFrequencies.append(int(line[line.find(' ')+1:]))
    absoluteBigramCount = sum(bigramFrequencies)

    return absoluteBigramCount

def filterBigrams(neededLetters ,bigrams, bigramFrequency):
    # This function trims the bigram-list to make getPermutations() MUCH faster.
    # It basically removes all the bigrams that were already tested. I'm amazing.
    
    trimmedBigrams = bigrams[:]

    j=0
    for bigram in bigrams: # Scan for redundant bigrams
        knockBigramOut = True
        for letter in neededLetters:
            if letter in bigram:
                knockBigramOut = False

        if knockBigramOut: # Remove the redundant bigrams
            trimmedBigrams.pop(j)
            bigramFrequency.pop(j)
            j-=1
        j+=1

    return trimmedBigrams, bigramFrequency

def lowercaseList(list):
    # This just takes any list and turns its uppercase letters into lowercase ones.
    if len(list) != 0:
        j=0
        while j < len(list):
            list[j] = list[j].lower()
            j+=1
        return list

def prepareAsciiArray(layer1letters, staticLetters):
    # This initializes the ascii-array.
    # It also creates the variable "emptySlots", which tells us what slots aren't filled by static letters. (in layer 1)
    asciiArray = [255]*256
    emptySlots = [0]*8
    letterPlacement = 0
    j=0
    while letterPlacement < len(layer1letters):
        if staticLetters[letterPlacement]:
            currentLetter = staticLetters[letterPlacement]
            asciiArray[ord(currentLetter)] = letterPlacement
        else:
            emptySlots[j] = letterPlacement
            j+=1
        letterPlacement += 1
    return asciiArray, emptySlots

def getLayouts(varLetters, staticLetters, layer2letters, layer3letters):
    # This calculates and returns all layouts.

    layer1layouts = getPermutations(varLetters, staticLetters)
    layer2layouts = ['']
    layer3layouts = ['']

    if layer2letters:
        layer2layouts = getPermutations(layer2letters)
    if layer3letters:
        layer3layouts = getPermutations(layer3letters)
    
    return layer1layouts, layer2layouts, layer3layouts

def getPermutations(varLetters, staticLetters=[]):
    # This returns all possible letter-positions (permutations) with the input letters.

    layouts = ['']*math.factorial(len(varLetters))

    if staticLetters: # this only activates for layer 1 (that has static letters)
        layoutIteration=0
        for letterCombination in itertools.permutations(varLetters): # try every layout
            letterPlacement = 0
            j=0
            while letterPlacement < nrOfLettersInEachLayer:
                if staticLetters[letterPlacement]:
                    layouts[layoutIteration] += staticLetters[letterPlacement]
                else:
                    layouts[layoutIteration] += letterCombination[j]
                    j+=1
                letterPlacement += 1
            layoutIteration+=1

    else: # This is used for all layers except for layer 1
        layoutIteration=0
        for letterCombination in itertools.permutations(varLetters): # try every layout
            layouts[layoutIteration] = ''.join(letterCombination)
            layoutIteration+=1

    return layouts

def getBestPermutations(layouts, asciiArray, bigrams, bigramFrequency, prevBestScores=None, prevWORSTScores=None, fixedLetters=None, emptySlots=None):
    # This calculates the best layouts and returns them (and their scores).

    goodgramList = [0]*len(layouts)
    badgramList = [0]*len(layouts)

    k=0
    for layout in layouts:

        if fixedLetters: # Fill up the asciiArray
            j=0
            while j < len(fixedLetters)-1:
                if fixedLetters[j]:
                    varLayout = layout.replace(fixedLetters[j],'')
                j+=1
            l=0
            for letter in varLayout:
                asciiArray[ord(letter)] = emptySlots[l]
                l+=1
        else:
            j=0
            for letter in layout:
                asciiArray[ord(letter)] = j
                j+=1
    
        j=0
        for bigram in bigrams: # go through every bigram
            firstLetterPlacement = asciiArray[ord(bigram[0])]
            secondLetterPlacement = asciiArray[ord(bigram[1])]

            if firstLetterPlacement < 8:
                if (firstLetterPlacement % 2) == 0: # if first letter of the bigram is EVEN, check the flowsWellArray
                    flowsWell = flow_evenNumbers_L1[secondLetterPlacement - firstLetterPlacement + 15]
                else: # if it's ODD, check the reversed flowsWellArray
                    flowsWell = flow_oddNumbers_L1[secondLetterPlacement - firstLetterPlacement + 15]
            else:
                if (firstLetterPlacement % 2) == 0: # if first letter of the bigram is EVEN, check the flowsWellArray
                    flowsWell = flow_evenNumbers_L2[secondLetterPlacement - firstLetterPlacement + 15]
                else: # if it's ODD, check the reversed flowsWellArray
                    flowsWell = flow_oddNumbers_L2[secondLetterPlacement - firstLetterPlacement + 15]

            if flowsWell: # if the bigram flows well, add it to the number of good-flowing-bigrams. Otherwise add it to the bad ones.
                goodgramList[k] += bigramFrequency[j]
            else:
                badgramList[k] += bigramFrequency[j]
            j+=1
        k+=1

    j=0
    while j < len(prevBestScores):
        layout_j_groupBeginning = int((len(layouts) / len(prevBestScores)) * j)
        layout_j_groupEnding = int((len(layouts) / len(prevBestScores)) * (j+1))
        
        k = layout_j_groupBeginning
        while k < layout_j_groupEnding:
            goodgramList[k] = goodgramList[k] + prevBestScores[j]
            badgramList[k] = badgramList[k] + prevWORSTScores[j]
            k+=1
        j+=1

        # haei=layout_j_groupBeginning
        # while haei < layout_j_groupEnding:
        #     print(j)
        #     print(haei)
        #     print(prevBestScores[j])
        #     print(layouts[haei])
        #     print(goodgramList[haei])
        #     print()
        #     haei+=999
        # j+=1

    
    # haei=0
    # while haei < len(layouts):
    #     print(layouts[haei])
    #     print(goodgramList[haei], '\n')
    #     haei+=2000


    orderedLayouts = [layouts for _,layouts in sorted(zip(goodgramList,layouts))]
    orderedGoodScores = goodgramList[:]
    orderedGoodScores.sort()
    orderedBadScores = badgramList[:]
    orderedBadScores.sort(reverse=True)

    bestLayouts = orderedLayouts[(len(orderedLayouts)-nrOfBestPermutations):]
    biggestGoodScores = orderedGoodScores[(len(orderedGoodScores)-nrOfBestPermutations):]
    smallestBadScores = orderedBadScores[(len(orderedBadScores)-nrOfBestPermutations):]

    return bestLayouts, biggestGoodScores, smallestBadScores

def combinePermutations(list1, list2):
    # This creates all possible permutations of two lists while still keeping them in the right order. (first, second) (a, then b)
    listOfStrings = []
    for a in list1:
        for b in list2:
            listOfStrings.append(a + b)
    return listOfStrings

def showDataInTerminal(layoutList, goodScoresList, badScoresList, sumOfALLbigrams, showData, showGeneralStats, showTopLayouts, showBottomLayouts):
    if showData:
        # Order the layouts. [0] is the worst layout, [nrOfLayouts] is the best.
        nrOfLayouts = len(layoutList)
        orderedLayouts = [layoutList for _,layoutList in sorted(zip(goodScoresList,layoutList))]
        sumOfBigramImportance = goodScoresList[0] + badScoresList[0]

        orderedGoodScores = goodScoresList[:]
        orderedGoodScores.sort()

        orderedBadScores = badScoresList[:]
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

                print('\nLayout:')#, layoutList.index(orderedLayouts[i])+1)
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
       #     print('"Average" Layout:', ' Good Bigrams:~%.2f' % float(100*statistics.mean(goodScoresList)/sumOfBigramImportance), '%',
       #             '\n                   Bad Bigrams: ~%.2f' % float(100*statistics.mean(badScoresList)/sumOfBigramImportance), '%')
        print('#######################################################################################################################')
        print('########################################### 8vim Keyboard Layout Calculator ###########################################')
        print('#######################################################################################################################')

main()
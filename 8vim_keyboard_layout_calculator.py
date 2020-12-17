import os.path
import itertools
import math
import statistics
import time
start_time = time.time()


def main():
    global n_gramLength
    global tempTxtName
    global bigBigramList

    global nrOfLettersInEachLayer

    global flow_EvenNumbers_L1
    global flow_OddNumbers_L1
    global flow_EvenNumbers_L2
    global flow_OddNumbers_L2

    global cachedTxt

    # Define the letters you want to use
    layer1letters = 'enirtsah'.lower() # All letters for the first cycle of calculation, including 'e' (or whatever you put in >staticLetters<)
    layer2letters = 'dulcgmob'.lower() # All letters for the second cycle of calculation
    layer3letters = ''.lower() # All letters for the second cycle of calculation

    # Define how which of the above letters are interchangeable (variable) between adjacent layers.
    # IT HAS TO BE AN EVEN NUMBER OF LETTERS. 0, 2, 4, 6, 8, 10, 12, 14 or 16. 
    varLetters_L1_L2 = 'ahdu'.lower()
    varLetters_L2_L3 = ''.lower()


    # For layer 1, define that a certain Letter ('e') doesn't change.
    # You can set it to other letters as well, it doesn't change anything about the quality of the layouts though.
    # IF 'e' IS NOT IN YOUR INNERMOST LAYER, PUT ANOTHER LETTER WHERE 'e' IS!!
    staticLetters = ['e', '', '', '', '', '', '', ''] # the positions go clockwise. 'e' is on the bottom left. 
    staticLetters = lowercaseList(staticLetters)


    # Define how many layers the layouts you recieve should contain.
    nrOfLayersToCalculate = 2
    # Define how many of the best layer-versions should be 
    nrOfBestPermutations = 10

    # Define bigram-stuff
    n_gramLength = 2
    tempTxtName = 'bigrams.txt'
    bigBigramList = 'german_bigrams.txt'
    cachedTxt = '' # <– do not change this one

    # Unless you're trying out a super funky layout with more (or less) than 4 sectors, this should be 8.
    nrOfLettersInEachLayer = 8

    # Define what placement-combinations have a "good flow"
    # 0 (the middle of this array) is assumed to be the position of the first letter. IT'S ASSUMED TO BE EVEN!!!
    # ( = where the 'e' is in the current Layout)
    # +1 is one step clockwise. +2 is two steps clockwise. -1 is one step counterclockwise. -2 is two steps counterclockwise.
    # Place the boolean values in a way that reflects how well the second letter follows after the first one.
    #                  -7     -6     -5    -4     -3    -2    -1   ~0~     1      2      3     4      5     6     7
    flow_EvenNumbers_L1 = [False, False, True, False, True, True, True, True, False, False, True, False, True, True, True]
    flow_EvenNumbers_L1 = enlargeList(flow_EvenNumbers_L1, nrOfLayersToCalculate)
    flow_OddNumbers_L1 = flow_EvenNumbers_L1.copy()
    flow_OddNumbers_L1.reverse()

    #                   -7     -6     -5    -4     -3    -2    -1   ~0~     1      2      3     4      5     6     7
    flow_EvenNumbers_L2 = [False, True, False, False, True, False, True, True, False, True, False, False, True, False, True]
    flow_EvenNumbers_L2 = enlargeList(flow_EvenNumbers_L2, nrOfLayersToCalculate)
    flow_OddNumbers_L2 = flow_EvenNumbers_L2.copy()
    flow_OddNumbers_L2.reverse()

    # Define what information you want to recieve.
    showData = True
    showGeneralStats = True
    nrOfTopLayouts = 10
    nrOfBottomLayouts = 0


    if nrOfBestPermutations < nrOfTopLayouts:
        nrOfTopLayouts = nrOfBestPermutations
    if nrOfBestPermutations < nrOfBottomLayouts:
        nrOfBottomLayouts = nrOfBestPermutations
    



    firstLayers, secondLayers = getLayers(layer1letters, layer2letters, varLetters_L1_L2)
    #secondLayers, thirdLayers = getLayers(layer2letters, layer3letters, varLetters_L2_L3)
    finalLayoutList = []
    finalGoodgramList = []
    finalBadgramList = []

    x=0
    for layer1letters in firstLayers:
        layer2letters = secondLayers[x]
        x+=1

        # create the asciiArray
        asciiArray, emptySlots = prepareAsciiArray(layer1letters, staticLetters)

        varLetters = getVariableLetters(layer1letters, staticLetters)



        # Get all layouts for each Layer with the current layer-letters.
        layouts_L1, layouts_L2, layouts_L3 = getLayouts(varLetters, staticLetters, layer2letters, layer3letters)
        print("\n------------------------ %s seconds --- layouts_L1 , layouts_L2, layouts_L3 done" % (time.time() - start_time))

        # Get the bigrams for Layer 1
        bigrams_L1, bigramFrequency_L1 = getBigramList(layer1letters)[1:]

        # Get the best layouts for layer 1
        bestLayouts_L1, bestScores_L1, WORSTSCORES_L1 = getBestPermutations(layouts_L1, asciiArray, bigrams_L1, bigramFrequency_L1, nrOfBestPermutations, [], [], staticLetters, emptySlots)
        print('\nBest Layouts of Layer 1:')
        for j in range(len(bestLayouts_L1)):
            print(j)
            print(bestLayouts_L1[j])
            print(bestScores_L1[j])
        
        
        # If the user says so, calculate the second layer.
        if nrOfLayersToCalculate > 1:

            # Combine the layouts of layer 1 and layer2 to all possible variants
            layouts_L1_L2 = combinePermutations(bestLayouts_L1, layouts_L2)
            print("\n------------------------ %s seconds --- Combined of the Layouts of Layer 1 and Layer2" % (time.time() - start_time))

            lettersInL1_L2 = layouts_L1_L2[0]
            print(lettersInL1_L2)
            # Get the bigrams for Layer 1 & 2
            bigrams_L1_L2, bigramFrequency_L1_L2 = getBigramList(lettersInL1_L2)[1:]
            # Remove the bigrams that are ONLY in layer 1
            bigrams_L1_L2, bigramFrequency_L1_L2 = filterBigrams(layer2letters, bigrams_L1_L2, bigramFrequency_L1_L2)
            print("\n------------------------ %s seconds --- Got bigrams for Layer 1 and Layer2" % (time.time() - start_time))

            # Get the BEST LAYOUTS for the combined layouts of layer 1 and layer2
            bestlayouts_L1_L2, bestScores_L1_L2, WORSTSCORES_L1_L2 = getBestPermutations(layouts_L1_L2, asciiArray, bigrams_L1_L2, bigramFrequency_L1_L2, nrOfBestPermutations, bestScores_L1, WORSTSCORES_L1)


            print("\n------------------------ %s seconds --- Got best permutations layouts_L1_L2" % (time.time() - start_time))
            print('\nBest Layouts of Layer 1 and Layer 2:')
            
            for j in range(len(bestlayouts_L1_L2)):
                print(j)
                print(bestlayouts_L1_L2[j])
                print(bestScores_L1_L2[j])

            # If the user says so, calculate the third layer.
            if nrOfLayersToCalculate > 2:
                pass
            else:
                layoutList, goodgramList, badgramList = bestlayouts_L1_L2, bestScores_L1_L2, WORSTSCORES_L1_L2
        else:
            layoutList, goodgramList, badgramList = bestLayouts_L1, bestScores_L1, WORSTSCORES_L1

        for j in  range(len(layoutList)):
            finalLayoutList.append(layoutList[j])
            finalGoodgramList.append(goodgramList[j])
            finalBadgramList.append(badgramList[j])

    sumOfALLbigrams = getAbsoluteBigramCount()
    showDataInTerminal(finalLayoutList, finalGoodgramList, finalBadgramList, sumOfALLbigrams, showData, showGeneralStats, nrOfTopLayouts, nrOfBottomLayouts)
    print("------------------------ %s seconds ---" % (time.time() - start_time))


def getLayers(layer1letters, layer2letters, varLetters_L1_L2):
    # This creates all possible layer-combinations with the letters you specified.

    if varLetters_L1_L2:

        L1_Layers = []
        L2_Layers = []
        #varLetters_L1_L2 = 'haeitrn'

        varLetterCombinations = []
        nrVarLetters_L1 = round(len(varLetters_L1_L2)/2)
        nrVarLetters_L2 = len(varLetters_L1_L2) - nrVarLetters_L1

        j=0
        for combination in itertools.permutations(varLetters_L1_L2):
            addTo_varLetterCombinations = True

            combination = ''.join(combination)
            varLetters_L1 = sorted(combination[:nrVarLetters_L1])
            varLetters_L1 = ''.join(varLetters_L1)

            for prevCombination in L1_Layers:
                if varLetters_L1 == prevCombination[-nrVarLetters_L1:]:
                    addTo_varLetterCombinations = False
                    break

            if addTo_varLetterCombinations:
                L1_LayerLetters = layer1letters[:-nrVarLetters_L1] + varLetters_L1 
                L2_LayerLetters = combination[nrVarLetters_L1:]+layer2letters[nrVarLetters_L2:]

                # varLetterCombinations.append(varLetters_L1+combination[nrVarLetters_L1:])
                L1_Layers.append(L1_LayerLetters)
                L2_Layers.append(L2_LayerLetters)
                
                print(L1_Layers[j], L2_Layers[j])
                j+=1
        return L1_Layers, L2_Layers

    else: # if there are no variable letters between layer 1 and 2, do nothing.
        return layer1letters, layer2letters

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

def enlargeList(flowList, nrOfLayers):
    
    j=0    
    flowList_end = len(flowList)
    firstSlots_flowList = flowList[:nrOfLettersInEachLayer]
    lastslots_flowList = flowList[flowList_end-nrOfLettersInEachLayer:]
    
    while j < nrOfLayers:
        flowList =  firstSlots_flowList + flowList + lastslots_flowList
        j+=1
    return flowList

def getBigramList(letters):
    bigramArray = []
    bigramFrequency = []

    bigTxtFile = './bigram_dictionaries/' + bigBigramList
    txtFile = './other input & output/' + tempTxtName
    previouslettersFile = './other input & output/' + 'previousletters.txt'
    previousBigTxtFile = './other input & output/' + 'previousBigTxtFileName.txt'
    updateTxtFile = False

    if os.path.exists(previouslettersFile):
        with open(previouslettersFile, 'r') as file:
            if file.readline() == letters:
                # print('Remember to take breaks if something hurts or thinking starts getting difficult. :)')
                pass
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
                # print('Still working on that one language ...')
                pass
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
                bigramArray.append(''.join(line[0:n_gramLength]))

        with open(txtFile, 'r') as file:
            for line in file:
                bigramFrequency.append(int(line[n_gramLength+1:]))
        
    else:
        for bigram in itertools.permutations(letters, n_gramLength):
            bigramArray.append(''.join(bigram))
        for letter in letters:
            bigramArray.append(letter+letter)

        bigrams = ''
        for currentBigram in bigramArray:
            with open(bigTxtFile, 'r') as bbl:
                for line in bbl:
                    line = line.lower()
                    if currentBigram == line[0:n_gramLength]:
                        bigrams += line
                        bigramFrequency.append(int(line[n_gramLength+1:]))
        with open(txtFile, 'w') as file:
            file.write(bigrams.lower())
        # with open(bigTxtFile, 'r') as bbl:
        #     for bigram in bigramArray:
        #         print(bigram)
        #         for line in bbl:
        #             line = line.lower()
        #             if bigram == line[0:n_gramLength]:
        #                 bigrams += line
        #                 bigramFrequency.append(int(line[n_gramLength+1:]))
        #                 break
        # with open(txtFile, 'w') as file:
        #     file.write(bigrams.lower())
    return bigrams, bigramArray, bigramFrequency

def getAbsoluteBigramCount():
    # This returns the total number of all bigram-frequencies, even of those with letters that don't exist in the calculated layers.
    absoluteBigramCount = []
    bigTxtFile = './bigram_dictionaries/' + bigBigramList
    with open(bigTxtFile, 'r') as file:
        for line in file:
            absoluteBigramCount.append(int(line[n_gramLength+1:]))
    absoluteBigramCount = sum(absoluteBigramCount)
    return absoluteBigramCount

def filterBigrams(neededLetters ,bigrams, bigramFrequency):
    # This function trims the bigram-list to make getPermutations() MUCH faster.
    # It basically removes all the bigrams that were already tested.
    trimmedBigrams = bigrams.copy()
    j=0
    for bigram in bigrams:
        knockBigramOut = True
        for letter in neededLetters:
            if letter in bigram:
                knockBigramOut = False
        if knockBigramOut:
            trimmedBigrams.pop(j)
            bigramFrequency.pop(j)
            j-=1
        j+=1

    return trimmedBigrams, bigramFrequency

def lowercaseList(list):
    if len(list) != 0:
        j=0
        # while j < len(layer1letters):
        while j < len(list):
            list[j] = list[j].lower()
            j+=1
        return list

def prepareAsciiArray(layer1letters, staticLetters):
    # This initializes the ascii-array.
    # It also creates the variable "emptySlots", which tells us what slots aren't filled by static letters.
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

    layer1layouts = getPermutations(varLetters, staticLetters)
    layer2layouts = ['']
    layer3layouts = ['']

    if layer2letters:
        layer2layouts = getPermutations(layer2letters)
    if layer3letters:
        layer3layouts = getPermutations(layer3letters)
    
    return layer1layouts, layer2layouts, layer3layouts
    #allLayouts = combinePermutations(layer1layouts, layer1or2layouts, layer2layouts, layer2or3layouts, layer3layouts)
    #return allLayouts

def getPermutations(varLetters, staticLetters=[]):
    layouts = ['']*math.factorial(len(varLetters))
    if staticLetters:
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
            ###  Un-comment this if you want only a certain number of tested layouts
            #if layoutIteration>1700:
            #    del layouts[(layoutIteration - nrOfPossibleLayouts):nrOfPossibleLayouts]
            #    del badgramList[(layoutIteration - nrOfPossibleLayouts):nrOfPossibleLayouts]
            #    del goodgramList[(layoutIteration - nrOfPossibleLayouts):nrOfPossibleLayouts]
            #    break
    else:
        layoutIteration=0
        for letterCombination in itertools.permutations(varLetters): # try every layout
            layouts[layoutIteration] = ''.join(letterCombination)
            layoutIteration+=1
    return layouts

def getBestPermutations(layouts, asciiArray, bigrams, bigramFrequency, nrOfBestPermutations, prevBestScores=None, prevWORSTScores=None, fixedLetters=None, emptySlots=None):
    
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
                    flowsWell = flow_EvenNumbers_L1[secondLetterPlacement - firstLetterPlacement + 15]
                else: # if it's ODD, check the reversed flowsWellArray
                    flowsWell = flow_OddNumbers_L1[secondLetterPlacement - firstLetterPlacement + 15]
            else:
                if (firstLetterPlacement % 2) == 0: # if first letter of the bigram is EVEN, check the flowsWellArray
                    flowsWell = flow_EvenNumbers_L2[secondLetterPlacement - firstLetterPlacement + 15]
                else: # if it's ODD, check the reversed flowsWellArray
                    flowsWell = flow_OddNumbers_L2[secondLetterPlacement - firstLetterPlacement + 15]

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
    orderedGoodScores = goodgramList.copy()
    orderedGoodScores.sort()
    orderedBadScores = badgramList.copy()
    orderedBadScores.sort(reverse=True)

    print(orderedGoodScores[0])
    print(orderedBadScores[0], '\n')
    
    print(goodgramList[0])

    print(badgramList[0], '\n')

    bestLayouts = orderedLayouts[(len(orderedLayouts)-nrOfBestPermutations):]
    biggestGoodScores = orderedGoodScores[(len(orderedGoodScores)-nrOfBestPermutations):]
    smallestBadScores = orderedBadScores[(len(orderedBadScores)-nrOfBestPermutations):]

    return bestLayouts, biggestGoodScores, smallestBadScores

def combinePermutations(list1, list2):

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


# def enlargeFlowList(flowList, nrOfLayers):
    
#     j=0
#     global flow_EvenNumbers_L1
#     global flow_EvenNumbers_L2
#     flowList_end = len(flow_EvenNumbers_L1)
#     #flow_EvenNumbers_L1 = flowList

#     if flow_EvenNumbers_L1:
#         firstSlots_flow_EvenNumbers_L1 = flow_EvenNumbers_L1[:nrOfLettersInEachLayer]
#         lastslots_flow__EvenNumbers_L1 = flow_EvenNumbers_L1[flowList_end-nrOfLettersInEachLayer:]
#         while j < nrOfLayers:
#             flow_EvenNumbers_L1 =  firstSlots_flow_EvenNumbers_L1 + flow_EvenNumbers_L1 + lastslots_flow__EvenNumbers_L1
#             j+=1
#     flow_EvenNumbers_L1 = flowList
#     return flowList

main()
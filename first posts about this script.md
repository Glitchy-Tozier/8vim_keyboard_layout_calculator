It's just the history of this (https://github.com/flide/8VIM/discussions/138) conversation. It's mostly me talking to myself though.
Some of the information, thought-processes and results may be outdated.

# Very first post
(Code: https://github.com/Glitchy-Tozier/8vim_keyboard_layout_calculator)

Hi, here's a preview of what's to come:
![8vim_preview](https://user-images.githubusercontent.com/59611881/101994263-607b9a80-3cc1-11eb-9329-bd53444d7983.png)

_______________________
A few thoughts I'd like to share:
## What can be calculated?
Trying out every single layout JUST FOR THE INNERMOST CIRCLE is possible. It's goes pretty fast actually. About 2 seconds. `5040` different Layouts. Easy.
However; When we look at the **two** innermost circles, what then can we calculate?

### We could try out ALL positions, regardless of what layer the letters belong in
In theory, this would be the best way of finding the optimal layout. You won't miss out on testing a single layout.
However, that method would surmount to the following number of possibilities:
```
15! = 15*14*13*12*11*…*4*3*2*1 = 1,307674368×10¹²
15! = 1.307.674.368.000
```
As you might have guessed, this WAY too much. (also, notice that we're still only talking about the 16 most common letters of a language. There's 10 more. Have fun calculating 26! possibilities!

### Fix letters to specific layers
A way to SHARPLY decrease the amount of possibilities is to say the following:
Always place the 8 most common letters in the innermost circle.
Always place letter 9-16 in the second layer.
Possibilities:
`7! * 8! = 203.212.800`
Way better, but still a lot. According to my (very rough) estimates, my laptop would need to run for about 80.000 seconds, or about a day to test through all of that.
Luckily, there's a way to make our live easier:

### Solution
- First, calculate all layouts ONLY for the innermost circle.
- Then, we take the – let's say 100 – best layouts we recieved…
- …and only for them try out all the possible second-layer-layouts.

This sums up to about
`7! + 100 * 8! =  4.037.040`

## My plan
This is what I'm aiming for:
Go for that last method. If that works fine…
- I might try to not only use 100, but 200 or 300 of the best layer-1 layouts.
- After layer 2, it's possible to continue the same thing for layer 3 and 4.
~ Layer 3 isn't that important though anymore, and placing the letters for layer 3 by hand should not be that big of a problem. I'll probably try to incorporate it anyways. Right now, my focus is on Layer 1 and 2 though.
~ Calculating anything for Layer 4 isn't worth the time. those letters have a EXTREMELY low frequencies (mostly lower than 0,1%). We can just manually place them (while of course still thinking of their most common bigrams)

_________________
#### Fun features
![8vim_preview3](https://user-images.githubusercontent.com/59611881/101994901-6627af00-3cc6-11eb-9604-478edb409956.png)
As you can see, it's very easy to compare layouts using this software. (The comparison still is being improved) That means, it'll be easy to check whether, for example, we should change the English layout.

#### German
The current tests are conducted for german. If there are any language-requests, I can try stuff out, if you give me the right data.

#### Data
Currently, I'm using this list of bigrams:
http://practicalcryptography.com/media/cryptanalysis/files/german_bigrams.txt
from this website:
http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/german-letter-frequencies/

They also have data on **other languages**: http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/
Also, their data is REALLY GOOD. Unfortunately they don't include special characters (like `,`, `.`, `!`, `?`, and `"`)... they have enormous samples though.
Their German corpus is about 1 billion characters. to put that into perspective, that's about 5000 books, WITH ABOVE AVERAGE LENGHT.
Their English corpus is even bigger.
Other languages they offer:  Danish, Finnish, French, Icelandic, Polish, Russian, Spanish, Swedish

If you want me to use any specific bigram-data, just tell me. Please make sure it's properly formatted though:
[bigram][space][how often the bigram appears in a text]


# Second post

Update: I can tell you the following:
The absolute worst **GERMAN** inner-circle-layouts are:
```
(3rd worst)
Layout 1662
ERIHNAST
Good bigrams: 14691419 out of 36226093   ~40.55 %
Bad  bigrams: 21534674 out of 36226093   ~59.45 % 

(2nd worst)
Layout 1611
ERISNATH
Good bigrams: 14348661 out of 36226093   ~39.61 %
Bad  bigrams: 21877432 out of 36226093   ~60.39 % 

(worst)
Layout 1661
ERIHNATS
Good bigrams: 14084606 out of 36226093   ~38.88 %
Bad  bigrams: 22141487 out of 36226093   ~61.12 %
```

Btw, the way the layout-names work is the following:
ERIHNATS = 
```
+—————————————————————————+
|   \  H           N  /   |
|  I  \             /  A  |
|       \         /       |
|         \     /         |
|           \ /           |
|           / \           |
|         /     \         |
|       /         \       |
|  R  /             \  T  |
|   /  E           S  \   |
+—————————————————————————+
```

Basically, that's how the positions work:
```
   \  3           4  /   
  2  \             /  5  
       \         /       
         \     /         
           \ /           
           / \           
         /     \         
       /         \       
  1  /             \  6  
   /  0           7  \   
```
Of course, those layouts can then be flipped or rotated and nothing changes about how good (or bad) they are.


# Third Post

## German Update
Okay.
Calculating the letters for Layer one is done. KEEP IN MIND, THOSE VALUES MIGHT CHANGE once calculating values for multiple layers.

That being said, here's some data :)

```
#######################################################################################################################
                                            The top 3 BEST layouts:

Layout 4029
EATRHINS
Good bigrams: 279207822 out of 362261187   ~77.07 %
Bad  bigrams: 83053365 out of 362261187   ~22.93 %
Layout-placing: 1

Layout 4750
EHTRAISN
Good bigrams: 277452507 out of 362261187   ~76.59 %
Bad  bigrams: 84808680 out of 362261187   ~23.41 %
Layout-placing: 2

Layout 4749
EHTRAINS
Good bigrams: 276679946 out of 362261187   ~76.38 %
Bad  bigrams: 85581241 out of 362261187   ~23.62 %
Layout-placing: 3
#######################################################################################################################
#######################################################################################################################
                                            The top 2 WORST layouts:

Layout 1662
ERIHNAST
Good bigrams: 146914363 out of 362261187   ~40.55 %
Bad  bigrams: 215346824 out of 362261187   ~59.45 %
Layout-placing: 5038

Layout 1611
ERISNATH
Good bigrams: 143486789 out of 362261187   ~39.61 %
Bad  bigrams: 218774398 out of 362261187   ~60.39 %
Layout-placing: 5039
#######################################################################################################################
#######################################################################################################################
                                                  General Stats:
Number of Layouts tested: 5040
Number of Bigrams possible with this layout (regardless of Fluidity): 362261187  ( ~39.57 %)
Sum of ALL Bigrams, if a whole keyboard was being used: 915463743
"Average" Layout:  Good Bigrams:~59 % 
                   Bad Bigrams: ~41 %
#######################################################################################################################
######################################### 8vim Keyboard Layout Calculator #############################################
#######################################################################################################################
```

## English update

Just for those interested, here's the results I get for the English language. Again, keep in mind those values are rough estimates.
While the following Layouts might be very good, the might not be the best ones overall. As I said, I'm still working on them.
```
#######################################################################################################################
                                            The top 3 BEST layouts:

Layout 3197
ENOSTRAI
Good bigrams: 1231752231 out of 1676972979   ~73.45 %
Bad  bigrams: 445220748 out of 1676972979   ~26.55 %
Layout-placing: 1

Layout 3131
ENOTIRAS
Good bigrams: 1231304219 out of 1676972979   ~73.42 %
Bad  bigrams: 445668760 out of 1676972979   ~26.58 %
Layout-placing: 2

Layout 2607
EINSOATR
Good bigrams: 1226914443 out of 1676972979   ~73.16 %
Bad  bigrams: 450058536 out of 1676972979   ~26.84 %
Layout-placing: 3
#######################################################################################################################
#######################################################################################################################
                                            The top 2 WORST layouts:

Layout 3813
ESANROTI
Good bigrams: 709532631 out of 1676972979   ~42.31 %
Bad  bigrams: 967440348 out of 1676972979   ~57.69 %
Layout-placing: 5038

Layout 4533
ERANSOTI
Good bigrams: 698586714 out of 1676972979   ~41.66 %
Bad  bigrams: 978386265 out of 1676972979   ~58.34 %
Layout-placing: 5039
#######################################################################################################################
#######################################################################################################################
                                                  General Stats:
Number of Layouts tested: 5040
Number of Bigrams possible with this layout (regardless of Fluidity): 1676972979  ( ~38.78 %)
Sum of ALL Bigrams, if a whole keyboard was being used: 4324127906
"Average" Layout:  Good Bigrams:~59 % 
                   Bad Bigrams: ~41 %
#######################################################################################################################
######################################### 8vim Keyboard Layout Calculator #############################################
#######################################################################################################################
```

I'm pretty happy with the way it turned out so far.  :)

For English (as well as for German), I used the top 8 most common letters. Depending on the source, the 8th most common letter might be `H` instead of `R`.
For those, This is the output:
```
#######################################################################################################################
                                            The top 3 BEST layouts:

Layout 3205
ENOSITAH
Good bigrams: 1219582549 out of 1625010561   ~75.05 %
Bad  bigrams: 405428012 out of 1625010561   ~24.95 %
Layout-placing: 1

Layout 2809
EIHOTANS
Good bigrams: 1213122507 out of 1625010561   ~74.65 %
Bad  bigrams: 411888054 out of 1625010561   ~25.35 %
Layout-placing: 2

Layout 344
ETIHOASN
Good bigrams: 1211725056 out of 1625010561   ~74.57 %
Bad  bigrams: 413285505 out of 1625010561   ~25.43 %
Layout-placing: 3
#######################################################################################################################
#######################################################################################################################
                                            The top 2 WORST layouts:

Layout 3916
ESONTIHA
Good bigrams: 682655773 out of 1625010561   ~42.01 %
Bad  bigrams: 942354788 out of 1625010561   ~57.99 %
Layout-placing: 5038

Layout 3794
ESANTOHI
Good bigrams: 658302239 out of 1625010561   ~40.51 %
Bad  bigrams: 966708322 out of 1625010561   ~59.49 %
Layout-placing: 5039
#######################################################################################################################
#######################################################################################################################
                                                  General Stats:
Number of Layouts tested: 5040
Number of Bigrams possible with this layout (regardless of Fluidity): 1625010561  ( ~37.58 %)
Sum of ALL Bigrams, if a whole keyboard was being used: 4324127906
"Average" Layout:  Good Bigrams:~59.14 % 
                   Bad Bigrams: ~40.86 %
#######################################################################################################################
######################################### 8vim Keyboard Layout Calculator #############################################
#######################################################################################################################
```
# Fourth Post
## Update:

The best layouts for TWO innermost layers now can be calculated.
Even more importantly, I changed pretty much the entire script so that the next few steps are **very easy** to implement. Those steps are:
0. (A little more cleaning up.)
1. Calculate 3 layers, not just 2. Originally, I didn't want to implement this, but it's so obvious and easy that it'd be a waste to stop now.
2. Implementing a finer control over what "flow" is.
Currently it's just a boolean. `Flow = True` / `Flow = False`.
Instead, I wand this: `Flow = 0.9` (out of 1)
3. Add a penalty for being in a higher layer. The penalty won't be very big, but It should prevent VERY common letters like 'e' in German and English to drop to something like the third layer.

Finally, a view into what happens in the command-window. The layout that's higher up is very good. It may not be the best though... we'll know once goals 2 and 3 are implemented.
If you want to help me, the best thing you can do is to go to this discussion and give me your answers to that little questionnaire: **https://github.com/flide/8VIM/discussions/140**

```
======>  1 out of 6 cycles

------------------------ 0.54 seconds --- Got best layouts for layer 1
------------------------ 21.42 seconds --- Got best layouts for layer 2

======>  2 out of 6 cycles

------------------------ 21.96 seconds --- Got best layouts for layer 1
------------------------ 42.8 seconds --- Got best layouts for layer 2

======>  3 out of 6 cycles

------------------------ 43.35 seconds --- Got best layouts for layer 1
------------------------ 64.12 seconds --- Got best layouts for layer 2

======>  4 out of 6 cycles

------------------------ 64.65 seconds --- Got best layouts for layer 1
------------------------ 85.82 seconds --- Got best layouts for layer 2

======>  5 out of 6 cycles

------------------------ 86.38 seconds --- Got best layouts for layer 1
------------------------ 107.29 seconds --- Got best layouts for layer 2

======>  6 out of 6 cycles

------------------------ 107.83 seconds --- Got best layouts for layer 1
------------------------ 128.38 seconds --- Got best layouts for layer 2
------------------------ 128.38 seconds --- Done computing


#######################################################################################################################
#######################################################################################################################
                                                The top 2 BEST layouts:

Layout:
eatrhinsbmcuodgl
Good bigrams: 555427171 out of 741644636   ~74.89 %
Bad  bigrams: 186217465 out of 741644636   ~25.11 %
Layout-placing: 1

Layout:
eutrhinsbmcaodgl
Good bigrams: 554255344 out of 741644636   ~74.73 %
Bad  bigrams: 187389292 out of 741644636   ~25.27 %
Layout-placing: 2
#######################################################################################################################
#######################################################################################################################
                                                    General Stats:
Number of Layouts tested: 12
Number of Bigrams possible with this layout (regardless of Fluidity): 741644636  ( ~81.01 %)
Sum of ALL Bigrams, if a whole keyboard was being used: 915463743
#######################################################################################################################
########################################### 8vim Keyboard Layout Calculator ###########################################
#######################################################################################################################
```
## Update:
Layers 1-4 now can be calculated. I also implemented a penalty for a letter being in a higher Layer and finer control over what movements are considered to have a good flow.
To-do's:
- Try implementing multiprocessing to make the program (hopefully) 4x as fast. This lets us calculate more layout-possibilities.
- What If a language needs really rare letters that don't exist in ascii?
- Once I know what the diacritics-movement will be, if necessary, add a mechanism to also test diacritics.
- Clean up and rename stuff.

# Fifth Post
(Code: https://github.com/Glitchy-Tozier/8vim_keyboard_layout_calculator)

So I created a small program, which can calculate the best layouts.

### Screenshot of what the results look like:
![results-shot](https://user-images.githubusercontent.com/59611881/103307486-76eb5b00-4a10-11eb-9d65-6a6ae70e70ae.png)


### To keep this post clean, here's a few links:
- Previous posts about this script (containing some of the thought-process): https://github.com/Glitchy-Tozier/8vim_keyboard_layout_calculator/blob/main/first%20posts%20about%20this%20script.md
- How the program's workflow works: https://github.com/Glitchy-Tozier/8vim_keyboard_layout_calculator/blob/main/Diagrams/How_the_layout_calculator_works.jpg
- You want to influence the future layouts? Please tell me what movements feel comfortable to you here: https://github.com/flide/8VIM/discussions/140

It is pretty much done! :)
The program can find layouts that are (probably) the best possible ones. ((you can never be 100% sure, unless you brute-force everything completely... which is too much work for a computer.

A few small things that still need to be done:
- Make program able create layouts that contain non-ASCII-characters
- Include the diacritics-gesture in the optimization.
- Clean up the code a little.
- Improve output for custom-tested layouts.

For now though, I'll leave it the way it is, until I have tested the layout it currently said was the best (German) one.

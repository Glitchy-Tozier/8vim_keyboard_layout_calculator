# How optimization works

Roughtly speaking, the optimizer uses the values in `config.py` to generate a list layouts, then tests them all. Atferwards, random letter-switches are being performed, and if the resulting layouts are better than already existing ones, they get added to the list of results.

A more detailed description:


## Layers 1 and 2
(The two innermost layers)
The following steps are performed for a particular set of first-layer-letters and second-layer-letters.

**Layer 1**: The optimizer...

1. generates a list of all possible **first** layers layouts and tests them.
1. keeps only the best X of these layouts.

**Layer 2**: The optimizer...

1. generates a list of all possible **second** layers layouts
1. combines all remaining **first** layers with all possible **second** layers. It then tests all these **first+second** layers layouts
1. keeps only the best X of these layouts.

If the config allows for certain letters to be swapped between layer 1 and 2, the process starts over again, performing the same operations for the new set of allowed first-layer-letters and second-layer-letters.


## Layer 3
The optimizer...

1. generates a list of all possible **third** layers layouts
1. combines all remaining **first+second** layers with all possible **third** layers. It then tests all these **first+second+third** layers layouts
1. keeps only the best X of these layouts.

Finally, random letter swaps are performed across each layout to generate and test for even better layouts. This is useful since the regular optimization doesn't allow letters to move between the **first+second** layer and the **third** layer.


## Layer 4
It's the same thing as happens in Layer 3. The optimizer...

1. generates a list of all possible **fourth** layers layouts
1. combines all remaining **first+second+third** layers with all possible **fourth** layers. It then tests all these **first+second+third+fourth** layers layouts
1. keeps only the best X of these layouts.

Finally, random letter swaps are performed across each layout to generate and test for even better layouts. This is useful since the regular optimization doesn't allow letters to move between the **first+second+third** layer and the **fourth** layer.

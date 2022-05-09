from copy import deepcopy


class BigramsConfig:
    def __init__(self, name: str, weight: float, path: str):
        self.name = name
        self.weight = weight
        self.path = path

    def fullWeightClone(self):
        """Copies [`self`] and sets its weight to 100"""
        copy = deepcopy(self)
        copy.weight = 100
        return copy


class ConfigSpecificResults:
    """The data for one or multiple [`BigramConfg`]s"""

    def __init__(self, name: str, weight: float, bigrams: tuple):
        self.name = name
        self.weight = weight
        self.bigrams = bigrams

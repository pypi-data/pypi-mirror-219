from scipy.stats import gmean
from itertools import chain
from .models import DecompoundingModel, download, load
from .utils import get_possible_splits, merge_prefix, merge_suffix
import re
import typing as t

#https://aclanthology.org/N16-1075/

class Decomposition: 
    def __init__(self, model: DecompoundingModel):
        self.model = model

    def decompose(self, word) -> t.List[str]:
        """
        Returns a list of tokens making up the word.
        """
        if word.lower() in self.model.precomputed_splits:
            return self.model.precomputed_splits[word.lower()]
        else:
            splits = get_possible_splits(word.lower(), self.model.generated_dictionary)
            suffix_prefix, prefix_suffix = self.merge_suffix_prefix(splits)
            compounds = self.get_compounds(word.lower(), splits, suffix_prefix, prefix_suffix)
            return compounds[0].resolve()
    
    def merge_suffix_prefix(self, splits) -> t.Tuple[t.List[int], t.List[int]]:
        suffix_prefix: t.List[int] = merge_suffix(splits, self.model.ml)
        suffix_prefix: t.List[int] = merge_prefix(suffix_prefix, self.model.ml)
        prefix_suffix: t.List[int] = merge_prefix(splits, self.model.ml)
        prefix_suffix: t.List[int] = merge_suffix(prefix_suffix, self.model.ml)
        return suffix_prefix, prefix_suffix

    def get_compounds(self, word, splits, suffix_prefix, prefix_suffix) -> list:
        compounds = ([
            Compounds([Compound((i,j), word.lower(), self.model) for i,j in zip(suffix_prefix, suffix_prefix[1:] + [max(splits)])]),
            Compounds([Compound((i,j), word.lower(), self.model) for i,j in zip(prefix_suffix, prefix_suffix[1:] + [max(splits)])])
            ])
        compounds: t.List[Compounds] = sorted(compounds, key=lambda c: c.score, reverse=True)
        return compounds

    def __repr__(self):
        return f"Decomposition({self.model.language})"
    
    @classmethod
    def load_model(cls, model_name):
        return load(model_name)
    
    @classmethod
    def download_model(cls, model_name, overwrite=False):
        return download(model_name, overwrite=overwrite)

class Compound:
    """
    Class to represente a compound. This class stores information about the span of the compound in the word,
    as well as its probability information.
    """
    def __init__(self, span: tuple, word: str, model: DecompoundingModel):
        self.span = span
        self.start = span[0]
        self.end = span[1]
        self.word = word.lower()
        self.compound = word[self.start:self.end]
        self.probability = model.calculate_probability(self.compound)

    def __repr__(self):
        return f"Compound({self.compound}, p={self.probability})"

class Compounds:
    """
    Class to calculate the joint probability of a list of compounds. 
    Takes a list of compounds instances as input and calculates its geometric mean
    """
    def __init__(self, compounds: list):
        self.compounds = compounds
        self.score = gmean([c.probability for c in self.compounds])
    
    def resolve(self):
        return [c.compound for c in self.compounds]
    
    def __repr__(self):
        return f"Compounds({','.join([c.compound for c in self.compounds])}, p={self.score})"
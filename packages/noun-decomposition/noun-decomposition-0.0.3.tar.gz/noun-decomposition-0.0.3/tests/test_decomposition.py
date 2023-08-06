# content of test_sysexit.py
import pytest
from Secos.Decomposition import Decomposition
from Secos.models import DecompoundingModel
from Secos.utils import get_possible_splits, merge_suffix, merge_prefix

vocab = ['Bund', 'Bunde', 'Bundes','finanz', 'minister', 'ministerium', 'Zuschauer', 'erwartung']

model = DecompoundingModel(
    language='German',
    precomputed_splits={},
    generated_dictionary=vocab,
    word_frequencies=dict(zip(vocab, [1]*len(vocab))),
    total_wordcount=100,
    n_words = 4,
    ml=3,
)

secos = Decomposition(model=model)

def test_split_indices(words = ['Bundesfinanzministerium', 'Zuschauererwartung'], 
                       splits = [[0, 4, 5, 6, 12, 20, 23],[0,9,18]]):
    for word, split in zip(words, splits):
        computed_splits = get_possible_splits(word, model.generated_dictionary)
        assert split == computed_splits

def test_probability_score():
    calculated_probability = model.calculate_probability('Bund')
    actual_probability = (1 + 0.001) / (100 + 0.001 * 4)
    assert actual_probability == calculated_probability
from importlib_resources import files

#https://devmount.github.io/GermanWordEmbeddings/

class DecompoundingModel:
    """
    Pretrained model to pass to Decompounding class. Holds data about the model used to compute splits.
    These include:
    language: 
    precomputed_splits: 
    generated_dictionary: 
    word_frequencies: ,
    total_wordcount: ,
    n_words: ,
    ml: ,
    epsilon: ,
    """
    def __init__(self, 
                 language: str, 
                 precomputed_splits: dict, 
                 generated_dictionary: list, 
                 word_frequencies: dict, 
                 total_wordcount: int, 
                 n_words: int, 
                 ml: int =3,
                 epsilon: float = 0.001, 
                 *args, 
                 **kwargs):
        self.language = language
        self.precomputed_splits = precomputed_splits
        self.generated_dictionary = set(generated_dictionary)
        self.word_frequencies = word_frequencies
        self.ml = ml
        self.total_wordcount = total_wordcount
        self.n_words = n_words
        self.epsilon = epsilon
    
    def calculate_probability(self, __name):
        prob = (self.word_frequencies.get(__name, 0) + self.epsilon) / (self.total_wordcount + self.epsilon * self.n_words)
        return prob

    def __repr__(self):
        return f"DecompoundingModel({self.language})"
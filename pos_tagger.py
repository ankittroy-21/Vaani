import nltk
from nltk.corpus import brown

print("Training the POS Tagger... This is a one-time process and might take a minute.")

# 1. Get a corpus of tagged sentences to train on. The Brown Corpus is a good general-purpose choice.
train_sents = brown.tagged_sents()

# 2. Define regular expression patterns for a RegexpTagger.
# This helps guess tags for words the other taggers haven't seen.
patterns = [
    (r'.*ing$', 'VBG'),               # Gerunds (e.g., "going")
    (r'.*ed$', 'VBD'),                # Simple past (e.g., "walked")
    (r'.*es$', 'VBZ'),                # 3rd singular present (e.g., "goes")
    (r'.*ould$', 'MD'),               # Modals (e.g., "could")
    (r'.*\'s$', 'NN$'),               # Possessive nouns (e.g., "child's")
    (r'.*s$', 'NNS'),                 # Plural nouns (e.g., "cars")
    (r'^-?[0-9]+(\.[0-9]+)?$', 'CD'),  # Cardinal numbers (e.g., "12", "-3.5")
    (r'.*', 'NN')                     # Default to noun
]

# 3. Create the sequence of taggers with backoff.
# We start with the most specific (Trigram) and back off to the most general (Default).
t0 = nltk.DefaultTagger('NN') # Default to a noun
t1 = nltk.UnigramTagger(train_sents, backoff=t0)
t2 = nltk.BigramTagger(train_sents, backoff=t1)
# You could even add a TrigramTagger for more context:
# t3 = nltk.TrigramTagger(train_sents, backoff=t2)

# The RegexpTagger is a great addition to the chain.
# We place it to back off to our n-gram tagger chain.
tagger = nltk.RegexpTagger(patterns, backoff=t2) 

print("POS Tagger trained and ready.")

def get_pos_tags(tokens):
    """
    Returns Part-of-Speech tags for a list of tokens using our trained backoff tagger.
    The input should be a list of words, e.g., ['what', 'is', 'the', 'price'].
    """
    return tagger.tag(tokens)
from nltk.corpus import wordnet as wn

def are_words_synonyms(word1, word2):
    """
    Checks if two words are synonyms by seeing if they share any synsets.
    """
    word1_synsets = wn.synsets(word1)
    if not word1_synsets:
        return False
        
    word2_synsets = wn.synsets(word2)
    if not word2_synsets:
        return False

    # Check for any overlap in the synset lists
    return bool(set(word1_synsets) & set(word2_synsets))

def command_contains_synonym(command_tokens, target_word):
    """
    Checks if any token in the user's command is a synonym of a target word.
    'command_tokens' should be a list of words.
    """
    target_synsets = wn.synsets(target_word)
    if not target_synsets:
        return False # The target word isn't in WordNet

    for token in command_tokens:
        token_synsets = wn.synsets(token)
        # Check if any of the token's meanings overlap with the target's meanings
        if set(token_synsets) & set(target_synsets):
            return True
    return False
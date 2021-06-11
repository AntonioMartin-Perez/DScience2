import nltk
import sys

TERMINALS = """
A -> "small" | "white"
N -> "cats" | "trees"
V -> "climb" | "run"
"""

NONTERMINALS = """
S -> NP V
NP -> N | A NP
"""

# NONTERMINALS = """
# S -> NP VP | S Conj S
# NP -> N | Det NP | P NP | Adj NP | NP Adv | NP NP
# VP -> V | V NP
# """

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            # print(np)
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = sentence.lower()
    wordList = nltk.word_tokenize(sentence)
    def alphanbetic_filter(string):
        return filter(str.isalpha, string)

    # print(wordList)

    for i in range(len(wordList)):
        wordList[i] = "".join(alphanbetic_filter(wordList[i]))
    
    cleanWordList = []
    for i in range(len(wordList)):
        if len(wordList[i]) != 0:
            cleanWordList.append(wordList[i])

    return cleanWordList
    # raise NotImplementedError

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    NPlist = []

    for s in tree.subtrees(lambda x: x.label() == "NP"):
        if len( list( s.subtrees(lambda y: y.label() == "NP"))) <= 1:
            NPlist.append(s)
        
        # Flatten resulting list
        # NPlist_flat = [item for sublist in NPlist for item in sublist]
    
    return NPlist
    # raise NotImplementedError


if __name__ == "__main__":
    main()



############################ TESTING #################

# sentence = "PRueB1412,!. d3 Fr4S3"
# print( preprocess(sentence) )
# w = "PRu3b4P4l4br4,!."
# w.isalpha()

# from nltk import Tree

# # t = Tree(1,[2,Tree(3,[4]),5])
# t = Tree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
# t.pretty_print()

# for s in t.subtrees():
#     print(s.label())
#     print("longitud del subarbol: ",len(s.subtrees()))

# for s in t.subtrees(lambda x: x.label() == "NP" and x.height() == 3):
#     print(s)
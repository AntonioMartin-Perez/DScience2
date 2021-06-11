import nltk
# nltk.download('stopwords')
import sys

import os
import string
import math

FILE_MATCHES = 1                # How many files should be matched to any given query
SENTENCE_MATCHES = 1            # How many sentences should be matched to any given query


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))                                          

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dic = {}
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            dic[filename] = f.read()
        
    return dic
    # raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # All words to lowercase
    document = document.lower()
    
    wordList = nltk.word_tokenize(document)
    wordListCopy = wordList.copy()

    setColon = {'\'\'','``' }
    for word in wordListCopy:
        # if not word.isalpha():
        #     print('!!')
        if word in string.punctuation or word in nltk.corpus.stopwords.words("english") or word in setColon or not word.isalpha():
            wordList.remove(word)          

        # if len(word) == 1:
        #     print(word)
        #     print(word.isalpha())

    return wordList
    # raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    IDFs = dict()

    allWords = dict()
    wordInEachDocument = dict()

    # Calculate frequencies accross documents and on each individual document
    for document in documents:
        wordInEachDocument[document] = set()
        for word in documents[document]:
            # Create a set of all individual words for a later all words loop.
            if word not in allWords:
                allWords[word] = 0
            # Create a set of individual words on each document
            if word not in wordInEachDocument[document]:
                wordInEachDocument[document].add(word)
                allWords[word] += 1

            # Inverse document frequency definition = ln(documents) / number of documents in which the word appears
            IDFs[word] = math.log( len(documents.keys()) ) / allWords[word]    

    return IDFs

    # raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # Clean up query to relevant words          -> Quizás no es necesario ya que tokeniza en la función main.
    queryWords = query

    # setColon = {'\'\'','``' }
    # for word in queryWords:
    #     if word in string.punctuation or word in nltk.corpus.stopwords.words("english") or word in setColon and word.isalpha():
    #         queryWords.remove(word)

    # Calculate term frequencies in each document
    frequencies = dict()                
    for filename in files:
        frequencies[filename] = dict()
        for word in queryWords:
            frequencies[filename][word] = 0
            for w in files[filename]:
                if w == word:
                    frequencies[filename][word] += 1
                
    # Calculate TF-IDFs
    tfIDFs = dict()
    for filename in files:
        tfIDFs[filename] = list()
        for word in queryWords:
            # tfIDF for individual words
            tfIDFs[filename].append(  frequencies[filename][word] * idfs[word] )

        # Document tfIDF
        tfIDFs[filename] = sum( tfIDFs[filename])
    
    # Ordenación decreciente
    tfIDFs = {key: value for key, value in sorted(tfIDFs.items(), key = lambda item: item[1], reverse = True)}
    tfIDFs = list(tfIDFs.keys())[0:n]

    return tfIDFs

    # raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    scoredSentences = dict()

    for sentence in sentences.keys():
        scoredSentences[ sentence ] = [0, 0]  # [IDF score , density]
        wordMatches = 0
        for word in sentences[ sentence ]:
            if word in query:
                wordMatches += 1
                scoredSentences[sentence][0] += idfs[word]
        scoredSentences[sentence][1] = wordMatches / len( sentences[sentence] )
    
    # Order by score
    # print(scoredSentences)
    orderedSentences = {key: value for key, value in sorted( scoredSentences.items(), key = lambda item: (item[1][0], item[1][1]), reverse = True)}
    # print(orderedSentences)

    # Select n top Sentences
    topSentences = list(orderedSentences.keys())[0:n]

    return topSentences
    # raise NotImplementedError


if __name__ == "__main__":
    main()


####################   Testing   #####################

# d = load_files('corpus')

# toc = tokenize(d['artificial_intelligence.txt'])

# dicToc = dict()
# for document in d:
#     dicToc[document] = tokenize(d[document])

# IDFs = compute_idfs(dicToc)
# # print(test)

# tfIDFs = top_files("ai, python",dicToc,IDFs,3)

# sentences =     {
#         'sentence1': ['modes', 'python'],
#         'sentence2': ['location', 'alleged'],
#         'sentence3': ['ai', 'python'],
#         'sentence4': ['modes', 'python','alleged'],
#     }


# scoredSentences = {
#     'sentence1': [1, 0.5], 
#     'sentence2': [2, 1.0], 
#     'sentence3': [3, 0.0],
#     'sentence4': [3, 0.5],
#     'sentence5': [3, 0.7],
#     }

# print({key: value for key, value in sorted( scoredSentences.items(), key = lambda item: (item[1][0], item[1][1]), reverse = True)})
# # print(topSentences)


# topSentences = top_sentences(
#     "ai, python",
#     sentences,
#     IDFs,
#     3
# )


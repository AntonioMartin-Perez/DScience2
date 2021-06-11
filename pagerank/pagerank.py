import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:                                  # Si no recuerdo mal sys.argv eran los argumentos con los que invocabas al programa
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])                             # Analiza el directorio de páginas y crea un diccionario con claves = página, valor = links de esa página
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)       # Esto es lo que tengo que implementar
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):  # Verificado con el ejemplo de la especificación
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pages = corpus.keys()

    distribution = {}

    for p in pages:
        distribution[p] = (1 - damping_factor) / len(pages)
        links = corpus[page]
        if p in links:
            distribution[p] +=  damping_factor /len(links)
    
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    PageRank = {}
    for page in corpus.keys():
        PageRank[page] = 0

    population = corpus.keys()
    first_sample = random.sample(population,1)[0]    # returns a list, hence [0]
    print('first sample = ',first_sample)
    for i in range(n):
        next_sample = random.choices(list(population), list(transition_model(corpus, first_sample, damping_factor).values()))[0]
        PageRank[next_sample] += (1 / n)
        first_sample = next_sample

    return PageRank


def iterate_pagerank_clean(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Parameters for convergence
    delta = 1000
    tolerance = 0.01

    PageRank = {}
    numPag = len(corpus.keys())
    # Initial uniform ranks
    for page in corpus.keys():
        PageRank[page] = 1/numPag

    # Loop until convergence
    while delta > tolerance:
        New_PageRank = {}
        # Loop to rank all pages
        for page in corpus.keys():
            sum_factor = 0
            # loop to find links directed to selected page
            for p in corpus.keys():
                if page in corpus[p]:
                    sum_factor += PageRank[p]/len(corpus[p])
            New_PageRank[page] = ( (1-damping_factor)/numPag ) + damping_factor * sum_factor
        
        # Update delta for breaking condition
        for p in PageRank.keys():
            increment = abs(PageRank[p]-New_PageRank[p])
            if increment < delta:
                delta = increment

        PageRank = New_PageRank.copy()

    return PageRank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Parameters for convergence
    delta = 1000
    tolerance = 0.0001

    PageRank = {}
    numPag = len(corpus.keys())
    # Initial uniform ranks
    for page in corpus.keys():
        PageRank[page] = 1/numPag
        
    # Loop until convergence
    while delta > tolerance:
        New_PageRank = {}
        # Loop to rank all pages
        for page in corpus.keys():
            # A page that has no links should be interpreted as one with a link for every page
            if len(corpus[page]) == 0:
                for otherpage in corpus.keys():
                    corpus[page].add(otherpage)

            sum_factor = 0
            # Loop to find links directed to selected page
            for p in corpus.keys():
                if page in corpus[p]:
                    sum_factor += PageRank[p]/len(corpus[p])
            New_PageRank[page] = ( (1-damping_factor)/numPag ) + damping_factor * sum_factor
        
        # Update delta for breaking condition
        increment = []
        for p in PageRank.keys():
            increment.append( abs(PageRank[p]-New_PageRank[p])  )
        if max(increment) < delta:
            delta = max(increment)

        PageRank = New_PageRank.copy()

    return PageRank
    # raise NotImplementedError


if __name__ == "__main__":
    main()



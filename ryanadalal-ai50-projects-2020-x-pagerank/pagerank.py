import os
import random
import re
import numpy
import copy
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
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

    print(pages)
    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    output = dict()
    if len(corpus[page]) == 0:
        for k in corpus.keys():
            output[k] = 1/len(corpus)

    for k in corpus.keys():
        output[k] = 1/len(corpus) * (1-damping_factor)
        if k in corpus[page] or len(corpus[page]) == 0:
            output[k] += 1/(len(corpus[page]) if len(corpus[page]) > 0 else len(corpus)) * damping_factor
    return output


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    result = dict()
    for k in corpus.keys():
        #each page rank starts out as 0 and each time the page is chosen the page rank will go up by 1/n
        result[k] = 0

    page = list(corpus.keys())[random.randint(0, len(corpus) - 1)]
    result[page] += 1/n

    for i in range(n - 1):
        tm = transition_model(corpus, page, damping_factor)
        option_list = list(tm.keys())
        weights = list(tm.values())
        page = numpy.random.choice(option_list, 1, p=weights)[0]
        result[page] += 1/n
    return result

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    result = dict()
    for k in corpus.keys():
        result[k] = 1/len(corpus)
    
    first = True
    count = 0
    while count < 100 or first:
        first = False
        previous = copy.deepcopy(result)
        for page in corpus.keys():
            linkers = getLinkingPages(corpus, page)
            result[page] = (1 - damping_factor)/len(corpus)
            addition = 0
            for p in linkers.keys():
                addition += result[p]/linkers[p]
            addition *= damping_factor
            result[page] += addition
        if (checkChange(previous, result)):
            count += 1
        else:
            count = 0
    return result
            
def getLinkingPages(corpus, page):
    result = dict()
    
    for k in corpus.keys():
        if page in corpus[k] or len(corpus[k]) == 0:
            result[k] = len(corpus[k]) if len(corpus[k]) > 0 else len(corpus)
    return result
     
def checkChange(past, current):
    for k in past.keys():
        if abs(past[k] - current[k]) > .001:
            return False
    return True

if __name__ == "__main__":
    main()

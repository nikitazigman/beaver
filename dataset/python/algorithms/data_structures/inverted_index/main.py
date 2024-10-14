from collections import defaultdict


def inverted_index(documents, stopwords=None):
    stopwords = stopwords or []
    index = defaultdict(lambda: set())
    for document in documents:
        words = document['data'].split()
        for word in words:
            if word in stopwords:
                continue
            index[word].add(document['id'])
    return index


def search(index, words):
    documents = [index[word] for word in words]
    return set.intersection(*documents)

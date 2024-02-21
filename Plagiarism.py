import re, string
import spacy
from spacy.util import filter_spans
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

# Note: Parts of this algorithm are adapted or implemented from the following two plagiarism detection projects:
# URL: https://github.com/AashitaK/Plagiarism-Detection/blob/master/notebook.ipynb
# URL: https://github.com/johnanisere/plagiarism_detector/blob/master/2_Plagiarism_Feature_Engineering.ipynb
# Credit goes to the original authors for their work.


def string_preprocessing(text_data):
    # for plagiarism algorithm 1
    '''remove "\n" "\r" and punctuations in raw texts and append filename and raw text in lists'''
    text_data = text_data.replace('\n', '').replace('\r', '')
    text_data = text_data.translate(str.maketrans('', '', string.punctuation)).lower()
    text_data = text_data.lstrip()
    # print(text_data)
    return text_data


def calculate_ngrams(n, e_text, s_text):
    # for plagiarism algorithm 1
    counts = CountVectorizer(analyzer='word', ngram_range=(n, n))
    ngram_array = counts.fit_transform([e_text, s_text]).toarray()
    # print("ngram array: ", ngram_array)
    return ngram_array


def containment(ngram_array):
    ''' Containment is a measure of text similarity. It is the normalized, intersection of ngram word counts in two texts.
       :param ngram_array: an array of ngram counts for an answer and source text.
       :return: a normalized containment value.'''
    # for plagiarism algorithm 1
    intersection = np.minimum(ngram_array[0], ngram_array[1]).sum()
    total_ngram_a = sum(ngram_array[0])
    cont = intersection / total_ngram_a
    # print("cont: ", cont)
    return cont


def calculate_containment(n, essay_text, source_text):
    '''Calculates the containment between a given essay text and its associated source text.
       This function creates a count of ngrams (of a size, n) for each text file in our data.
       Then calculates the containment by finding the ngram count for a given essay text,
       and its associated source text, and calculating the normalized intersection of those counts.
       :param n: An integer that defines the ngram size
       :return: A single containment value that represents the similarity
           between an essay text and its source text.
    '''
    # for plagiarism algorithm 1
    ngram_array = calculate_ngrams(n, essay_text, source_text)
    ctnmnt = containment(ngram_array)
    # print(ctnmnt)
    return ctnmnt


def get_tokens(text_data):
    # Get a list of tokens excluding stop words
    tokens = [token.text.replace('\n', '').replace('\r', '').strip() for token in text_data if
              not token.is_stop and not token.is_punct and token.text.strip()]
    # Filter out any remaining empty strings
    tokens = [token for token in tokens if token]
    return tokens

def get_trigrams(tokens):
    # Generate trigrams from the list of token texts
    trigrams = [' '.join(tokens[i:i + 3]) for i in range(len(tokens) - 2)]
    # Clean the trigrams by removing any potential empty trigrams or trigrams that only contain spaces
    trigrams = [trigram for trigram in trigrams if trigram.strip()]
    trigrams = set(trigrams)
    return trigrams

def Jaccard_similarity_coefficient(A, B):
    # for plagiarism algorithm 2
    J = len(A.intersection(B))/len(A.union(B))
    return J


def containment_measure(A, B):
    # for plagiarism algorithm 2
    if len(B) != 0:
        J = len(A.intersection(B))/len(B)
    else:
        J = 0
    return J


def LCS(A, B):
    # for plagiarism algorithm 2
    m, n = len(A), len(B)
    # print("m, n", m, n)
    counter = [[0]*(n+1) for x in range(m+1)]
    # print("counter_1", counter)
    A, B = list(A), list(B)
    # print("A", A)
    # print("B", B)
    longest = 0
    for i in range(m):
        for j in range(n):
            if A[i] == B[j]:
                count = counter[i][j] + 1
                # print("count", count)
                counter[i+1][j+1] = count
                # print("counter_2", counter)
                if count > longest:
                    longest = count
    # print("longest", longest)
    return longest

def plagiarism_features(input, input_doc, source, source_doc):

    input_text = string_preprocessing(input)
    source_text = string_preprocessing(source)

    result_dict = {}

    # Define an ngram range
    ngram_range = range(1, 7)

    # Calculate features for containment for ngrams in range
    i = 0
    for n in ngram_range:
        column_name = 'Containment_' + str(n) + "_score"
        # create containment features
        containment_score = calculate_containment(n, input_text, source_text)
        result_dict[column_name] = containment_score
        # print(column_name + ": ", containment_score)
        i += 1

    essay_token  = get_tokens(input_doc)
    source_token = get_tokens(source_doc)

    essay_trigram  = get_trigrams(essay_token)
    source_trigram = get_trigrams(source_token)

    Jaccard_similarity_score  = Jaccard_similarity_coefficient(source_trigram, essay_trigram)
    Containment_measure_score = containment_measure(source_trigram, essay_trigram)
    Longest_common_sequence   = LCS(source_token, essay_token)

    result_dict["Jaccard_similarity_score"] = Jaccard_similarity_score
    result_dict["Containment_measure_score"] = Containment_measure_score
    result_dict["Longest_common_sequence"] = Longest_common_sequence
    if len(essay_token) != 0:
        result_dict["Normed_longest_common_sequence"] = Longest_common_sequence / len(essay_token)
    else:
        result_dict["Normed_longest_common_sequence"] = "N/A"
    # print(result_dict)

    return result_dict

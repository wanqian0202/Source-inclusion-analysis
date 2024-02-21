import re, string
import numpy as np
from collections import Counter
from statistics import mean, stdev


def split_into_sentences(text):
    '''
    This function tokenize a string into sentences
    :param text: a string
    :return: sentences: a list of sentences
    '''
    alphabets = "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|Mt)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|me|edu)"

    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    if "..." in text: text = text.replace("...", "<prd><prd><prd>")
    if "......" in text: text = text.replace("......", "<prd><prd><prd><prd><prd><prd>")
    if "e.g." in text: text = text.replace("e.g.", "e<prd>g<prd>")
    if "i.e." in text: text = text.replace("i.e.", "i<prd>e<prd>")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    if len(sentences) == 0:
        sentences.append(text.strip())
    sentences = [ s for s in sentences if len(s) > 2 ]
    return sentences


def identify_citation(target):
    '''
    This function identify citations according to fixed format (e.g., Source A, (Source A))
    or keywords from the source text
    :return: lists: direct_citation, indirect_citation, all_citation_name
    '''

    keywords = ["source", "text", "article", "essay", "report", "blog", "post", "book", "chapter", "editorial",
                "excerpt", "interview", "journal", "lecture", "magazine", "newspaper", "paper", "passage",
                "quote", "research", "study", "speech", "website"]

    def citation_filter_1(target, expression):
        filtered_list = [s for s in expression.findall(target) if s.split()[1] != "I"]
        # print("list1: ", filtered_list)
        return filtered_list

    def citation_filter_2(expression):
        filtered_list_2 = [s for s in expression if
                           s.translate(str.maketrans('', '', string.punctuation)).split()[0].lower() in keywords]
        # print("list2: ", filtered_list_2)
        return filtered_list_2

    direct_list_1 = citation_filter_2(citation_filter_1(target, expression_1))
    direct_list_2 = citation_filter_2(citation_filter_1(target, expression_2))
    direct_list_3 = citation_filter_2(citation_filter_1(target, expression_3))
    direct_list_4 = citation_filter_2(citation_filter_1(target, expression_4))

    direct_list_5 = citation_filter_1(target, expression_5)
    direct_list_6 = citation_filter_1(target, expression_6)

    direct_citation = direct_list_1 + direct_list_2 + direct_list_3 + direct_list_4 + direct_list_5 + direct_list_6

    return direct_citation

def build_sent_dict(content):
    '''
    This function build dicts for each sentence in an essay, and the dicts contain info of:
    (1) the type of the sentence (citation/non-citation)
    (2) position of the sentence in the paragraph and in the essay
    :return: a list of dicts for all sentences in an essay
    '''

    def tokenize(content):
        '''
        This function tokenize the content of an essay into lists of paragraphs and sentences:
        [[sentence1, sentence2, sentence...][sentence1, sentence2, ...]]
        :return: content_list: list of paragraphs and sentences
        '''
        content_list = list(filter(bool, content.splitlines()))
        content_list = [para.strip() for para in content_list]
        content_list = [split_into_sentences(para) for para in content_list]
        return content_list

    sent_dict_list = []
    content_list = tokenize(content)

    # a list that directly comprised of sentences in the essay
    all_sent_list = [ sent for para in content_list for sent in para ]

    how_many_sent_in_essay = len(all_sent_list)
    how_many_para_in_essay = len(content_list)

    sent_no = 0
    # for each paragraph
    for i in range(len(content_list)):

        in_which_para = i + 1
        norm_para_position = in_which_para / how_many_para_in_essay
        # for each sentence
        for j in range(len(content_list[i])):

            sent_no += 1
            sent_dict = {}

            raw_location_in_para        = j + 1
            how_many_sent_in_para       = len(content_list[i])
            norm_sent_position_in_para = raw_location_in_para / how_many_sent_in_para
            raw_location_in_essay = sent_no
            norm_sent_position_in_essay = raw_location_in_essay / how_many_sent_in_essay
            # identify the type of the sentence: contain citations / not contain citations
            citation_all = identify_citation(content_list[i][j])

            if len(citation_all) != 0:
                sent_type = 'citation'
            else:
                sent_type = 'non-citation'

            # info about the sentence (type and position)
            sent_dict['sentence']                    = content_list[i][j]
            sent_dict['sent_type']                   = sent_type
            sent_dict['in_which_para']               = in_which_para
            sent_dict['how_many_para']               = how_many_para_in_essay
            sent_dict['norm_para_position']          = norm_para_position
            sent_dict['raw_location_in_para']        = raw_location_in_para
            sent_dict['how_many_sent_in_para']       = how_many_sent_in_para
            sent_dict['norm_sent_position_in_para']  = norm_sent_position_in_para
            sent_dict['raw_location_in_essay']       = raw_location_in_essay
            sent_dict['how_many_sent_in_essay']      = how_many_sent_in_essay
            sent_dict['norm_sent_position_in_essay'] = norm_sent_position_in_essay
            sent_dict_list.append(sent_dict)

    return sent_dict_list

def citation_sent_position(result_dict, input):
    '''
    This fuction calculate the position of citation sentences in the paragraph and in the essay
    :return: None (the function add in the positional info to the feature dict)
    '''

    def average_sentence_position(citation_data_list, number_unique_para, number_para):
        '''
        Calculate average sentence position of citations in paragraph and in the essay according the df of citations
        :param citation_df:
        :return: modified feature dict
        '''
        dataframe = np.array(citation_data_list)

        # calculate the means
        result_dict['average_raw_citation_sentence_location_in_essay']  = np.mean(dataframe, axis=0)[0]
        result_dict['average_norm_citation_sentence_location_in_essay'] = np.mean(dataframe, axis=0)[1]
        result_dict['average_raw_citation_sentence_location_in_para']   = np.mean(dataframe, axis=0)[2]
        result_dict['average_norm_citation_sentence_location_in_para']  = np.mean(dataframe, axis=0)[3]

        # calculate the SD of the position info, if citation number < 2 in an essay, fill SD value with "0"
        if len(citation_data_list) >= 2:
            result_dict['sd_raw_citation_sentence_location_in_essay']  = np.std(dataframe, axis=0)[0]
            result_dict['sd_norm_citation_sentence_location_in_essay'] = np.std(dataframe, axis=0)[1]
            result_dict['sd_raw_citation_sentence_location_in_para']   = np.std(dataframe, axis=0)[2]
            result_dict['sd_norm_citation_sentence_location_in_para']  = np.std(dataframe, axis=0)[3]
        else:
            result_dict['sd_norm_citation_sentence_location_in_essay'] = 0
            result_dict['sd_raw_citation_sentence_location_in_essay']  = 0
            result_dict['sd_raw_citation_sentence_location_in_para']   = 0
            result_dict['sd_norm_citation_sentence_location_in_para']  = 0
        # calculate how many percent of paragraphs contain citations
        result_dict['percentage_of_paragraphs_with_citations'] = number_unique_para / number_para

    sent_dict_list = build_sent_dict(input)
    # only extract info from the sentences that contain citations

    citation_data_list = []
    para_position_list = []
    number_para_list = []
    for sent_dict in sent_dict_list:
        if sent_dict['sent_type'] == 'citation':
            sent_position_list = []
            para_position_list.append(sent_dict['in_which_para'])
            number_para_list.append(sent_dict['how_many_para'])

            sent_position_list.append(sent_dict['raw_location_in_essay'])
            sent_position_list.append(sent_dict['norm_sent_position_in_essay'])
            sent_position_list.append(sent_dict['raw_location_in_para'])
            sent_position_list.append(sent_dict['norm_sent_position_in_para'])

            citation_data_list.append(sent_position_list)

    if len(citation_data_list) != 0:
        # # calculate average citation position in essay based on sentences
        number_unique_para = len(set(para_position_list))
        number_para = number_para_list[0]
        average_sentence_position(citation_data_list, number_unique_para, number_para)
    else:
        # if there is no citation in an essay at all, fill the positions with "0"
        result_dict['average_raw_citation_sentence_location_in_essay']  = 0
        result_dict['sd_raw_citation_sentence_location_in_essay']       = 0
        result_dict['average_norm_citation_sentence_location_in_essay'] = 0
        result_dict['sd_norm_citation_sentence_location_in_essay']      = 0

        result_dict['average_raw_citation_sentence_location_in_para']   = 0
        result_dict['sd_raw_citation_sentence_location_in_para']        = 0
        result_dict['average_norm_citation_sentence_location_in_para']  = 0
        result_dict['sd_norm_citation_sentence_location_in_para']       = 0
        result_dict['percentage_of_paragraphs_with_citations']          = 0

def citation_word_position(result_dict, content):
    '''
    This function calculate word-based position of citations in the essay
    :return: None (the function adds in the positional info to the feature dict)
    '''

    def replace_citations(rep, content):
        # replace the original mark of citations with a new mark that starts with "***"
        for citation, marked_citation in rep.items():
            content = content.replace(citation, marked_citation)
        # print(content)
        return content

    # get the direct and indirect citations in each essay
    direct_citation = identify_citation(content)
    direct_citation_set = set(direct_citation)
    direct_citation = list(direct_citation_set)
    # dicts that show how the mark of citations should be replaced
    rep = {citation: "***" + citation for citation in direct_citation}
    # replace the mark of citations in the essay
    if len(direct_citation) != 0:
        text = replace_citations(rep, content)
    else:
        text = content
    # remove parentheses in the essay
    text = text.replace('(', '').replace(')', '')
    # print(text)
    tokens = text.split()
    # get the position index of words that start with "***", which should be citations
    index = [i for i in range(len(tokens)) if tokens[i].startswith('***')]
    # calculate mean and SD of word-based position of citations in essay
    if len(index) > 0:
        result_dict["average_citation_word_location_in_essay"] = mean(index)
        if len(index) >= 2:
            result_dict["sd_citation_word_location_in_essay"]  = stdev(index)
        else:
            result_dict["sd_citation_word_location_in_essay"]  = 0
    else:
        result_dict["average_citation_word_location_in_essay"] = 0
        result_dict["sd_citation_word_location_in_essay"]      = 0


def citation_char_position(result_dict, content):
    '''
    This fuction calculate character-based position of citations and add the result to the feature dict
    :return: None (the function adds in the positional info to the feature dict)
    '''

    # get all character-based position indices of citations in an essay
    all_citations = identify_citation(content)
    all_char_position = []
    for s in set(all_citations):
        char_position = [m.start() for m in re.finditer(s, content)]
        for element in char_position:
            all_char_position.append(element)

    all_char_position = list(set(all_char_position))

    # calculate the mean and SD of the character-based position of citations in the essay
    if len(all_char_position) > 0:
        result_dict["average_citation_character_location_in_essay"] = mean(all_char_position)
        if len(all_char_position) >= 2:
            result_dict["sd_citation_character_location_in_essay"]  = stdev(all_char_position)
        else:
            result_dict["sd_citation_character_location_in_essay"]  = 0
    else:
        result_dict["average_citation_character_location_in_essay"] = 0
        result_dict["sd_citation_character_location_in_essay"]      = 0

def source_citation_coverage(result_dict, content):
    '''
    This function calculates percentages of most cited source, usage of sources, and the frequency of citations
    :return: None (the function adds in the frequency info to the feature dict)
    '''

    # get all citations in the essay
    direct_citation = identify_citation(content)
    number_citation = len(direct_citation)
    # number of citations in the essay
    result_dict["count_of_citations"] = number_citation

    # calculate the frequency of citations in the essays
    word_count = len(content.split())
    if word_count != 0:
        frequency_citation = number_citation / word_count
        result_dict["frequency_of_citations"] = frequency_citation
    else:
        result_dict["frequency_of_citations"] = 0

    # calculate the percentage of the most common cited source text,
    # and the percentage of how many source texts have been cited in the essay
    if number_citation != 0:
        cleaned_citation_list = [re.sub(r'[^\w\s]', '', citation.lower()) for citation in direct_citation]
        # print(cleaned_citation_list)
        citation_freq_dict = Counter(cleaned_citation_list)
        most_common_source  = citation_freq_dict.most_common(1)
        most_common_percent = most_common_source[0][1] / number_citation
        result_dict["percent_most_common_cited_source"] = most_common_percent

        citation_set      = set(cleaned_citation_list)
        type_citation     = len(citation_set)
        result_dict["number_of_unique_citations"] = type_citation
    else:
        result_dict["percent_most_common_cited_source"] = 0
        result_dict["number_of_unique_citations"]        = 0


def citation_features(input):

    global expression_1, expression_2, expression_3, expression_4, expression_5, expression_6

    expression_1 = re.compile(r"([a-zA-Z]+ [A-Z]) ")  # Letters A-Z
    expression_2 = re.compile(r"\([a-zA-Z]+\s[0-9]+\)", re.IGNORECASE)  # (Letters 0-9)
    expression_3 = re.compile(r"([a-zA-Z]+\s[0-9] )", re.IGNORECASE)  # Letters 0-9
    expression_4 = re.compile(r"\([a-zA-Z]+ [A-Z]\)", re.IGNORECASE)  # (Letters A-Z)
    expression_5 = re.compile(r"\([a-zA-Z]+ et al\., \d{4}\)", re.IGNORECASE)  # (Letters et al., 4-digit number)
    expression_6 = re.compile(r"\([a-zA-Z]+, \d{4}\)", re.IGNORECASE)  # (Letters, 4-digit number)

    result_dict = {}

    citation_sent_position(result_dict, input)
    citation_word_position(result_dict, input)
    citation_char_position(result_dict, input)
    source_citation_coverage(result_dict, input)
    # print("Citation result: ", result_dict)

    return result_dict








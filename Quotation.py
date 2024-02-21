import re

def quotation_features(input, input_doc, source):
    '''
    This fuction calculates the number and frequency of quotations
    and the number and percentage of quotations from the source texts
    :return: None (the function adds in the frequency info to the feature dict)
    '''

    result_dict = {}
    # identify quoted strings
    quotation_list   = re.findall(r"[\"](.*?)[\"]", input)
    quotation_str    = " ".join(quotation_list)
    quotation_length = len(quotation_str.split())
    # number of quoted words
    result_dict["number_of_quoted_words"] = quotation_length

    # ratio of quoted words
    # word_count = len(self._content.split())
    word_count = len(input_doc)
    if word_count != 0:
        result_dict["ratio_of_quoted_words"] = quotation_length / word_count
    else:
        result_dict["ratio_of_quoted_words"] = 0

    # calculate number of quotations from the source texts
    covered = 0
    for quotation in quotation_list:
        if quotation in source:
            covered += 1
    result_dict["number_quotations_from_source"] = covered
    # calculate percentage of quotations from the source texts
    if len(quotation_list) != 0:
        result_dict["percentage_quotations_from_source"] = covered / len(quotation_list)
    else:
        result_dict["percentage_quotations_from_source"] = 0

    # print(result_dict)
    return result_dict
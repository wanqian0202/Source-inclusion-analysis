import os, csv
import spacy
from Citation import citation_features
from Plagiarism import plagiarism_features
from Quotation import quotation_features

# Path to the folder containing the text files (files must be in .txt format)
texts_folder_path = 'path/to/texts_folder'

# Path to the source text file (in .txt format)
source_text_path  = 'path/to/source_text.txt'

# Path for the output CSV file
output_csv_path = 'path/to/output.csv'

final_result_list = []

# loading the english language model of spacy
nlp = spacy.load('en_core_web_md')
# Disable unnecessary components to speed up processing
nlp.disable_pipes('ner', 'parser')

# Read the source text and input texts from the folder
with open(source_text_path, 'r') as file:
    source_text = file.read()
    source_doc  = nlp(source_text)
for filename in os.listdir(texts_folder_path):
    if filename.endswith('.txt'):
        with open(os.path.join(texts_folder_path, filename), 'r') as file:
            text     = file.read()
            text_doc = nlp(text)
            print("File name: ", filename)
            # Process the text through each module
            citation_result   = citation_features(text)
            plagiarism_result = plagiarism_features(text, text_doc, source_text, source_doc)
            quotation_result  = quotation_features(text, text_doc, source_text)
            # Merge the result dictionaries
            merged_dict = {**citation_result, **plagiarism_result, **quotation_result}
            final_dict = {'Filename': filename, **merged_dict}
            final_result_list.append(final_dict)

headers = final_result_list[0].keys()

# Write the list of dictionaries to a CSV file
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    # Write the header
    writer.writeheader()
    # Write the rows
    for result_dict in final_result_list:
        writer.writerow(result_dict)

print(f'Processing complete. Results saved to {output_csv_path}')

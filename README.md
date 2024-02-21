## Paper Information

**Title:** Source Inclusion in Synthesis Writing: An NLP Approach

**Authors:** Scott Crossley, Qian Wan, Laura Allen, Danielle McNamara

**Publication Date:** November 11, 2021

**Journal:** Reading and Writing

**Pages:** 1-31

**Publisher:** Springer Netherlands

**Link to Paper:** https://files.eric.ed.gov/fulltext/ED619918.pdf

**Description:**
This repository contains code related to the study "Source Inclusion in Synthesis Writing: An NLP Approach to Understanding Argumentation, Sourcing, and Essay Quality" published in the Reading and Writing journal. Synthesis writing, a vital skill across domains, requires writers to integrate information from source materials. This study investigates how the integration of source material influences writing quality for synthesis tasks. Approximately 900 source-based essays, scored for holistic quality, argumentation, and source use, were analyzed using hand-crafted natural language processing (NLP) features. This repository provides access to the code used in the study, facilitating further research and exploration in the field of synthesis writing and NLP analysis.

## Setup Instructions

1. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt

2. **Update Paths:**
   - Open the `main.py` file in a text editor.
   - Ensure that the text files in the folder to be processed are in .txt format.
   - Specify the path to the folder containing the text files to be analyzed in the `main.py` file.
   - Specify the path to the source text file (currently, only one .txt file can be used as the source file) in the `main.py` file.
   - Specify the path for the output CSV file where the results will be stored in the `main.py` file.
   - Save the changes.

3. **Run the Code:**
- Run the `main.py` file to start the analysis.

# Text Analysis Assignment

## Objective
Extract textual data articles from given URLs and perform text analysis to compute variables.

## Files
- `text_analysis.py`: Python script to extract article text and perform text analysis.
- `output.xlsx`: Excel file with the computed variables for each article.
- `input.xlsx`: Input file with URLs of the articles.

## Instructions

### Dependencies
- Python 3.x
- pandas
- requests
- BeautifulSoup
- nltk

### How to Run the Script
1. Install the dependencies:
    ```bash
    pip install pandas requests beautifulsoup4 nltk
    ```

2. Download NLTK data:
    ```python
    import nltk
    nltk.download('punkt')
    ```

3. Place the following files in the same directory as the script:
    - `input.xlsx`
    - Folder containing stopword files: `StopWords`
    - Master dictionary files: `positive-words.txt` and `negative-words.txt` in the `MasterDictionary` folder

4. Run the script:
    ```bash
    python text_analysis.py
    ```

5. The script will generate `output.xlsx` with the computed variables for each article.

### Approach
1. **Data Extraction**: Extracted the article title and text from each URL.
2. **Text Analysis**: Performed text analysis to compute various variables such as positive score, negative score, polarity score, subjectivity score, average sentence length, percentage of complex words, fog index, average number of words per sentence, complex word count, word count, syllable per word, personal pronouns, and average word length.
3. **Output**: Saved the extracted text in text files named after the URL IDs and saved the computed variables in `output.xlsx`.

### Dependencies Required
- pandas
- requests
- BeautifulSoup
- nltk

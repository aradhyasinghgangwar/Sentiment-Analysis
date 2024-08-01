# THIS IS THE MAIN PYTHON FILE.




import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk

# Download NLTK data if not already available
nltk.download('punkt')

def syllable_count(word):
    word = word.lower()
    syllables = len(re.findall(r'[aeiouy]+', word))
    syllables -= len(re.findall(r'(es|ed)$', word))
    return max(1, syllables)

def load_words(file_path):
    encodings = ['utf-8', 'ISO-8859-1', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return set(file.read().split())
        except Exception as e:
            print(f"Error loading words from {file_path} with encoding {encoding}: {e}")
    return set()

def load_stopwords_from_folder(folder_path):
    stopwords = set()
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and file_path.endswith('.txt'):
            stopwords.update(load_words(file_path))
    return stopwords

# Load stop words from the StopWords folder
stop_words = load_stopwords_from_folder('C:\\Users\\Aradhya Singh\\Documents\\Sentiment Analysis\\StopWords')

# Load positive and negative words
positive_words = load_words('C:\\Users\\Aradhya Singh\\Documents\\Sentiment Analysis\\MasterDictionary\\positive-words.txt')
negative_words = load_words('C:\\Users\\Aradhya Singh\\Documents\\Sentiment Analysis\\MasterDictionary\\negative-words.txt')

def extract_article_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title_meta = soup.find('meta', property='og:title')
        title = title_meta['content'] if title_meta else 'No Title'
        
        article = soup.find('div', class_='td-ss-main-content')
        paragraphs = article.find_all('p') if article else []
        article_text = ' '.join([para.text for para in paragraphs])
        
        return title, article_text
    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return 'Error', ''

def analyze_text(text):
    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    
    cleaned_words = [word for word in words if word.isalpha() and word.lower() not in stop_words]
    cleaned_text = ' '.join(cleaned_words)
    
    positive_score = sum(1 for word in cleaned_words if word in positive_words)
    negative_score = sum(1 for word in cleaned_words if word in negative_words)
    
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(cleaned_words) + 0.000001)
    
    avg_sentence_length = len(words) / len(sentences)
    complex_words = [word for word in cleaned_words if syllable_count(word) > 2]
    percentage_complex_words = len(complex_words) / len(cleaned_words)
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    
    avg_words_per_sentence = len(words) / len(sentences)
    complex_word_count = len(complex_words)
    word_count = len(cleaned_words)
    syllables_per_word = sum(syllable_count(word) for word in cleaned_words) / len(cleaned_words)
    
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.I))
    avg_word_length = sum(len(word) for word in cleaned_words) / len(cleaned_words)
    
    return {
        'POSITIVE SCORE': positive_score,
        'NEGATIVE SCORE': negative_score,
        'POLARITY SCORE': polarity_score,
        'SUBJECTIVITY SCORE': subjectivity_score,
        'AVG SENTENCE LENGTH': avg_sentence_length,
        'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
        'FOG INDEX': fog_index,
        'AVG NUMBER OF WORDS PER SENTENCE': avg_words_per_sentence,
        'COMPLEX WORD COUNT': complex_word_count,
        'WORD COUNT': word_count,
        'SYLLABLE PER WORD': syllables_per_word,
        'PERSONAL PRONOUNS': personal_pronouns,
        'AVG WORD LENGTH': avg_word_length
    }

def main():
    # Read input URLs from input.xlsx
    input_df = pd.read_excel('input.xlsx')
    
    # Prepare the output DataFrame
    output_data = []

    for index, row in input_df.iterrows():
        url_id = row['URL_ID']
        url = row['URL']
        title, article_text = extract_article_text(url)
        
        # Save the extracted article text to a file
        with open(f'{url_id}.txt', 'w', encoding='utf-8') as file:
            file.write(f'{title}\n{article_text}')
        
        # Perform text analysis
        analysis = analyze_text(article_text)
        
        # Append to output data
        output_data.append({
            'URL_ID': url_id,
            'URL': url,
            **analysis
        })
    
    # Convert output data to DataFrame
    output_df = pd.DataFrame(output_data)
    
    # Save output DataFrame to output.xlsx
    output_df.to_excel('output.xlsx', index=False)

if __name__ == '__main__':
    main()

import nltk
from nltk.corpus import stopwords
from collections import Counter
import re

# Ensure you have the 'punkt' and 'stopwords' resources for nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')  # Add this line to download 'punkt_tab'

# Function to clean and tokenize text
def clean_and_tokenize(text):
    text = re.sub(r'\W+', ' ', text.lower())
    words = nltk.word_tokenize(text)
    return words

# Load common words from file
def load_common_words(common_words_path):
    with open(common_words_path, 'r') as f:
        common_words = set(line.strip().lower() for line in f)
    return common_words

# Load previously found rare words from file
def load_previous_rare_words(previous_rare_words_path):
    try:
        with open(previous_rare_words_path, 'r') as f:
            previous_rare_words = set(line.strip().lower() for line in f)
    except FileNotFoundError:
        previous_rare_words = set()
    return previous_rare_words

# Main function to find rare words
def find_rare_words_from_txt(txt_path, common_words_path, previous_rare_words_path, output_rare_words_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
    words = clean_and_tokenize(text)
    common_words = load_common_words(common_words_path)
    previous_rare_words = load_previous_rare_words(previous_rare_words_path)
    filtered_words = [
        word for word in words if word not in common_words and word not in previous_rare_words
        and word not in stopwords.words('english') and len(word) > 2 and not word.isdigit()
    ]
    word_freq = Counter(filtered_words)
    rare_words = word_freq.most_common()[:-101:-1]  # Get 100 rarest words

    # Append the list of rarest words to a txt file without overwriting it
    with open(output_rare_words_path, 'a', encoding='utf-8') as f:
        for word, freq in rare_words:
            if word not in previous_rare_words:
                f.write(f"{word}\n")
    print(f"100 rarest words appended to {output_rare_words_path}")

# Example usage
txt_path = 'extracted_text.txt'
common_words_path = 'google-10000-english-no-swears.txt'
previous_rare_words_path = 'rarest_words.txt'
output_rare_words_path = 'rarest_words.txt'
find_rare_words_from_txt(txt_path, common_words_path, previous_rare_words_path, output_rare_words_path)

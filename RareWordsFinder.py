import os
import nltk
import argparse
from nltk.corpus import stopwords
from collections import Counter
import re

# Ensure you have the 'punkt' and 'stopwords' resources for nltk
nltk.download('punkt')
nltk.download('stopwords')

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
def load_previous_rare_words(file_paths):
    previous_rare_words = set()
    for path in file_paths:
        try:
            with open(path, 'r') as f:
                previous_rare_words.update(set(line.strip().lower() for line in f))
        except FileNotFoundError:
            continue
    return previous_rare_words

# Load words from all .txt files in the 'Common Words' folder
def load_common_words_from_folder(folder_path):
    common_words = set()
    if os.path.exists(folder_path):
        txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        if not txt_files:
            print("Warning: 'Common Words' folder is empty. It's wise to add common word text files in that folder to avoid common words being outputted.")
        for txt_file in txt_files:
            with open(os.path.join(folder_path, txt_file), 'r') as f:
                common_words.update(set(line.strip().lower() for line in f))
    else:
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created. Please add common word text files to this folder.")
    return common_words

# Main function to find rare words
def find_rare_words_from_txt(previous_rare_words_paths, output_rare_words_path, percentage=100, begin_percentage=0):
    folder_path = 'Extracted Texts'
    common_words_folder = 'Common Words'
    
    # Check if the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created. Please add a text file and try again.")
        return

    # Get list of files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    # Check if there are multiple files in the folder
    if len(files) != 1:
        print("Error: There should be exactly one text file in the 'Extracted Texts' folder.")
        return

    txt_path = os.path.join(folder_path, files[0])
    
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
    words = clean_and_tokenize(text)
    
    # Calculate the starting and ending indices based on percentages
    start_index = int(len(words) * (begin_percentage / 100.0))
    end_index = int(len(words) * (percentage / 100.0))
    
    # Ensure the end index is within the length of the text
    end_index = min(end_index, len(words))
    words = words[start_index:end_index]
    
    previous_rare_words = load_previous_rare_words(previous_rare_words_paths)
    common_words = load_common_words_from_folder(common_words_folder)
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
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find rare words from text')
    parser.add_argument('-p', '--percentage', type=int, default=100, help='Percentage of the text to use (default: 100)')
    parser.add_argument('-b', '--begin_percentage', type=int, default=0, help='Percentage of the text to skip from the beginning (default: 0)')
    args = parser.parse_args()

    if args.percentage <= 0 or args.percentage > 100:
        print("Error: The percentage must be between 1 and 100.")
    elif args.begin_percentage < 0 or args.begin_percentage >= args.percentage:
        print("Error: The begin percentage must be between 0 and the specified percentage.")
    else:
        previous_rare_words_paths = ['rarest_words.txt', 'unknown_words.txt', 'known_words.txt']
        output_rare_words_path = 'rarest_words.txt'
        find_rare_words_from_txt(previous_rare_words_paths, output_rare_words_path, args.percentage, args.begin_percentage)

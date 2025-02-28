import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import os
import argparse

# Function to extract text from epub and clean it
def extract_text_from_epub(epub_path, output_txt_path, debug=False):
    book = epub.read_epub(epub_path)
    text = ""
    raw_text = ""
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            raw_text += str(soup)
            text += soup.get_text(separator=' ')
    
    # Clean the extracted text
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'\s+', ' ', text).strip()  # Remove excessive whitespace
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Text extracted to {output_txt_path}")
    
    # If debug mode is enabled, save the raw extracted content
    if debug:
        debug_output_path = f"{os.path.splitext(output_txt_path)[0]}_debug.txt"
        with open(debug_output_path, 'w', encoding='utf-8') as f:
            f.write(raw_text)
        print(f"Raw content extracted to {debug_output_path}")

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Extract and clean text from an EPUB file.')
parser.add_argument('--debug', action='store_true', help='Enable debug mode to save raw extracted content')
args = parser.parse_args()

# Ensure the "Epub book Here" folder exists
folder_path = 'Epub book Here'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Check for multiple .epub files
epub_files = [file for file in os.listdir(folder_path) if file.endswith('.epub')]
if len(epub_files) != 1:
    raise Exception("The folder must contain exactly one .epub file.")

# Process the single .epub file
epub_path = os.path.join(folder_path, epub_files[0])
output_folder = 'Extracted Texts'
os.makedirs(output_folder, exist_ok=True)
output_txt_path = os.path.join(output_folder, f"{os.path.splitext(epub_files[0])[0]}.txt")
extract_text_from_epub(epub_path, output_txt_path, debug=args.debug)

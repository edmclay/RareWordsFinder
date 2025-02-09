import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import os

# Function to extract text from epub and clean it
def extract_text_from_epub(epub_path, output_txt_path):
    book = epub.read_epub(epub_path)
    text = ""
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            # Remove header, footer, div, span tags
            for tag in soup.find_all(['header', 'footer', 'div', 'span']):
                tag.decompose()
            text += soup.get_text(separator=' ')
    
    # Remove numbers and clean the text further
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'\s+', ' ', text).strip()  # Remove excessive whitespace
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Text extracted to {output_txt_path}")

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
extract_text_from_epub(epub_path, output_txt_path)

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re

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

# Example usage
epub_path = 'pg1342-images.epub'
output_txt_path = 'extracted_text.txt'
extract_text_from_epub(epub_path, output_txt_path)

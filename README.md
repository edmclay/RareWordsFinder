# Rare Words Finder

This project is designed to help find rare words from a given text by comparing it against a list of common words.

## Files

You can add any text files containing frequently used words that need to be excluded from the list. This is optional.

Example URL link to a repository of frequently used English words: [GitHub - dwyl/english-words](https://github.com/dwyl/english-words)

## Usage

### Stage 1: Convert EPUB to TXT

1. Place the EPUB book you want to analyze in the `EPUB Books` directory.
2. Run the script to convert the EPUB book to a TXT file.
3. The converted TXT file will be placed in the `Extracted Texts` directory.

### Stage 2: Compare Against Common Words

1. Place the converted TXT file in the `Extracted Texts` directory.
2. Run the script to compare the text against the common words lists.
3. The script will output the rare words found in the text to `rarest_words.txt`.

### Stage 3: Sort Words Using GUI

1. Run the GUI script to load the `rarest_words.txt` file.
2. Use the GUI to sort the words into `known.txt` and `unknown.txt`.
3. Save the sorted lists for further analysis.

## Example

To find rare words in an EPUB book:

1. Place the EPUB book in the `EPUB Books` directory.
2. Run the script to convert the EPUB book to a TXT file.
3. Place the converted TXT file in the `Extracted Texts` directory.
4. Run the script to compare the text against the common words lists.
5. Check `rarest_words.txt` for the list of rare words.
6. Run the GUI script to sort the words into `known.txt` and `unknown.txt`.

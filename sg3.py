#! /usr/bin/env python3
"""
CMP SCI 4500: Intro to Software Profession
Project SG3
Project Start Date: 11/20/2025

Team Members:
Alan Zheng
Jamie Harris
Elena Miller
Hannah Smid
Xavian Kimbrough
Ryan Berry

IDE's used:
Neovim
Thonny
VSCode

Description:
This program processes up to 10 text files containing words. It parses each file
to extract valid words, tracks word counts, and allows users to search for specific
words across all files. The program displays formatted summaries of file statistics
and search results.

Revision History:
[10/20/2025]-[Alan]-[Reused SG2 Program & Updated Comments]

External Sources:
https://docs.python.org/3/library/re.html
https://stackoverflow.com/questions/48138015/printing-table-in-format-without-using-a-library-sqlite-3-python
https://www.w3schools.com/python/python_conditions.asp
https://stackoverflow.com/questions/65144347/how-create-summary-table-for-every-column
"""
import os
import re
import sys

max_input_files = 10
intro = (
    "This program will allow an input of up to 10 text files (.TXT).\n"
    "Each file will be parsed into separate words (Case-insensitive letters A-Z and optional hyphens are allowed)\n"
    "This program will display a total and a distinct word count per file.\n"
    "Words may be searched to see how many times they occur in each file.\n"
    "A summary table of all searches for all files will be displayed at the end."
)

outro = "Program has finished executing."

def extract_words(text):
    """
    Splits text into words while removing the line-break hyphens
    Returns an array of words.
    """
    #Remove hyphen and newline
    text = re.sub(r"-\n","", text)
    #Extract words (letters and hyphens)
    words_array = re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)*", text)
    return words_array

'''
call this in get_legal_word function according to SG1 specifications
If the user types in a string that contains any other characters,
SG1 should point out the FIRST problem in the string and politely reprompt
'''

def first_invalid_ch(word):
    """
    Returns the first character that isn't a letter (a-z) or hyphen '-'
    and returns none if all the characters are valid
    """

    legal = set("abcdefghijklmnopqrstuvwxyz-")
    for ch in word.lower():
        if ch not in legal:
            return ch
    return None

def get_legal_word():
    """
    Prompt the user for a legal word and give the definition of a legal word
    Rules for a legal word:
        -Only letters A-Z (case-insensitive)
        -Optional hyphens are allowed
        -No spaces, punctuation, or numbers allowed
    Returns the valid word (lowercased)
    """
    while True:
        print("Legal words may only contain letters (A-Z) and optional hyphens (-).\nA word is defined as a series of alphabetic characters, uninterrupted by a blank or a punctuation mark (excluding a hyphen).")
        word = input("Enter a legal word: ").strip()
        #Regex validates word based on rules
        if re.fullmatch(r"[A-Za-z]+(?:-[A-Za-z]+)*", word):
            return word.lower()
        else:
            invalid_char = first_invalid_ch(word)
            if invalid_char:
                print(f"Error: Invalid character '{invalid_char}' found. Word must only contain legal characters: abcdefghijklmnopqrstuvwxyz-")
            else:
                print("Error: Word must only contain legal characters: abcdefghijklmnopqrstuvwxyz-")

def ask_another_file():
    """
    Ask User if they want to add another file. Will accept Yes/No (Y/N) which is made case insensitive
    Loop until a valid response is given
    """
    while True:
        response = input("Do you want to add another file? (Yes/No): ").strip().lower()
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            return False
        else:
            print("Error: Please enter Yes, No, Y, or N.")
        
def ask_continue():
    """
    Ask user if they want to continue. Will accept Yes/No (Y/N) which is made case insensitive
    Loop until a valid response is given
    """
    while True:
        response = input("Do you want to continue? (Yes/No): ").strip().lower()
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            return False
        else:
            print("Error: Please enter Yes, No, Y, or N.")

def count_word(filenames, words_arrays, counted_word):
    """
    Counts words in word arrays for displaying total.
    Parameters:
        filenames - array of filenames
        words_arrays - array of word arrays
        counted_word - the word to count
    Returns list of [filename, count] pairs for each file
    """
    totals = []
    for index, words_array in enumerate(words_arrays):
        filename = filenames[index]
        total = sum(1 for word in words_array if word.lower() == counted_word.lower())
        totals.append([filename, total])
    return totals

#This checks if the filename ends with .TXT (case-insensitive)
def txt_filename(filename):
    name, extension = os.path.splitext(filename)
    return extension.upper() == ".TXT"

#This ask the user for a file and checks to make sure it hasn't been used already
#This also make sure the file is .TXT and exists in the directory
def prompt_for_filename(used_names):
    while True:
        filename = input("Please enter a file ending with .TXT: ").strip()
        if not txt_filename(filename):
            print("ERROR, filename must end in .TXT.")
        elif not os.path.isfile(filename):
            print("ERROR, this file doesn't exist in directory.")
        elif filename in used_names:
            print("ERROR, file has already been used.")
        else:
            return filename

def print_file_table(filenames, wordlists):
    """
    Print a table with:
    Filename, Total Words, and Distinct Words
    Parameters:
        filenames-  array of filenames (from user)
        wordlists - array of an array of words (extracted from files)
    """
    index = 0
    rows = []
    for filename, wordlist in zip(filenames, wordlists):
        total_words = len(wordlist)
        distinct_words = set(wordlist)
        row = [filename, total_words, len(distinct_words)]
        rows.append(row)

    # width of the colums
    columns = ["Filename ", "Total Words ", "Distinct Words"]
    col_widths = [len(c) for c in columns]
    for row in rows:
        for i, c in enumerate(row):
            col_widths[i] = max(len(str(c)), col_widths[i])

    row_format = ' '.join('{:>%d}' % width for width in col_widths)

    #header display
    print(row_format.format(*columns))
    print("-" * (sum(col_widths)+ 6))

    #rows display
    for row in rows:
        print(row_format.format(*row))

#This should keep the list of words that were extracted from the word_search_array
#This is for the end stats
def get_queried_words_from(word_search_array):
    seen = set()
    out = []
    for item in word_search_array:
        if isinstance(item, tuple) and item:
            w = str(item[0]).lower()
        else:
            w = str(item).lower()
        if w and w not in seen:
            seen.add(w)
            out.append(w)
    return out

#This is to create a table to present the specific words derived from the files
#This function also like the files and how many times that word is shown in each 
#of those files. This is for the end stats
def print_summary_words(queried_words, filenames, wordlists):
    if not queried_words:
        print("\nNo words were queried during this program run.")
        return

    # count occurences of each queried word in each of the files
    counts = []
    for w in queried_words:
        row = []
        for words in wordlists:
            cnt = sum(1 for x in words if x.lower() == w.lower())
            row.append(cnt)
        counts.append([w] + row)

    # makes headers for table
    columns = ["Word"] + filenames
    col_widths = [len(c) for c in columns]

    # adjust column widths according to data
    for row in counts:
        for i, c in enumerate(row):
            col_widths[i] = max(len(str(c)), col_widths[i])

    #format string
    row_format = ' '.join('{:>%d}' % width for width in col_widths)

    print("\nSummary of all words queried from files:\n")
    print(row_format.format(*columns))
    print("-" * (sum(col_widths) +2 * (len(columns) -1)))

    for row in counts:
        print(row_format.format(*row))
        
# function to build concordance
def build_concordance(filenames):
    concordance = {} #dictionary for concordance
    
    for file_num, filename in enumerate(filenames, start = 1):
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start = 1):
                #remove the line-break hyphen and split the text
                line = re.sub(r"-\n", "", line)
                words = re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)*", line)
                for word_num, word in enumerate(words, start = 1):
                    word_lower = word.lower()
                    location = f"{file_num}.{line_num}.{word_num}"
                    concordance.setdefault(word_lower, []).append(location)
                    
    #sort the dictionary alphabetically (hyphen comes before 'a')       
    sorted_concordance = dict(sorted(concordance.items(), key = lambda x: x[0].replace("-", " ")))
    return sorted_concordance

#Concordance function to write to txt file and print
def write_concordance(concordance):
    with open("CONCORDANCE.TXT", "w", encoding="utf-8") as f:
        for word, locations in concordance.items():
            line = f"{word} " + "; ".join(locations) + "."
            print(line)
            f.write(line + "\n")
            
#Function to build extra lists
def write_extra_lists(concordance_array, filenames, wordlists):
    all_words = list(concordance_array.keys())
    
    # top ten words
    word_counts = []
    for word in all_words:
        count = sum(w.lower() == word for wl in wordlists for w in wl)
        files_appeared = sum(1 for wl in wordlists if word in [w.lower() for w in wl])
        word_counts.append([word, count, files_appeared])
    word_counts.sort(key=lambda x: x[1], reverse=True)
    top_ten = word_counts[:10]

    # words appearing at least once in all files
    words_in_all = []
    for word in all_words:
        if all(word in [w.lower() for w in wl] for wl in wordlists):
            words_in_all.append(word)

    # words appearing only in one file
    words_in_one = []
    for word in all_words:
        file_indices = [i+1 for i, wl in enumerate(wordlists) if word in [w.lower() for w in wl]]
        if len(file_indices) == 1:
            words_in_one.append([word, file_indices[0]])

    # Write to file and print to screen
    with open("ExtraLists.txt", "w", encoding="utf-8") as f:
        # top ten words
        header1 = "1. TOP TEN WORDS (Word | Total | Files Appeared In)"
        print(header1)
        f.write(header1 + "\n")
        for word, count, files_appeared in top_ten:
            line = f"{word:>15} {count:>10} {files_appeared:>10}"
            print(line)
            f.write(line + "\n")
        print()
        f.write("\n")

        # words appearing at least once in all files
        header2 = "2. WORDS APPEARING AT LEAST ONCE IN ALL FILES:"
        print(header2)
        f.write(header2 + "\n")
        for word in words_in_all:
            line = f"{word:>15}"
            print(line)
            f.write(line + "\n")
        print()
        f.write("\n")

        # words appearing only in one file
        header3 = "3. WORDS APPEARING IN ONLY ONE FILE (Word | File Number):"
        print(header3)
        f.write(header3 + "\n")
        for word, file_num in words_in_one:
            line = f"{word:>15} {file_num:>10}"
            print(line)
            f.write(line + "\n")


#Main Function
def main():
    print(intro)

    #Array initialization for filenames and word lists for each file
    filenames_array = [] 
    all_words_array = [] 
    word_search_array = []
    
    #file input requiring a minimum of one, and accepting up to 9 more (10 total no duplicates)
    print("Enter at least one .TXT file")
    
    #repeat file process until max is at 10 or user says no
    addFile = True
    while addFile == True:
        filename = prompt_for_filename(filenames_array)
        file_index = len(filenames_array)
        filenames_array.append(filename) # add filename to array
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
        wordlist =  extract_words(text)
        all_words_array.append(wordlist)
        #file total files reach 10, exit loop
        if file_index < (max_input_files-1):
            addFile = ask_another_file()
        else:
            addFile = False
    
    #print formatted table
    print_file_table(filenames_array, all_words_array)
    
    continueWordCount = True
    while continueWordCount == True:
        legal_word = get_legal_word()
        totals = count_word(filenames_array, all_words_array, legal_word)
        
        #print results for this word
        print(f"\nSearch results for '{legal_word}':")
        for filename, count in totals:
            print(f"  {filename}: {count} occurrence(s)")
        
        word_search_array.append((legal_word, totals))
        continueWordCount = ask_continue()

    #This is to call for the table that shows specific words 
    #and their count in files for the end stats
    queried_words_lc = get_queried_words_from(word_search_array)
    print_summary_words(queried_words_lc, filenames_array, all_words_array)
    
    # SG2 extension
    # concordance
    print ("\nBuilding Concordance and Extra Lists...\n")
    concordance = build_concordance(filenames_array)
    write_concordance(concordance)
    write_extra_lists(concordance, filenames_array, all_words_array)
   
    print("\nConcordance written to CONCORDANCE.TXT!")
    print("\nExtra lists written to ExtraLists.txt!")
    
    print(outro)
    input("\nPress Enter/Return to exit...")
    #exit program after displaying summary
    sys.exit(0)

if __name__ == "__main__":
    main()

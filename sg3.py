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
[12/01/2025]-[Elena]-[Added initial GUI framework and interface classes]
[12/02/2025]-[Hannah]-[Implemented the SG3 code into the SG2 base]

External Sources:
https://docs.python.org/3/library/re.html
https://stackoverflow.com/questions/48138015/printing-table-in-format-without-using-a-library-sqlite-3-python
https://www.w3schools.com/python/python_conditions.asp
https://stackoverflow.com/questions/65144347/how-create-summary-table-for-every-column
"""
import os
import re
import sys
import tkinter as tk
import tkinter import ttk, messagebox

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

# The new sg3 implementations done so far. I adding multiple lines so
#it is obvious where it was placed.
#***********************************************************
#Here is where I put Elenas code. It seem that this code acts as the
#main and so I deleted the previous sg2 main function. -Hannah
MAIN_FONT = "Arial"
MAIN_STYLE = {
    'font': "Arial", 
}   

class OpenFileUI(tk.Frame):
    def __init__(self,parent,on_submit):
        tk.Frame.__init__(self,parent)
        """
        Initialize Widget
        """
        pass
    
class CloseFileUI(tk.Frame):
    program = 4
    def __init__(self,parent,files,on_submit):
        """
        Initialize Widget
        """
        tk.Frame.__init__(self,parent,files)
        self._files = files
        if len(self._files)>0:
            pass
        else:
            messagebox.showerror("Error", "You must have open files to use this option.")
        pass
    def getProgramId(self):
        """ Returns Id of Program"""
        return self.program
class WordSearchUI(tk.Frame):
    """ Ui for word search, """
    program = 2
    """  """
    def __init__(self,parent,files,on_submit,on_cancel,on_error):
        """
        Initialize Widget
        """
        tk.Frame.__init__(self,parent)
        if len(self._files)>0:
            self._search_panel = ttk.LabelFrame(parent,text="Word Search")
            self._search_panel.pack(anchor="to")
            self._input = tk.Text(self._search_panel,width="25")
            self._input.grid(row=0,column=0,columnspan=2,sticky="W")
            self._result_panel = ttk.LabelFrame(parent,text="Results")
            
            self._submit_btn = tk.Button(self._search_panel,text="Enter",command=on_submit)
            self._submit_btn.grid(row=0,column=2,sticky="E")
            self._cancel_btn = tk.Button(self._search_panel,text="Cancel",command=on_cancel)
            self._cancel_btn.grid(row=0,column=3)
        else:
            messagebox.showerror("Error", "You must have open files to use this option.")
            on_error(self.program)
        #end of file
    def getProgramId(self):
        return self.program

class SelectOpenFile(tk.Frame):
    """
        Gui that shows the user a list of opened files to choose from
    """
    def __init__(self,parent, open_files=[], on_submit=None):
        """
        Initialize Widget
        """
        tk.Frame.__init__(self,parent)
        self._open_files = []
        if len(self._open_files > 0):
            pass
        else:
            messagebox.showerror("")
        pass
class BuildConcordance(tk.Frame):
    """
        Gui Frame that 
    """
    def __init__(self,parent, open_files=[], on_submit=None):
        """
        Initialize Widget
        """
        tk.Frame.__init__(self,parent)
        self._open_files = []
        if len(self._open_files > 0):
            
            pass
        else:
            messagebox.showerror("")
        pass

"""
https://www.digitalocean.com/community/tutorials/tkinter-working-with-classes
"""
class MainMenu(tk.Frame):
    """ Main Menu for Program """
    _selected_option = None
    """
    
    """
    def __init__(self,parent,on_submit):
        """
        Initialize Widget
        on submit
        """
        tk.Frame.__init__(self,parent)
        
        self._selected_option = tk.IntVar()# selected option
        
        self._panel = ttk.LabelFrame(parent,text="Main Menu")
        self._panel.pack(side="left",anchor='nw',fill="y")
        # titleLbl = tk.Label(parent,text="Main Menu",font=(MAIN_FONT,20,"bold"))
        # titleLbl.grid(row=0, column=0)
        #options
        
        option1 = tk.Radiobutton(self._panel,text="1. Select a File",
                                value=1,
                                variable=self._selected_option,justify='left',takefocus=True)
        option1.grid(row=1,column=0,columnspan=2,sticky='W')
        option2 = tk.Radiobutton(self._panel,text="2. Find a word in all your open files",
                                value=2, variable=self._selected_option,justify='left',takefocus=False)
        option2.grid(row=2,column=0,columnspan=2,sticky='W')
        option3 = tk.Radiobutton(self._panel,text="3. Build a concordance for one open file",
                                value=3, variable=self._selected_option,justify='left',takefocus=False)
        option3.grid(row=3,column=0,columnspan=2,sticky='W')
        option4 =   tk.Radiobutton(self._panel,text="4. Close one of the files",
                                value=4, variable=self._selected_option,justify='left',takefocus=False)
        option4.grid(row=4,column=0,columnspan=2,sticky='W')
        option5 = tk.Radiobutton(self._panel,text="5. Quit Program",
                                value=5,variable=self._selected_option,justify='left',takefocus=False)
        option5.grid(row=5,column=0,sticky='W')
        self.submit = tk.Button(self._panel,text="Enter",command=on_submit)
        self.submit.grid(row=6,column=1)
    # def on_selected(self):
    def getSelectedOption(self):
        return self._selected_option.get()
    def clearOptions(self):
        self._selected_option.set(0)
    # def enable
    
class SG3:
    '''
    Runs the program
    Note: I Created Certain Components as separate classes for the sake of organization.
    
    '''
    TITLE = "SG3 Program"
    SIZE = "700x600"
    introduction = ("Usage: This program accepts a '.txt.' file that must reside within the same directory as this program.\n"
      "After the file is successfully uploaded. The words within the file will be parsed and counted.\n"
      "Afterwards you will be prompted to enter a word, this will check the occurrences of that word and display a count.\n"
      "You will then be prompted to continue entering words until you are complete.\n"
      "Once completed the list of words and their counts will be listed.")
   
    def __init__(self):
        self._files = []
        self._words_arrays = []
        self._open_files = []
        self._program = 0 #for 
        self.root = tk.Tk()
        self.root.geometry(self.SIZE)
        self.root.title = self.TITLE
        self._main_menu =  MainMenu(self.root,on_submit=self.menu_option_selected)
        self._main_menu.pack(fill="x",side='right',anchor='nw')
        self.sub_panel = ttk.LabelFrame(self.root,text="Program",width=450)
        self.sub_panel.pack(side='right',anchor="ne",fill="both")
        self.sub_window = None
        # self.OpenMainMenu()
        self.root.mainloop()
    
    def menu_option_selected(self):
        print("Menu Option Selected")
        self._program = self._main_menu.getSelectedOption()
        match self._program:
            case 1:
                self.open_files_ui()
            case 2:
                self.word_search_ui()
            case 3:
                self.concordance_window()
            case 4:
                self.close_file_ui()
            case 5:
                self.exit_program()
            case _:
                pass
    def on_error(self,program):
        if program != 0:
            self.sub_window.destroy()
            self._program = 0
            
    def open_files_ui(self): # for opening files
        
        self.sub_panel.config(text="Open File")
        
        # self.sub_window = OpenFileUI(self.sub_panel)
        print("To Be Implemented")
        pass
    def concordance_window(self):
        self.sub_panel.config(text="Build Concordance")
        print("To Be Implemented")
        pass
    def build_concordance(self):
        pass
    
    def close_file_ui(self):
        self.sub_panel.config(text="Close a File")
        print("To Be Implemented")

        pass
    def word_search_ui(self):
        self.sub_panel.config(text="Word Search")
        print("To Be Implemented")
        pass
    
    def onSubProgramEnded(self,sub):
        self.sub_panel.config(text="")
        self.sub_panel
        pass
    def exit_program(self):
        print("To Be Implemented")
        pass
    
    @staticmethod
    def show_help(x):
        ''' Displays a help box on screen '''
        # messagebox.showinfo(title="SG3",message=SG3.introduction)
    @staticmethod
    def show(title,msg):
        return messagebox.showinfo(title=title,message=msg)
    
    @staticmethod
    def ask_continue(title,msg):
        return messagebox.askyesno(title=title,message=msg)
    @staticmethod
    def error(title,msg):
        return messagebox.showerror(title,msg)
def main():
    messagebox.showinfo(title="SG3",message=SG3.introduction)
    main_program = SG3()
    sys.exit(0)
    
if __name__=="__main__":
    main()

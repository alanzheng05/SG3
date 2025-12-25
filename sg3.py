import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import re

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
#Addition to get user to input the text manually from the directory
        self._on_submit = on_submit
        label = tk.Label(self, text="Enter .TXT filename in this directory:",
                         font=(MAIN_FONT, 10))
        label.pack(anchor="w", padx=5, pady=5)

        self._entry = tk.Entry(self, width=40)
        self._entry.pack(anchor="w", padx=5, pady=5)

        submit_btn = tk.Button(
            self,
            text="Open File",
            command=self._handle_submit
        )
        submit_btn.pack(anchor="w", padx=5, pady=5)

        self._msg_label = tk.Label(self, text="", fg="blue",
                                   font=(MAIN_FONT, 9))
        self._msg_label.pack(anchor="w", padx=5, pady=5)

    def _handle_submit(self):
        filename = self._entry.get().strip()
        if self._on_submit:
            self._on_submit(self, filename)

    def show_message(self, text, is_error=False):
        self._msg_label.config(text=text, fg="red" if is_error else "blue")


#Edited this class so that the file will close one of the files as per request
#of the user.   
class CloseFileUI(tk.Frame):
    program = 4
    def __init__(self,parent,files,on_submit):
        """
        Initialize Widget
        """
        tk.Frame.__init__(self,parent)
        self._files = files
        self._on_submit = on_submit

        if len(self._files)>0:
            lbl = tk.Label(self, text="Select a file to close:",
                           font=(MAIN_FONT, 10))
            lbl.pack(anchor="w", padx=5, pady=5)

            self._listbox = tk.Listbox(self, height=min(10, len(files)))
            for fname in self._files:
                self._listbox.insert(tk.END, fname)
            self._listbox.pack(fill="x", padx=5, pady=5)

            close_btn = tk.Button(
                self,
                text="Close Selected File",
                command=self._handle_close
            )
            close_btn.pack(anchor="w", padx=5, pady=5)
        else:
            messagebox.showerror("Error, you must have open files to use this option.")

    def _handle_close(self):
        if not self._files:
            return
        sel = self._listbox.curselection()
        if not sel:
            messagebox.showerror("Error", "Please select a file to close.")
            return
        index = sel[0]
        filename = self._files[index]
        if self._on_submit:
            self._on_submit(filename)

    def getProgramId(self):
        """ Returns Id of Program"""
        return self.program

#Edited to add a textbox for the user to manually input the files
class WordSearchUI(tk.Frame):
    """ Ui for word search, """
    program = 2
    """  """
    def __init__(self,parent,files,on_submit,on_cancel,on_error):
        """
        Initialize Widget
        """
        tk.Frame.__init__(self,parent)
        self._files = files
        self._on_submit = on_submit
        self._on_cancel = on_cancel
        self._on_error = on_error

        if len(self._files) > 0:
            self._search_panel = ttk.LabelFrame(self, text="Word Search")
            self._search_panel.pack(anchor="nw", fill="x", padx=5, pady=5)

            tk.Label(self._search_panel, text="Enter a legal word "
                      "(letters and optional hyphens):").grid(
                row=0, column=0, columnspan=3, sticky="w", pady=2
            )

            self._input = tk.Text(self._search_panel, width=25, height=1)
            self._input.grid(row=1, column=0, columnspan=3, sticky="w")

            self._submit_btn = tk.Button(
                self._search_panel,
                text="Search",
                command=lambda: self._on_submit(self)
            )
            self._submit_btn.grid(row=2, column=0, sticky="w", pady=5)

            self._cancel_btn = tk.Button(
                self._search_panel,
                text="Cancel",
                command=self._on_cancel
            )
            self._cancel_btn.grid(row=2, column=1, sticky="w", pady=5)

            self._result_panel = ttk.LabelFrame(self, text="Results")
            self._result_panel.pack(anchor="nw", fill="both",
                                    expand=True, padx=5, pady=5)

            self._results = tk.Text(self._result_panel, width=60, height=15)
            self._results.pack(fill="both", expand=True, padx=5, pady=5)
        else:
            messagebox.showerror("Error, you must have open files to use this option.")
            if self._on_error:
                self._on_error(self.program)

    def get_word(self):
        word = self._input.get("1.0", tk.END).strip()
        return word

    def show_results(self, text):
        self._results.delete("1.0", tk.END)
        self._results.insert(tk.END, text + "\n")

    def getProgramId(self):
        return self.program


#Edited to let the user see a list of the files and fix the bug of the 
#open_files being passed into _init_ which would make the list empty
#And send the appropriate erros for the user
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
            open_files = []
        self._open_files = open_files
        self._on_submit = on_submit

        if len(self._open_files) > 0:
            lbl = tk.Label(self, text="Select an open file:",
                           font=(MAIN_FONT, 10))
            lbl.pack(anchor="w", padx=5, pady=5)

            self._listbox = tk.Listbox(self, height=min(10, len(open_files)))
            for fname in self._open_files:
                self._listbox.insert(tk.END, fname)
            self._listbox.pack(fill="x", padx=5, pady=5)

            submit_btn = tk.Button(
                self,
                text="OK",
                command=self._handle_submit
            )
            submit_btn.pack(anchor="w", padx=5, pady=5)
        else:
            messagebox.showerror("Error", "No open files available.")

    def _handle_submit(self):
        if not self._open_files or not self._on_submit:
            return
        sel = self._listbox.curselection()
        if not sel:
            messagebox.showerror("Error", "Please select a file.")
            return
        index = sel[0]
        self._on_submit(self._open_files[index])


#Edit this class so that is can align more with the previous sg2 that
#we are using as the base. I also makes it more convienient for the
#User to see all the files and to buid the option of build cordanance. 
class BuildConcordance(tk.Frame):
    """
        Gui Frame that 
    """
    def __init__(self,parent, open_files=[], on_submit=None):
        """
        Initialize Widget
        """
        tk.Frame.__init__(self,parent)
        if open_files is None:
            open_files = []
        self._open_files = open_files
        self._on_submit = on_submit
        self._selected_index = tk.IntVar(value=0)

        if len(self._open_files) > 0:
            lbl = tk.Label(self, text="Select a file to build a concordance:",
                           font=(MAIN_FONT, 10))
            lbl.pack(anchor="w", padx=5, pady=5)

            for i, fname in enumerate(self._open_files):
                rb = tk.Radiobutton(
                    self,
                    text=fname,
                    variable=self._selected_index,
                    value=i,
                    anchor="w",
                    justify="left"
                )
                rb.pack(anchor="w", padx=10)

            build_btn = tk.Button(
                self,
                text="Build Concordance",
                command=self._handle_submit
            )
            build_btn.pack(anchor="w", padx=5, pady=10)
        else:
            messagebox.showerror("Error, you must have open files to use this option.")

    def _handle_submit(self):
        if not self._open_files:
            return
        idx = self._selected_index.get()
        if idx < 0 or idx >= len(self._open_files):
            messagebox.showerror("Error", "Invalid file selection.")
            return
        if self._on_submit:
            self._on_submit(self._open_files[idx])
#Self note of where the end of what I edited 12/03/2025 - hannah

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
        # Edited to keep track of open files, their word lists, and word searches
        self._files = []
        self._words_arrays = []
        self._open_files = []
        self._word_search_array = []
        self._program = 0
        self.root = tk.Tk()
        self.root.geometry(self.SIZE)
        self.root.title(self.TITLE)

        self._main_menu =  MainMenu(self.root,on_submit=self.menu_option_selected)
        self._main_menu.pack(fill="x",side='right',anchor='nw')

        self.sub_panel = ttk.LabelFrame(self.root,text="Program",width=450)
        self.sub_panel.pack(side='right',anchor="ne",fill="both")
        self.sub_window = None

        self.root.mainloop()

    
    def menu_option_selected(self):
        print("Menu Option Selected")
        self._program = self._main_menu.getSelectedOption()
        #edited to add this to clear the previous subwindows
        if self.sub_window is not None:
            self.sub_window.destroy()
            self.sub_window = None

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
        #edited this to properly send error fot sub_window is none
        if program != 0 and self.sub_window is not None:
            self.sub_window.destroy()
        self._program = 0

#editing this because some of the functions were moved about and
#this function is used to implement GUI open file handler        
    def open_files_ui(self): # for opening files
        self.sub_panel.config(text="Open File")
        if len(self._files) >= max_input_files:
            messagebox.showerror(
                "Error",
                f"You already have the maximum of {max_input_files} files open."
            )
            return
        self.sub_window = OpenFileUI(self.sub_panel, on_submit=self._handle_open_file)
        self.sub_window.pack(fill="both", expand=True, padx=5, pady=5)
    #to handle the opened files selcted bu the user
    def _handle_open_file(self, ui: OpenFileUI, filename: str):
        if not filename:
            ui.show_message("ERROR: Please enter a filename.", is_error=True)
            return
        if not txt_filename(filename):
            ui.show_message("ERROR: Filename must end in .TXT.", is_error=True)
            return
        if not os.path.isfile(filename):
            ui.show_message("ERROR: File does not exist in this directory.", is_error=True)
            return
        if filename in self._files:
            ui.show_message("ERROR: File has already been opened.", is_error=True)
            return
        if len(self._files) >= max_input_files:
            ui.show_message(f"ERROR: Cannot open more than {max_input_files} files.", is_error=True)
            return

        # Actually open and parse
        try:
            with open(filename, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            ui.show_message(f"ERROR reading file: {e}", is_error=True)
            return

        words = extract_words(text)
        self._files.append(filename)
        self._words_arrays.append(words)
        self._open_files = self._files

        ui.show_message(f"File '{filename}' opened successfully. "
                        f"Total words: {len(words)}, distinct: {len(set(words))}.")

        print_file_table(self._files, self._words_arrays)

    #this function does the GUI word search
    def word_search_ui(self):
        self.sub_panel.config(text="Word Search")
        if len(self._files) == 0:
            messagebox.showerror("Error", "You must open at least one file first.")
            return
        self.sub_window = WordSearchUI(
            self.sub_panel,
            self._files,
            on_submit=self._do_word_search,
            on_cancel=self._cancel_subprogram,
            on_error=self.on_error
        )
        self.sub_window.pack(fill="both", expand=True, padx=5, pady=5)
    #helps the code do the word search based on user gui input
    def _do_word_search(self, ui: WordSearchUI):
        word = ui.get_word()
        if not word:
            ui.show_results("Error: Please enter a word to search.")
            return

        if not re.fullmatch(r"[A-Za-z]+(?:-[A-Za-z]+)*", word):
            invalid_char = first_invalid_ch(word)
            if invalid_char:
                ui.show_results(
                    f"Error: Invalid character '{invalid_char}' found. "
                    "Word must only contain letters A-Z and optional hyphens."
                )
            else:
                ui.show_results(
                    "Error: Word must only contain letters A-Z and optional hyphens."
                )
            return

        word_lc = word.lower()
        totals = count_word(self._files, self._words_arrays, word_lc)

        self._word_search_array.append((word_lc, totals))

        # Creating the GUI result text
        result_lines = [f"Search results for '{word_lc}':"]
        for filename, count in totals:
            result_lines.append(f"  {filename}: {count} occurrence(s)")
        ui.show_results("\n".join(result_lines))
        print("\n".join(result_lines))

    #create the concordance of the user selected files from the GUi
    def concordance_window(self):
        self.sub_panel.config(text="Build Concordance")
        if len(self._files) == 0:
            messagebox.showerror("Error", "You must open at least one file first.")
            return
        self.sub_window = BuildConcordance(
            self.sub_panel,
            open_files=self._files,
            on_submit=self._handle_build_concordance
        )
        self.sub_window.pack(fill="both", expand=True, padx=5, pady=5)
    #only the selected files only can be used to build the concordance
    def _handle_build_concordance(self, filename: str):
        if filename not in self._files:
            messagebox.showerror("Error", f"File '{filename}' is not currently open.")
            return

        concordance = build_concordance([filename])
        write_concordance(concordance)

        index = self._files.index(filename)
        wordlists = [self._words_arrays[index]]
        filenames = [filename]
        write_extra_lists(concordance, filenames, wordlists)

        messagebox.showinfo(
            "Concordance",
            "Concordance written to CONCORDANCE.TXT\n"
            "Extra lists written to ExtraLists.txt\n"
            f"(Built using file: {filename})"
        )

        print("\nConcordance and Extra Lists built for:", filename)

    #close the file in the gui option 4
    def close_file_ui(self):
        self.sub_panel.config(text="Close a File")
        if len(self._files) == 0:
            messagebox.showerror("Error", "You must have open files to use this option.")
            return
        self.sub_window = CloseFileUI(
            self.sub_panel,
            files=self._files.copy(),
            on_submit=self._handle_close_file
        )
        self.sub_window.pack(fill="both", expand=True, padx=5, pady=5)

    #function to close the file and to remove it from the memory and list
    def _handle_close_file(self, filename: str):
        if filename not in self._files:
            messagebox.showerror("Error", f"File '{filename}' is not currently open.")
            return
        idx = self._files.index(filename)
        self._files.pop(idx)
        self._words_arrays.pop(idx)
        self._open_files = self._files

        messagebox.showinfo("Close File", f"Closed file '{filename}'.")
        print(f"Closed file '{filename}'.")

        if self._files:
            print_file_table(self._files, self._words_arrays)
        else:
            print("No files currently open.")

        if self.sub_window is not None:
            self.sub_window.destroy()
            self.sub_window = None

    #option 5 of exiting the program with sumary statement
    def exit_program(self):
        if self._word_search_array and self._files:
            queried_words_lc = get_queried_words_from(self._word_search_array)
            print_summary_words(queried_words_lc, self._files, self._words_arrays)

        print(outro)
        messagebox.showinfo("Exit", "Program has finished executing.")
        self.root.destroy()
        sys.exit(0)
    
    #to end the program 
    def _cancel_subprogram(self):
        if self.sub_window is not None:
            self.sub_window.destroy()
            self.sub_window = None
        self.sub_panel.config(text="Program")

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

# SWE Project
A Python GUI application that processes up to 10 text files with a graphical interface. Users can open files, search for words across all files, build concordances for individual files, and close files through an interactive menu system built with Tkinter.

## Members
- Alan Zheng
- Jamie Harris
- Elena Miller
- Hannah Smid
- Xavian Kimbrough

## Note
- File names: Must end with .txt (case-insensitive)
- Maximum 10 files can be opened (no duplicates allowed)
- Enter .txt files from the current directory
- Search words: Only letters (a-z, A-Z) & hyphens allowed
- Main menu options: (1) Open file, (2) Search word in all files, (3) Build concordance for one file, (4) Close a file, (5) Quit program
- Options 2-4 require at least one file to be open
- Concordance output: Alphabetically sorted with X.Y.Z location format (file.line.word)
- Generates output files: CONCORDANCE.TXT and ExtraLists.txt
- Program displays error messages through GUI dialog boxes
- All previous SG2 functionality maintained with GUI interface

# Smart File Organizer

This is my Task 08 project for the White Band Associates Python Internship. In this task I built a Smart File Organizer that automatically sorts files into folders based on their type. It also has search, duplicate detection, report generation and a few bonus features.

---

## Objective

The idea behind this project was to build a real-world automation tool using Python. I used concepts like file handling, directory management, OOP, exception handling and the os and shutil modules to build this application.

---

## Features

- Select any folder on your computer
- Scan all files and display their names and extensions
- Automatically organize files into folders like Images, Documents, Videos, Audio, Archives, Programs and Others
- View file statistics category-wise
- Search files by name or extension
- Detect duplicate file names
- Generate a detailed report as file_report.txt
- Export file data to CSV
- Find the largest files in the folder
- View recently modified files
- Delete empty folders

---

## Modules

| Module | Description |
|--------|-------------|
| Module 1 | Directory Selection with path validation |
| Module 2 | File Scanning with name and extension display |
| Module 3 | Automatic File Organization into category folders |
| Module 4 | File Statistics in a formatted table |
| Module 5 | Search by file name or extension |
| Module 6 | Duplicate File Detection |
| Module 7 | Generate TXT Report |
| Bonus | CSV Export, Largest File Finder, Recently Modified, Delete Empty Folders |

---

## Technologies Used

- Python 3
- os module
- shutil module
- csv module
- datetime module

No third party libraries needed. Everything runs with Python's built in modules.

---

## How to Run

1. Make sure Python 3 is installed on your system
2. Create a test folder and put some files in it (jpg, pdf, mp3, zip etc.)
3. Open Command Prompt and go to the folder where the script is saved
4. Run this command:

```
python smart_file_organizer.py
```

5. From the menu, press 1 first to select your folder path
6. Then use the other options to scan, organize, search and generate reports

---

## Project Structure

```
Python_Task_08_YourName/
│
├── smart_file_organizer.py
├── file_report.txt
├── file_report.csv
├── README.md
├── Screenshots/
└── TestFolder/
    ├── Images/
    ├── Documents/
    ├── Videos/
    ├── Audio/
    ├── Archives/
    └── Others/
```

---

## Sample Output

```
=============================================
        SMART FILE ORGANIZER
=============================================
  1. Select Directory
  2. Scan Files
  3. Organize Files
  4. File Statistics
  5. Search Files
  6. Detect Duplicate Files
  7. Generate Report (TXT)
  -- Bonus ----------------------------
  8. Export Report to CSV
  9. Find Largest Files
  10. Recently Modified Files
  11. Delete Empty Folders
  0. Exit
=============================================

Enter Folder Path: C:\Users\YourName\TestFolder
✔  Folder found: C:\Users\YourName\TestFolder

Found 12 File(s)

  Organizing: [####################] 100%
✔  Files organized successfully!
```

---

## Challenges Faced

The first issue I ran into was the encoding error when generating the report on Windows. Special characters like └── were causing a charmap error. I fixed it by adding encoding="utf-8" when opening the file and replacing those characters with plain ASCII.

Another challenge was making sure the program does not crash when a folder has no files or when there are permission issues. I handled all of this using try and except blocks.

---

## Future Improvements

- Add a graphical user interface using Tkinter
- Add undo functionality to move files back to original location
- Schedule automatic organization using a timer
- Add file preview feature
- Support for organizing files by date modified

---

## What I Learned

This project helped me understand how Python can be used for real automation tasks. I learned how to work with the os and shutil modules, handle file paths on Windows, manage exceptions properly and build a clean menu driven application. This kind of tool is actually useful in daily life which made it more fun to build.

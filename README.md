# Personal Phonebook and Notes Application - Chat Bot

This is a simple phonebook application that allows you to manage your contacts, notes, and search for information.

## About

This application is designed to help you keep track of your contacts and their information, including phone numbers, email addresses, addresses, and birthdays and search for information by name, phone number, email address, address, birthday. It also allows you to add notes, edit notes and search in the notes.

## How to Use

The application is available for Windows and Mac/Linux.
Download the source code from the project's GitHub repository. Extract the source code and open a terminal window in the extracted directory. Run the following command to install the dependencies:

### Windows
`pip install -r requirements.txt`

### Mac/Linux
`pip3 install -r requirements.txt`

Then, run the following command to start the application:

### Windows
`python main.py`

### Mac/Linux
`python3 main.py`

### Test data
If you want to create some test data in the phone book, you can uncomment the line `#print(add_test_data(phone_book_bd))` in the `main.py` file before running it. This will add some sample users with phone numbers and birthdays to the phone book. You can comment it again if you want to start with an empty phone book.

# Commands List

## CONTACTS Commands List

### Contact Add Commands
- `add <name> <phone> [birthday]` - Add a new user to the phone book with a phone number and an optional birthday.
- `add phone <name> <phone>` - Add a phone number to a user.
- `add address <name> <address>` - Add an address to a user.
- `add birthday <name> <birthday>` - Add a birthday to a user.
- `add email <user name> <email>` - Add an email to a user.

### Contact Remove Commands
- `remove <user name>` - Remove a user from the phone book.
- `remove phone <name> <phone>` - Remove a phone number from a user.
- `remove address <user name>` - Remove an address from a user.
- `remove birthday <user name>` - Remove a birthday from a user.
- `remove email <name> <email>` - Remove an email from a user.

### Contact Change (Edit) Commands
- `change <name> <old phone> <new phone>` - Change the old phone number to the new phone number for a user.
- `change phone <name> <old phone> <new phone>` - Change the old phone number to the new phone number for a user.
- `change address <name> <address>` - Change the address for a user.
- `change birthday <name> <birthday>` - Change the birthday for a user.
- `change email <name> <old email> <new email>` - Change the old email to the new email for a user.

### Contact Find and Show Commands
- `find <user name>` - Show all information about the user.
- `search contacts <text_1> <text_n>` - Display all the users whose name, phone number, email, address, or birthday match the search text(s).
- `show all` - Show all users in the phone book.
- `show <number>` - Show users in the phone book split into pages by the number of records per page.

## NOTES Command List

- `add note` - Add a new note with optional tags, separated by a comma.
- `remove note` - Remove a note.
- `change note` - Change the text and/or tags of the note (existing note will be replaced by the new note).
- `show notes` - Show all notes.
- `add tag` - Add a tag to a note.
- `remove tag` - Remove a tag from a note.
- `edit tag` - Edit the tag of a note.
- `search notes <text_1> <text_n>` - Display all notes whose title, text, or tag match the search text(s).

## General Commands

- `help` - Show the full commands list.
- `help contacts` - Show the commands list for contacts.
- `help notes` - Show the commands list for notes.
- `exit` - Exit the program.


## Data storage

The chat bot uses `phone_book.bin` and `notes_book.bin` to save the contacts and notes. It reads and loads the data from these files when it starts. It also writes the data to these files after exit. It uses binary files because they are faster and more efficient than text files.
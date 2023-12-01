from abc import ABC, abstractmethod
from colorama import Fore, Style
from classes import AddressBook, Name, Phone, Record, Email, Birthday
from classes import Note, NoteTitle, NoteBook, NoteText, Tag


file_name = "phone_book.bin"

notes_file_name = "notes_book.bin"

phone_book_bd = AddressBook(file_name)

note_book_bd = NoteBook(notes_file_name)


class ErrorHandler(ABC):
    @abstractmethod
    def handle_error(func):
        def inner(*args):
            try:
                return func(*args)
            except IndexError:
                return "Not enough params for this command. Try help command for more information."
            except KeyError:
                return "User not exist in the phone book."
            except ValueError as ve:
                return ve
            except TypeError as te:
                return te

        return inner


class Command(ABC):
    def __init__(self, phone_book: AddressBook):
        self.phone_book = phone_book

    @abstractmethod
    def execute(self, *args) -> str:
        pass


class HelpCommand(ABC):
    def __init__():
        pass

    @abstractmethod
    def execute() -> str:
        pass


class AddUserCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    # def add_user(*args) -> str:
    def execute(self, *args) -> str:
        name = Name(args[0])
        phone = Phone(sanitize_phone_number(args[1]))
        bithday = args[2] if len(args) > 2 else None
        rec = phone_book_bd.get(name.value)
        if rec:
            phone_book_bd.get(name.value).add_phone(phone.value)
            return f"Phone {phone} was added to the contact {name}"
        else:
            if not bithday:
                phone_book_bd.add_record(Record(name.value, phone.value))
                return f"User {name} with phone {phone} was added to the phone book"
            else:
                phone_book_bd.add_record(
                    Record(name.value, phone.value, bithday))
                return f"User {name} with phone {phone} and birthday {bithday} was added to the phone book"


class AddAddressCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(cls, *args) -> str:
        # def add_address(*args) -> str:
        addr_str = ""
        addr_str = " ".join(args[1:])
        name = Name(args[0])
        rec = phone_book_bd.get(name.value)
        if rec:
            phone_book_bd.get(name.value).add_address(addr_str)
            return f"Address was added sucessfully to the {name.value}"
        return f"User {name} not found in the phone book"


class AddBirthdayCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def add_birthday(*args) -> str:
        name = Name(args[0])
        birthday = Birthday(args[1])
        rec = phone_book_bd.get(name.value)
        return rec.add_birthday(args[1]) if rec else f"User {name} not found in the phone book"


class AddEmailCommand(Command):
    @classmethod
    # @staticmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def add_email(*args) -> str:
        name = Name(args[0])
        email = Email(args[1])
        rec = phone_book_bd.get(name.value, None)
        return rec.add_email(email) if rec else f"User {name} not found in the phone book"


class ChangeUserPhoneCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def change_user_phone(*args) -> str:
        name = Name(args[0])
        old_phone = Phone(sanitize_phone_number(args[1]))
        new_phone = Phone(sanitize_phone_number(args[2]))
        rec = phone_book_bd.find(name.value)
        if rec:
            if rec.find_phone(old_phone.value) and old_phone.value != new_phone.value:
                rec.edit_phone(old_phone.value, new_phone.value)
                return f"User {name} phone {old_phone.value} was changed to {new_phone.value}"
            else:
                return f"User {name} has no phone {old_phone.value} or old and new phones are the same"


class ChangeUserEmailCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def change_user_email(*args) -> str:
        name = Name(args[0])
        old_email = Email(args[1])
        new_email = Email(args[2])
        rec = phone_book_bd.find(name.value)
        if rec:
            if rec.find_email(old_email.value) and old_email.value != new_email.value:
                rec.edit_email(old_email.value, new_email.value)
                return f"User {name} email {old_email.value} was changed to {new_email.value}"
            else:
                return f"User {name} has no email {old_email.value} or old and new emails are the same"


class ShowUserCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(cls, *args) -> str:
        # def show_user_by_phone(*args) -> str:
        name = Name(args[0])
        rec = phone_book_bd.find(name.value)
        if rec:
            return f"{rec}"
        else:
            return f"User {name.value} not exist in the phone book"


class RemoveUserCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def remove_user(*args) -> str:
        name = Name(args[0])
        rec = phone_book_bd.find(name.value)
        if rec:
            phone_book_bd.delete(name.value)
            return f"User {name.value} was removed from the phone book"
        else:
            return f"User {name.value} not exist in the phone book"


class ShowAllUsersCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(cls, *args) -> str:
        # def execute() -> str:
        # def show_all_users(*_) -> str:
        if not bool(phone_book_bd):
            result_str = "No contacts list in the phone book"
        else:
            result_str = "Contacts list in the phone book:\n" + \
                "\n".join([f"{v}" for _, v in phone_book_bd.items()])
        return result_str


class ShowMatchUsersCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def show_match_users(*args) -> str:
        if len(args) == 0:
            return "No search parameters. Try help command for more information."
        result_str = ""
        if not bool(phone_book_bd):
            result_str = "No contacts list in the phone book"
        else:

            for arg in args:
                for record in phone_book_bd.values():

                    if record.name.value.find(arg) != -1:

                        result_str += f"[   {Fore.BLUE}Name match{Style.RESET_ALL}] {Fore.YELLOW}{arg}{Style.RESET_ALL}: {record}\n"

                    for p in record.phones:
                        if p.value.find(arg) != -1:
                            result_str += f"[  {Fore.BLUE}Phone match{Style.RESET_ALL}] {Fore.YELLOW}{arg}{Style.RESET_ALL}: {record}\n"

                    for e in record.emails:
                        if e.value.find(arg) != -1:
                            result_str += f"[  {Fore.BLUE}Email match{Style.RESET_ALL}] {Fore.YELLOW}{arg}{Style.RESET_ALL}: {record}\n"

                    if record.address:
                        if record.address.value.find(arg) != -1:
                            result_str += f"[{Fore.BLUE}Address match{Style.RESET_ALL}] {Fore.YELLOW}{arg}{Style.RESET_ALL}: {record}\n"

                    if record.birthday:
                        date_str = record.birthday.value.strftime('%d.%m.%Y')
                        if date_str.find(arg) != -1:
                            result_str += f"[   {Fore.BLUE}Bday match{Style.RESET_ALL}] {Fore.YELLOW}{arg}{Style.RESET_ALL}: {record}\n"

            result_str = "The contacts in the phone book that match the search results are:\n" + \
                result_str if result_str else "No contacts in the phone book match the search results"
        return result_str


class ShowAllUsersOnPage(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def show_all_users_on_pages(*args):
        n = args[0] if args else 2

        if not args[0].isdigit():
            raise ValueError(
                "Invalid number of records per page. Try again or help command for more information.")

        if int(n) <= 0:
            raise ValueError(
                "Invalid number of records per page. Try again or help command for more information.")

        print(f"Printing {n} contacts per page:")
        rec_per_page = int(n)
        page_number = 1
        for page in phone_book_bd.iterator(rec_per_page):

            print(f"Page {page_number}", "-"*45)
            for v in page:
                print(v)
            input("Press any key to continue >>> ")

            page_number += 1

        return f"Printing finished, total pages was printed {page_number - 1}\n"


class RemovePhoneCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def remove_phone(*args) -> str:
        name = Name(args[0])
        phone = Phone(sanitize_phone_number(args[1]))
        rec = phone_book_bd.find(name.value)
        if rec:
            if rec.find_phone(phone.value):
                rec.remove_phone(phone.value)
                return f"Phone {phone.value} was removed from the contact {name.value}"
        return f"User {name.value} not exist or does not have phone {phone.value}"


class RemoveEmailCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def remove_email(*args) -> str:
        name = Name(args[0])
        email = Email(args[1])
        rec = phone_book_bd.find(name.value)
        if rec:
            if rec.find_email(email.value):
                rec.remove_email(email.value)
                return f"Email was removed from the contact {name.value}"
        return f"User {name.value} not exist or does not have email {email.value}"


class RemoveAddressCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def remove_address(*args) -> str:
        name = Name(args[0])
        rec = phone_book_bd.find(name.value)
        if rec:
            rec.remove_address()
            return f"Address was removed from the contact {name.value}"
        return f"User {name.value} not exist or does not have address"


class RemoveBirthdayCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def remove_birthday(*args) -> str:
        name = Name(args[0])
        rec = phone_book_bd.find(name.value)
        if rec:
            rec.remove_birthday()
            return f"Birthday was removed from the contact {name.value}"
        return f"User {name.value} not exist or does not have birthday"


class AddNoteCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self) -> str:
        # def add_note() -> str:
        title = input("Note Title >>> ")
        if not title:
            raise ValueError("Note title cannot be empty")
        title = NoteTitle(title)
        text = input("Note Text >>> ")
        text = NoteText(text)
        tags = input("Add Note Tags, separated by comma >>> ")
        tags = [(tag.strip()) for tag in tags.split(",")] if tags else None

        rec = note_book_bd.get(title.value)
        if not rec:
            note_book_bd.add_record(Note(title.value, text.value, tags))
            return f"Note {title.value} was added"
        else:
            return f"Note {title.value} exist"


class RemoveNoteCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def remove_note(*args) -> str:
        title = input("Note Title >>> ")
        if not title:
            raise ValueError("Note title cannot be empty")
        title = NoteTitle(title)
        rec = note_book_bd.get(title.value)
        return note_book_bd.delete(title.value) if rec else f"Note {title.value} not exist"


class ChangeNoteCommand(Command):
    # TEST
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def change_note(*args) -> str:
        title = input("Note Title >>> ")
        if not title:
            raise ValueError("Note title cannot be empty")
        title = NoteTitle(title)
        rec = note_book_bd.get(title.value)
        if not rec:
            return f"Note {title.value} not exist"

        text = input("Note Text >>> ")
        if not text:
            raise ValueError("Note text cannot be empty")
        text = NoteText(text)
        tags = input("Add Note Tags, separated by comma >>> ")
        tags = [(tag.strip()) for tag in tags.split(",")] if tags else None
        return note_book_bd.edit_record(Note(title.value, text.value, tags))


class AddTagCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def add_tag(*args) -> str:
        title = input("Note Title >>> ")
        if not title:
            raise ValueError("Note title cannot be empty")
        title = NoteTitle(title)
        rec = note_book_bd.get(title.value)
        if not rec:
            return f"Note {title.value} not exist"

        tag = input("Tag >>> ")
        if not tag:
            raise ValueError("Note tag cannot be empty")
        tag = Tag(tag)
        return rec.add_tag(tag.value)


class RemoveTagCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def remove_tag(*args) -> str:
        title = input("Note Title >>> ")
        if not title:
            raise ValueError("Note title cannot be empty")
        title = NoteTitle(title)
        rec = note_book_bd.get(title.value)
        if not rec:
            return f"Note {title.value} not exist"

        tag = input("Tag >>> ")
        if not tag:
            raise ValueError("Note tag cannot be empty")
        tag = Tag(tag)
        return rec.remove_tag(tag.value)


class ChangeTagCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def change_tag(*args) -> str:
        title = input("Note Title >>> ")
        if not title:
            raise ValueError("Note title cannot be empty")
        title = NoteTitle(title)
        rec = note_book_bd.get(title.value)
        if not rec:
            return f"Note {title.value} not exist"

        tag = input("Tag >>> ")
        if not tag:
            raise ValueError("Note tag cannot be empty")
        tag = Tag(tag)
        new_tag = input("New Tag >>> ")
        if not new_tag:
            raise ValueError("Note tag cannot be empty")
        new_tag = Tag(new_tag)
        return rec.edit_tag(tag.value, new_tag.value)


class SearchNotesCommand(Command):
    @classmethod
    @ErrorHandler.handle_error
    def execute(self, *args) -> str:
        # def search_notes(*args) -> str:
        if len(args) == 0:
            return "No search parameters. Try help command for more information."
        result_str = ""
        if not bool(note_book_bd):
            result_str = "No notes list in the note book"
        else:
            result_str = ""
            for arg in args:
                for record in note_book_bd.values():
                    if record.title.value.find(arg) != -1:
                        result_str += f"[{Fore.BLUE}Title match{Style.RESET_ALL}] {Fore.YELLOW}{arg}{Style.RESET_ALL}: {record}\n"
                    if record.text.value.find(arg) != -1:
                        result_str += f"[ {Fore.BLUE}Text match{Style.RESET_ALL}] {Fore.YELLOW}{arg}{Style.RESET_ALL}: {record}\n"
                    for tag in record.tags:
                        if tag.value.find(arg) != -1:
                            result_str += f"[  {Fore.BLUE}Tag match{Style.RESET_ALL}] {Fore.YELLOW}{arg}{Style.RESET_ALL}: {record}\n"
        return "The notes in the note book that match the search results are:\n" + result_str if result_str else "No notes in the note book match the search results\n"


class ShowAllNotesCommand(Command):
    @ErrorHandler.handle_error
    # def execute(self, *args) -> str:
    def execute() -> str:
        # def show_all_notes(*args) -> str:
        if not bool(note_book_bd):
            result_str = "No notes list in the note book"
        else:
            result_str = "Notes list in the note book:\n" + \
                "\n".join([f"{v}" for _, v in note_book_bd.items()])
        return result_str


class NoCommand(Command):
    @classmethod
    def execute(cls, *_) -> str:
        # def execute() -> str:
        # def no_command(*_) -> str:
        return "Enter the command or help for the list of commands"


class ShowHelpCotactsCommand(HelpCommand):
    def execute() -> str:
        # def help_contacts(*_) -> str:
        message = """
==== CONTACTS Commands List ====

==== Contact Add commands ====
add <name> <phone> [birthday]  - Add a new user to the phone book with a phone number and an optional birthday.
add phone <name> <phone>       - Add a phone number to a user.
add address <name> <address>   - Add an address to a user.
add birthday <name> <birthday> - Add a birthday to a user.
add email <user name> <email>  - Add an email to a user.

==== Contact Remove commands ====
remove <user name>          - Remove a user from the phone book.
remove phone <name> <phone> - Remove a phone number from a user.
remove address <user name>  - Remove an address from a user.
remove birthday <user name> - Remove a birthday from a user.
remove email <name> <email> - Remove an email from a user.

==== Contact Change (edit) commands ====
change <name> <old phone> <new phone>       - Change the old phone number to the new phone number for a user.
change phone <name> <old phone> <new phone> - Change the old phone number to the new phone number for a user.
change address <name> <address>             - Change the address for a user.
change birthday <name> <birthday>           - Change the birthday for a user.
change email <name> <old email> <new email> - Change the old email to the new email for a user.

==== Contact Find and show commands ====
find <user name>       - Show all information about the user.
search contacts <text_1 > <text_n> - Display all the users whose name, phone number, email, address or birthday match the search text(s).
show all               - Show all users in the phone book.
show <number>          - Show users in the phone book split into pages by the number of records per page.
"""
        return message


class ShowHelpNotesCommand(HelpCommand):
    def execute() -> str:
        # def help_notes(*_) -> str:
        message = """
====================== NOTES Command list ======================
add note    - Add a new note with optional tags, seperated by comma
remove note - Remove a note.
change note - Change the text and/or tags of the note (exiting note will be replaced by new note).
show notes  - Show all notes.
add tag     - Add tag to note.
remove tag  - Remove tag from note.
edit tag    - Edit tag of note.
search notes <text_1> <text_n> - Display all notes whose title, text or tag match the search text(s).
    """
        return message


class ShowHelpCommand(HelpCommand):
    def execute() -> str:
        # def help(*_) -> str:
        message = """
help          - Show the full commands list.
help contacts - Show the commands list for the contacts.
help notes    - Show the commands list for the notes.
exit          - Exit the program.
"""
        return message


class HelloUserCommand(HelpCommand):
    @ErrorHandler.handle_error
    def execute() -> str:
        # def hello(*_) -> str:
        return "Hello, I am a Contact book bot. Please enter any command or type help\n"


class Parser:
    # @staticmethod
    # def parse_command(text: str) -> tuple[Command, list[str]]:
    #     for kwd, command in COMMANDS.items():
    #         if text.lower().startswith(kwd):
    #             args = text[len(kwd):].strip().split()
    #             return command, args
    #     #return no_command, []
    #     return NoCommand(), []
    def parse(text: str):
        # def parser(text: str):
        for kwd, command in COMMANDS.items():
            if text.lower().startswith(kwd):
                args = text[len(kwd):].strip().split()
                return command, args
        # return no_command, []
        return NoCommand, []


def sanitize_phone_number(phone: str) -> str:
    new_phone = (
        phone.strip()
        .removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )
    return new_phone


def add_test_data(phone_book: AddressBook):
    phone_book.add_record(Record("user1", "1111111111", "12.12.1990"))
    phone_book.add_record(Record("user2", "2222222222", "13.12.1990"))
    phone_book.add_record(Record("user3", "3333333333", "14.12.1990"))
    phone_book.add_record(Record("user4", "4444444444", "15.12.1990"))
    phone_book.add_record(Record("user5", "5555555555", "01.01.2000"))
    phone_book.add_record(Record("user6", "6666666666", "20.10.1940"))
    phone_book_bd.add_record(Record("Jane", "1112223333"))
    phone_book_bd.add_record(Record("Jack"))

    # note_book_bd.add_record(Note("Note Title there ", "Text of the note there"))
    # note_book_bd.add_record(Note("Note1", "Text1", "One, two, t h r e"))
    return f"Test data added"


COMMANDS = {"?": help,
            "help contacts": ShowHelpCotactsCommand,  # help_contacts,
            "help notes": ShowHelpNotesCommand,  # help_notes,
            "help": ShowHelpCommand,  # help,
            "add phone": AddUserCommand,  # add_user,
            "add address": AddAddressCommand,  # add_address,
            "add birthday": AddBirthdayCommand,  # add_birthday,
            "add email": AddEmailCommand,  # add_email,
            "add note": AddNoteCommand,  # add_note,
            "add tag": AddTagCommand,  # add_tag,
            "add": AddUserCommand,  # add_user,
            "remove phone": RemovePhoneCommand,  # remove_phone,
            "remove address": RemoveAddressCommand,  # remove_address,
            "remove birthday": RemoveBirthdayCommand,  # remove_birthday,
            "remove email": RemoveEmailCommand,  # remove_email,
            "remove note": RemoveNoteCommand,  # remove_note,
            "remove tag": RemoveTagCommand,  # remove_tag,
            "remove": RemoveUserCommand,  # remove_user,
            "change phone": ChangeUserPhoneCommand,  # change_user_phone,
            "change address": AddAddressCommand,  # add_address,
            "change birthday": AddBirthdayCommand,  # add_birthday,
            "change email": ChangeUserEmailCommand,  # change_user_email,
            "change note": ChangeNoteCommand,  # change_note,
            "change tag": ChangeTagCommand,  # change_tag,"
            "find": ShowUserCommand,  # show_user_by_phone,
            "search contacts": ShowMatchUsersCommand,  # show_match_users,
            "search notes": SearchNotesCommand,  # search_notes,
            "show all": ShowAllUsersCommand,  # show_all_users,
            "show notes": ShowAllNotesCommand,  # show_all_notes,
            "show": ShowAllUsersOnPage  # show_all_users_on_pages
            }

EXIT_COMMANDS = ["exit", "close", "quit", "good bye"]


def main():

    print(phone_book_bd.load_data(file_name))
    print(note_book_bd.load_data(notes_file_name))

    # Uncomment to add test data to the phone book
    # print(add_test_data(phone_book_bd))

    # print(hello())
    print(HelloUserCommand.execute())

    while True:
        user_input = input("Enter command >>>")

        if user_input.lower() in EXIT_COMMANDS:
            print(phone_book_bd.save_data(file_name))
            print(note_book_bd.save_data(notes_file_name))
            print("Good bye!")
            break
        else:
            # command, args = parser(user_input)
            # print(command(*args))
            command, args = Parser.parse(user_input)
            print(command.execute(*args))


if __name__ == '__main__':
    main()

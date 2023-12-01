
from datetime import datetime
from collections import UserDict
from abc import ABC, abstractmethod
from colorama import Fore, Style
import pickle
import os
import re


class Field(ABC):
    def __init__(self, value):
        self.value = value

    @abstractmethod
    def __str__(self):
        pass


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return self.value


class NoteTitle(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return self.value


class NoteText(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = value

    def __str__(self):
        return self.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) > 0:
            self.__value = value
        else:
            raise ValueError(
                f"Note text '{value}' is incorrect, it should be at least 1 symbol")


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = value

    def __str__(self):
        return self.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) == 10 and value.isdigit():
            self.__value = value
        else:
            raise ValueError(
                f"Phone number {value} is incorrect, it should be 10 numbers")


class Email(Field):
    def __init__(self, value):
        super().__init__(value)

    def __eq__(self, __value: object) -> bool:
        return self.value == __value.value

    def find_all_emails(text):
        result = re.findall(r"[A-z.]+\w+@[A-z]+\.[A-z]{2,}", text)
        return result

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, email: str):
        new_email = str(email).strip()
        if re.findall(r"[A-z.]+\w+@[A-z]+\.[A-z]{2,}", new_email):
            self.__value = new_email
        else:
            raise ValueError(
                f"{new_email} - invalid email, the email must contains only letters, digits, @ and .")

    def __str__(self) -> str:
        return f"{self.value}" if self.value else ""


class Tag(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return super().__str__()

    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        bday = None
        if value:
            bday = datetime.strptime(value, '%d.%m.%Y').date()
        if bday:
            self.__value = bday
        else:
            raise ValueError(
                f"Birthday {value} is incorrect, it should be DD.MM.YYYY")

    def __str__(self):
        return f"#{self.value}" if self.value else ""


class Address(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value:
            self.__value = value
        else:
            raise ValueError(
                f"Address {value} is incorrect, it should be at least 1 symbol")

    def __str__(self) -> str:
        return f"{self.value}" if self.value else ""


class Note:
    def __init__(self, title_str: str, text_str: str, tag_list: list[Tag] = None):
        self.title = NoteTitle(title_str)
        self.text = NoteText(text_str)
        self.tags: list[Tag] = []
        if tag_list:
            for tag in tag_list:
                self.tags.append(Tag(tag))

        self.date = datetime.now()
        # self.path = f"{self.date.strftime('%d.%m.%Y')}_{self.title.value}.txt"

    def find_tag(self, tag_str: str) -> str | None:
        tag = None
        for t in self.tags:
            if t.value == tag_str:
                tag = t
                break
        return tag

    def add_tag(self, tag_str: str) -> str:
        new_tag = Tag(tag_str)
        is_tag = self.find_tag(tag_str)
        if not is_tag:
            self.tags.append(new_tag)
            return f"{new_tag.value} was added sucessfully to {self.title.value}"
        return f"{new_tag.value} already exist in {self.title.value}"

    def remove_tag(self, tag_str: str) -> str:
        tag = self.find_tag(tag_str)
        if tag:
            self.tags.remove(tag)
            return f"{tag_str} was removed sucessfully from the note '{self.title.value}'"
        return f"{tag_str} was not found in the note '{self.title.value}'"

    def edit_tag(self, tag: str, new_tag: str) -> str:
        # tag = Tag(tag)
        # new_tag = Tag(new_tag)
        is_tag = self.find_tag(tag)
        if tag == new_tag:
            return f"New and old tags are the same {tag} = {new_tag} in {self.title.value}"
        if is_tag:
            # self.tags[self.tags.index(is_tag)] = new_tag
            self.tags.remove(is_tag)
            self.tags.append(Tag(new_tag))
            return f"{tag} was changed to {new_tag} sucessfully for the note '{self.title.value}'"
        else:
            raise ValueError(
                f"{tag} was not found in the note '{self.title.value}'")

    def __str__(self) -> str:
        title_str = f"{Fore.BLUE}Title: {Style.RESET_ALL}{self.title.value:{20}}"
        text_str = f"{Fore.BLUE}Text: {Style.RESET_ALL}{self.text.value}"
        # tags_str = f'tags: {"#".join(t.value for t in self.tags)}' if self.tags else ""
        # formatted_tags = ' '.join(f'#{tag}' for tag in tags)
        formatted_tags = ' '.join(
            f'#{t.value}' for t in self.tags) if self.tags else ""
        tags_str = f"{Fore.GREEN}Tags: {Style.RESET_ALL}{formatted_tags}" if self.tags else ""
        date_str = f"{Fore.YELLOW}Date: {Style.RESET_ALL}{self.date.strftime('%d.%m.%Y %H:%M:%S')}"

        return f"{title_str} {text_str} {tags_str} {date_str}"


# def __str__(self):
#         name_str = f"Contact: {self.name.value}"
#         phones_str = ' '.join(p.value for p in self.phones)
#         emails_str = " ".join(e.value for e in self.emails)
#         address_str = self.address.value if self.address else ""
#         date_str = f"{datetime.strftime(self.birthday.value, '%d.%m.%Y')}, {self.days_to_birthday(self.birthday.value)}" if self.birthday else ""
#         return f"{name_str} {phones_str} {emails_str} {address_str} {date_str}"

class Record:
    def __init__(self, name: str, phone_str: str = None, birthday_str: str = None, email_str: Email = None, address_str: Address = None):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.emails: list[Email] = []
        if phone_str:
            self.phones.append(Phone(phone_str))
        if email_str:
            self.emails.append(Email(email_str))
        self.address = Address(address_str) if address_str else None
        self.birthday = Birthday(birthday_str) if birthday_str else None

    def add_address(self, address: str) -> str:
        self.address = Address(address)
        return f"{address} was added sucessfully to {self.name.value}"

    def add_phone(self, phone_str: str) -> str:
        new_phone = Phone(phone_str)
        phone = self.find_phone(phone_str)
        if not phone:
            self.phones.append(new_phone)
            return f"{phone_str} was added sucessfully to {self.name.value}"
        else:
            return f"{phone_str} already exist"

    def add_birthday(self, birthday_str: str) -> str:
        self.birthday = Birthday(birthday_str)
        return f"{birthday_str} was added sucessfully to {self.name.value}"

    def remove_phone(self, phone_str: str) -> str:
        phone = self.find_phone(phone_str)
        if phone:
            self.phones.remove(phone)
            return f"{phone_str} was removed sucessfully from {self.name.value}"
        return f"Phone number {phone_str} was not found in the contact {self.name.value}"

    def remove_email(self, email: str) -> str:
        email = Email(email)
        if email in self.emails:
            self.emails.remove(email)
            return f"{email} was removed sucessfully from {self.name.value}"
        return f"{email} was not found in {self.name.value}"

    def remove_address(self) -> str:
        self.address = None
        return f"Address was removed sucessfully from {self.name.value}"

    def remove_birthday(self) -> str:
        self.birthday = None
        return f"Birthday was removed sucessfully from {self.name.value}"

    def edit_phone(self, phone_str: str, new_phone: str) -> str:
        phone = self.find_phone(phone_str)
        if phone:
            self.phones.remove(phone)
            self.phones.append(Phone(new_phone))
            return f"{phone_str} was changed to {new_phone} sucessfully for the contact {self.name.value}"
        else:
            raise ValueError(
                f"Phone number {phone_str} was not found in the contact {self.name.name}")

    def add_email(self, email: str) -> str:
        email = Email(email)
        if email not in self.emails:
            self.emails.append(email)
            return f"{email} was added sucessfully to {self.name.value}"
        return f"{email} already exist in {self.name.value}"

    def edit_email(self, email: str, new_email: str) -> str:
        email = Email(email)
        new_email = Email(new_email)
        if email == new_email:
            return f"New and old emails are the same {email} = {new_email} in {self.name.value}"
        if email in self.emails:
            # self.emails.remove(email)
            # self.emails.append(new_email)
            self.emails[self.emails.index(email)] = new_email
            return f"{email} was changed to {new_email} sucessfully for the contact {self.name.value}"
        return f"{email} was not found in {self.name.value}"

    def find_phone(self, phone_str: str) -> str | None:
        phone = None
        for p in self.phones:
            if p.value == phone_str:
                phone = p
                break
        return phone

    def find_email(self, email_str: str) -> str | None:
        email = None
        for e in self.emails:
            if e.value == email_str:
                email = e
                break
        return email

    def days_to_birthday(self, birth_date):
        current_date = datetime.now().date()
        birthday = birth_date.replace(year=current_date.year)
        birthday = birthday.replace(
            year=current_date.year+1) if birthday < current_date else birthday
        delta = (birthday-current_date).days
        return f'{delta}'

    def __str__(self):
        name_str = f"{Fore.BLUE}Contact: {self.name.value:{20}}{Style.RESET_ALL}"
        phones_str = ' '.join(p.value for p in self.phones)
        emails_str = " ".join(e.value for e in self.emails)
        address_str = f"{Fore.GREEN}{self.address.value}{Style.RESET_ALL}" if self.address else ""
        date_str = (
            f"{Fore.YELLOW}{datetime.strftime(self.birthday.value, '%d.%m.%Y'):{10}}, {Style.RESET_ALL}"
            f"{self.days_to_birthday(self.birthday.value)} days to the next birthday!{Style.RESET_ALL}"
        ) if self.birthday else ""
        return f"{name_str} {phones_str} {emails_str} {address_str} {date_str}"

    # def __str__(self):
    #     name_str = f"Contact: {self.name.value}"
    #     phones_str = ' '.join(p.value for p in self.phones)
    #     emails_str = " ".join(e.value for e in self.emails)
    #     address_str = self.address.value if self.address else ""
    #     date_str = f"{datetime.strftime(self.birthday.value, '%d.%m.%Y')}, {self.days_to_birthday(self.birthday.value)}" if self.birthday else ""
    #     return f"{name_str} {phones_str} {emails_str} {address_str} {date_str}"
    #     # return f"{self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, {emails_str}, {address_str}, birthday: {date_str}, {self.days_to_birthday(self.birthday.value)}"
    #     # return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)} {emails_str}, {address_str}"


class AddressBook(UserDict):
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.data = {}
        if not os.path.isfile(file_name):
            self.create_empty_file(file_name)

        self.load_data(self.file_name)

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return f"{record.name.value} was added sucessfully"

    def find(self, name: str):
        if name in self.data.keys():
            return self.data[name]
        return None

    def delete(self, name: str):
        self.data.pop(name, None)
        return f"{name} was deleted sucessfully"

    def iterator(self, n=2):
        records = 0
        while records < len(self):
            yield list(self.values())[records: records + n]
            records += n

    def load_data(self, file_name: str):
        with open(file_name, "rb") as f:
            self.data = pickle.load(f)
        return (f"Data loaded from file {file_name}. Total users in the phone book: {len(self.data)}")

    def save_data(self, file_name: str):
        with open(file_name, "wb") as f:
            pickle.dump(self.data, f)
        return (f"Data saved to file. Total users in the phone book: {len(self.data)}")

    def create_empty_file(self, file_name: str):
        with open(file_name, "xb") as f:
            pickle.dump(self.data, f)
        return (f"Phone book file {file_name} was created")


class NoteBook(UserDict):
    def __init__(self, notes_file_name: str):
        self.file_name = notes_file_name
        self.data = {}
        if not os.path.isfile(notes_file_name):
            self.create_empty_file(notes_file_name)
        self.load_data(self.file_name)

    def add_record(self, note: Note):
        self.data[note.title.value] = note
        return f"Note '{note.title.value}' was added sucessfully"

    def edit_record(self, note: Note) -> str:
        self.data[note.title.value] = note
        return f"Note '{note.title.value}' was changed sucessfully"

    def find(self, name: str):
        if name in self.data.keys():
            return self.data[name]
        return None

    def delete(self, name: str):
        self.data.pop(name, None)
        return f"{name} was deleted sucessfully"

    def iterator(self, n=2):
        records = 0
        while records < len(self):
            yield list(self.values())[records: records + n]
            records += n

    def load_data(self, file_name: str):
        with open(file_name, "rb") as f:
            self.data = pickle.load(f)
        return (f"Data loaded from file {file_name}. Total notes in the notes book: {len(self.data)}")

    def save_data(self, file_name: str):
        with open(file_name, "wb") as f:
            pickle.dump(self.data, f)
        return (f"Data saved to file. Total notes in the notes book: {len(self.data)}")

    def create_empty_file(self, file_name: str):
        with open(file_name, "xb") as f:
            pickle.dump(self.data, f)
        return (f"Notes book file {file_name} was created")


def main():
    ...


if __name__ == "__main__":
    main()

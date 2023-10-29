from collections import UserDict
from datetime import datetime
import re
from birthday import *


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if value is None:
            raise ValueError("invalid name")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        pattern = r'^\d{10}$'
        if value is not None and re.match(pattern, value):
            super().__init__(value)
        else:
            raise ValueError("invalid phone")


class Birthday:
    date = None

    def __init__(self, date):
        try:
            date = datetime.strptime(date, "%d.%m.%Y")
        except ValueError:
            raise ValueError("invalid format. try format DD.MM.YYYY")
        if date >= datetime.now():
            raise ValueError("birthday can not be in future")
        self.date = date


class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(phone)

    def edit_phone(self, new):
        self.phones = []
        self.phones.append(new)

    def find_phone(self, number):
        return next(iter([i for i in self.phones if i == number]), None)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_birthday(self, new_birthday: Birthday):
        self.birthday = new_birthday

    def show_birthday(self):
        return self.birthday

    def __getitem__(self, index):
        if index == "name":
            return self.name
        elif index == "birthday":
            return self.birthday
        else:
            return None


class AddressBook(UserDict):

    def add_record(self, rec: Record):
        self.data[rec.name.value] = rec

    def find(self, search_name):
        return self.data[search_name] if search_name in self.data else None

    def delete(self, search_name):
        del self.data[search_name]

    def get_birthdays_per_week(self):
        get_birthdays_per_week(self.data)

    def print_birthdays_per_week(self):
        print_birthdays_per_week(self.data)

    def all(self):
        for k, v in self.data.items():
            print(v)

from collections import UserDict
from datetime import datetime
import re
from birthday import *


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def to_dict(self):
        return self.__dict__


class Name(Field):
    def __init__(self, value):
        if value is None:
            raise ValueError("invalid name")
        super().__init__(value)

    def to_dict(self):
        return self.__dict__


class Phone(Field):
    def __init__(self, value):
        pattern = r'^\d{10}$'
        if value is not None and re.match(pattern, value):
            super().__init__(value)
        else:
            raise ValueError("invalid phone")


class Birthday:
    date = None

    def __init__(self, date = None):
        if not date is None:
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
        self.birthday = None
        self.phones = None

    def add_phone(self, phone):
        self.phones = phone

    def edit_phone(self, new):
        self.phones = new

    def __str__(self):
        return f"Contact name: {self.name.value}, phone: {self.phones}"

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

    def to_dict(self):
        return {
            "name": self.name.value,
            "phone": self.phones.value,
            "birthday": self.birthday.date.isoformat() if self.birthday else None
        }
    @classmethod
    def from_dict(cls, record_data):
        r = Record(record_data['name'])
        r.add_phone(Phone(record_data['phone']))
        birthday = record_data['birthday']
        if not birthday is None:
            b = Birthday()
            b.date = datetime.fromisoformat(birthday)
            r.birthday = b
        return  r


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

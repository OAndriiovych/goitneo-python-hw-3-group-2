from typing import List, Dict, Tuple

import os
from contact import *
import pickle
import json


class Bot:
    book = AddressBook()

    def add(self, name=None, phone=None):
        try:
            phone = Phone(phone)
        except ValueError as e:
            print(e)
            return

        find = self.book.find(name)
        if find is None:
            find = Record(name)
            self.book.add_record(find)
        find.add_phone(phone)

    def change(self, name=None, new_phone=None):
        try:
            new_phone = Phone(new_phone)
        except ValueError as e:
            print(e)

        find = self.book.find(name)
        if find is None:
            find = Record(name)
            self.book.add_record(find)
            find.add_phone(new_phone)
        else:
            find.edit_phone(new_phone)

    def phone(self, name=None):
        find = self.book.find(name)
        if find is not None:
            print(str(find))
        else:
            print("there is no contact with name " + name)

    def all(self):
        self.book.all()

    def add_birthday(self, name=None, birthday=None):
        find = self.book.find(name)
        if find is not None:
            try:
                find.add_birthday(Birthday(birthday))
            except ValueError as e:
                print(e)
        else:
            print("there is no contact with name " + name)

    def show_birthday(self, name=None):
        find = self.book.find(name)
        if find is not None:
            birthday = find.show_birthday()
            print(birthday if birthday is not None else 'contact has not birthday')
        else:
            print("there is no contact with name " + name)

    def birthdays(self):
        self.book.print_birthdays_per_week()


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    cmd, *args = user_input.strip().lower().split()
    return cmd, args


def save_to_file(data, filename):
    serializable_data = {key: record.to_dict() for key, record in data.items()}
    with open(filename, 'w') as file:
        json.dump(serializable_data, file)


def load_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            bot = Bot()
            bot.book.data =  {name: Record.from_dict(record_data) for name, record_data in data.items()}
            return bot
    except FileNotFoundError:
        return {}

def main():
    filename = "cache"
    bot = None
    if os.path.exists(filename):
        bot = load_from_file(filename)
    else:
        bot = Bot()


    while True:
        user_input = input("> ")
        command, args = parse_input(user_input)
        i = iter(args)
        f = next(i, None)
        s = next(i, None)
        if command == "hello":
            print("How can I help you?")
        elif command == "add":
            bot.add(f, s)
        elif command == "change":
            bot.change(f, s)
        elif command == "phone":
            bot.phone(f)
        elif command == "all":
            bot.all()
        elif command == "add-birthday":
            bot.add_birthday(f, s)
        elif command == "show-birthday":
            bot.show_birthday(f)
        elif command == "birthdays":
            bot.birthdays()
        elif command in ["close", "exit"]:
            save_to_file(bot.book,filename)
            print("Good bye!")
            break
        else:
            print("Invalid command.")




main()

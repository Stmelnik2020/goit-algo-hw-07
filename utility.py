from collections import UserDict
from datetime import datetime, date, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):

    def __init__(self, value: str):
        if not Phone.validate(value):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)

    @staticmethod
    def validate(value: str) -> bool:
        return value.strip().isdigit() and len(value.strip()) == 10


class Birthday(Field):
    def __init__(self, value: str):
        try:
            date_value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(date_value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday_date: Birthday):
        self.birthday = birthday_date

    def find_phone(self, searched_phone: str):
        for phone in self.phones:
            if phone.value == searched_phone:
                return phone

    def edit_phone(self, old_number: str, new_number: str):
        if not Phone.validate(new_number):
            raise ValueError(f"{new_number} not valid phone number!")
        self.remove_phone(old_number)
        self.add_phone(new_number)

    def remove_phone(self, removing_phone):
        phone = self.find_phone(removing_phone)
        if phone:
            self.phones.remove(phone)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, users, days=7):
        upcoming_birthdays = []
        today = date.today()
        for user in users:
            birthday_this_year = user["birthday"].replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(
                    year=today.year+1)
            if 0 < (birthday_this_year - today).days <= days:
                birthday_this_year = AddressBook.adjust_for_weekend(
                    birthday_this_year)
                congratulation_date_str = AddressBook.date_to_string(
                    birthday_this_year)
                upcoming_birthdays.append(

                    {"name": user["name"], "congratulation_date": congratulation_date_str})
        return upcoming_birthdays

    @staticmethod
    def string_to_date(date_string):
        return datetime.strptime(date_string, "%d.%m.%Y").date()

    @staticmethod
    def date_to_string(input_date):
        return input_date.strftime("%d.%m.%Y")

    @staticmethod
    def prepare_user_list(user_data):
        prepared_list = []
        for user in user_data:
            prepared_list.append(
                {"name": user["name"], "birthday": AddressBook.string_to_date(user["birthday"])})
        return prepared_list

    @staticmethod
    def find_next_weekday(start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    @staticmethod
    def adjust_for_weekend(birthday):
        if birthday.weekday() >= 5:
            return AddressBook.find_next_weekday(birthday, 0)
        return birthday

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

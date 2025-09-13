from addressbook import AddressBook, Record, Birthday


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command"
        except KeyError:
            return "Contact not defined!"
    return inner


@input_error
def parse_input(user_input: str) -> list[str]:
    """
    takes a user input string user_input and splits it into words 
    using the split() method. It returns the first word as the 
    command cmd and the rest as a list of arguments *args
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday_str, *_ = args
    record = book.find(name)
    birthday_str = Birthday(birthday_str)
    if record is None:
        return "Contact not defined!"
    record.add_birthday(birthday_str)
    return "Contact birthday update!"


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        return f"Birthday {name} : {record.birthday.value.strftime('%d.%m.%Y')}"


@input_error
def birthdays(book: AddressBook):
    users_birthdays = []
    for record in book.data.values():
        if record.birthday:
            users_birthdays.append(
                {"name": record.name.value, "birthday": record.birthday.value})
    upcoming = book.get_upcoming_birthdays(users_birthdays, 7)
    if not upcoming:
        return "No birthdays in the next 7 days."
    return "\n".join(f"{u['name']} : {u["congratulation_date"]}" for u in upcoming)


@input_error
def change_contact(args, book: AddressBook) -> str:
    """
    stores a new phone number for the contact
    username that already exists in the dictionary
    """
    name, old_phone, new_phone = args
    record = book.find(name)
    message = "Contact updated."
    if record:
        record.edit_phone(old_phone, new_phone)
        return (message)
    else:
        raise KeyError


@input_error
def show_phone(args, book: AddressBook) -> str:
    """
    return the phone number for the
    specified contact username to the console
    """
    name = args[0]
    record = book.find(name)
    if record:
        return f"{record}"
    else:
        raise KeyError


def show_all(book: AddressBook) -> str:
    """
    return the phone number for all contacts
    """
    if not book:
        return "No contacts."
    return "\n".join(f"{name}" for name in book.values())


def main():
    # create an empty list for further filling
    book = AddressBook()
    print("Welcome to the assistant bot!")
    # an infinite loop in which the main logic of the program is processed
    while True:
        # receive input from the user
        user_input = input("Enter a command: ")
        # separate user input into commands and arguments
        command, *args = parse_input(user_input)
        # condition for completing an infinite loop
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        # condition for making changes to an existing contact
        elif command == "change":
            print(change_contact(args, book))
        # condition for displaying one contact in the console
        elif command == "phone":
            print(show_phone(args, book))
        # condition for displaying all contacts in the console
        elif command == "all":
            print(show_all(book))
        # condition for displaying a welcome message
        elif command == "hello":
            print("How can I help you?")
        # condition for adding new phone number to dictionary
        elif command == "add":
            print(add_contact(args, book))
        # condition for all unforeseen commands
        elif command == "add_birthday":
            print(add_birthday(args, book))
        elif command == "show_birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

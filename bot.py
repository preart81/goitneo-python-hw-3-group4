from bot_classes import *
import pickle

file = "data.dat"


class colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    END = "\033[0m"


def input_error(error_message=""):
    def error_decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error_detail:
                error_detail = str(error_detail) or "no details"
                error_descr = f"Error. {error_message} Details: {error_detail}"
                return colors.RED + error_descr + colors.END

        return inner

    return error_decorator


@input_error("Can`t parse the input")
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error("Can't add contact. Give me name and phone please.")
def add_contact(args, book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    # book[name].add_phone(phone)
    return "Contact added."


@input_error("Can't change contact. Give me name, old_phone, new_phone please.")
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    if name in book.data.keys():
        if old_phone in map(str, book[name].phones):
            book[name].edit_phone(old_phone, new_phone)
            return "Contact changed."
        else:
            raise IndexError(f"Phone {old_phone} not found")
    else:
        raise IndexError("Name not found")


@input_error("Can`t show phone.")
def show_phone(args, book: AddressBook):
    name = args[0]
    if name in book.keys():
        phone_list = ",".join(map(str, book[name].phones))
        return phone_list
    else:
        raise IndexError("Name not found")


@input_error("Can't change birthday.")
def add_birthday(args, book: AddressBook):
    """add-birthday [ім'я] [дата народження]: Додати дату народження для вказаного контакту."""
    name, birthday = args
    if name in book.keys():
        book[name].add_birthday(birthday)
        return "Birthday added"
    else:
        raise IndexError("Name not found")


@input_error("Can't show birthday.")
def show_birthday(args, book: AddressBook):
    """show-birthday [ім'я]: Показати дату народження для вказаного контакту."""
    name = args[0]
    if name in book.keys():
        # birthday = datetime.strftime(book[name].birthday.value, r"%d.%m.%Y")
        return f"{name}'s birthday is {book[name].birthday}"
    else:
        raise IndexError("Name not found")


@input_error("Can't show birthday.")
def birthdays(book: AddressBook):
    """birthdays - повертає список користувачів, яких потрібно привітати по днях на наступному тижні"""
    return book.get_birthdays_per_week()


@input_error()
def show_all(book: AddressBook):
    all_list = ""
    all_list = "\n".join(map(str, book.values()))
    # for record in book.values():
    # all_list += f"{record\n"
    return all_list.removesuffix("\n")


def main():
    print("Welcome to the assistant bot!")
    book = AddressBook()
    try:
        with open(file, "rb") as fh:
            book = pickle.load(fh)
            print("Book loaded")
    except:
        print(f"Config file {file} not found. Ccreated new empty book.")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            with open(file, "wb") as fh:
                pickle.dump(book, fh)
                print("Book saved.")
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            """show-birthday [ім'я]: Показати дату народження для вказаного контакту."""
            print(show_birthday(args, book))

        elif command == "birthdays":
            """birthdays - повертає список користувачів, яких потрібно привітати по днях на наступному тижні"""
            print(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

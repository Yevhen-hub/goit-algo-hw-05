# Task 4
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except KeyError:
            return "Контакт не знайдено. Перевірте ім'я."

        except ValueError:
            return "Помилка: дайте мені ім'я і телефон."

        except IndexError:
            return "Помилка: передайте аргумент для команди."

    return inner


@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone

    return f"Контакт '{name}' додано."


@input_error
def change_contact(args, contacts):
    name, phone = args
    contacts[name] = phone

    return f"Контакт '{name}' оновлено."


@input_error
def get_phone(args, contacts):
    name = args[0]

    return f"{name}: {contacts[name]}"


@input_error
def get_all_contacts(args, contacts):
    if not contacts:
        return "Контактів не збережено."

    result = ""

    for name, phone in contacts.items():
        result += f"{name}: {phone}\n"

    return result.strip()


def parse_input(user_input: str):
    parts = user_input.strip().split()

    if not parts:
        return None, []

    command = parts[0].lower()
    args = parts[1:]

    return command, args


def main():
    contacts = {}

    print("Привіт! Я твій помічник з контактами.")
    print("Команди: add, change, phone, all, hello, exit\n")

    while True:
        user_input = input("Введи команду: ").strip()

        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command is None:
            continue

        if command == "exit" or command == "quit":
            print("До побачення!")
            break

        elif command == "hello":
            print("Привіт! Чим я можу тобі допомогти?")

        elif command == "add":
            result = add_contact(args, contacts)
            print(result)

        elif command == "change":
            result = change_contact(args, contacts)
            print(result)

        elif command == "phone":
            result = get_phone(args, contacts)
            print(result)

        elif command == "all":
            result = get_all_contacts(args, contacts)
            print(result)

        else:
            print("Невідома команда. Спробуй ще раз.")


if __name__ == "__main__":
    main()
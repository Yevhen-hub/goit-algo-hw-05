# Task 1

def caching_fibonacci():
    cache = {}

    def fibonacci(n):
        if n <= 0:
            return 0
        if n == 1:
            return 1

        if n in cache:
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


fib = caching_fibonacci()
print(fib(10))
print(fib(15))

# Task 2

import re
from typing import Callable


def generator_numbers(text: str):
    pattern = r'\b\d+\.\d+\b|\b\d+\b'
    matches = re.findall(pattern, text)

    for match in matches:
        yield float(match)


def sum_profit(text: str, func: Callable) -> float:
    total = 0
    for number in func(text):
        total += number
    return total


text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")

# Task 3

import sys
from collections import defaultdict
from typing import Dict, List


def parse_log_line(line: str) -> dict:
    parts = line.split()

    if len(parts) < 4:
        return {}

    return {
        'date': parts[0],
        'time': parts[1],
        'level': parts[2],
        'message': ' '.join(parts[3:])
    }


def load_logs(file_path: str) -> List[dict]:
    logs = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                log = parse_log_line(line.strip())
                if log:
                    logs.append(log)
    except FileNotFoundError:
        print(f"Помилка: Файл '{file_path}' не знайдено.")
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")

    return logs


def filter_logs_by_level(logs: List[dict], level: str) -> List[dict]:
    return [log for log in logs if log['level'].upper() == level.upper()]


def count_logs_by_level(logs: List[dict]) -> Dict[str, int]:
    counts = defaultdict(int)

    for log in logs:
        counts[log['level']] += 1

    return dict(counts)


def display_log_counts(counts: Dict[str, int]):
    print(f"\n{'Рівень логування':<20} | {'Кількість':<10}")
    print("-" * 35)

    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)

    for level, count in sorted_counts:
        print(f"{level:<20} | {count:<10}")


def main():
    if len(sys.argv) < 2:
        print("Використання: python task3_log_analyzer.py <шлях_до_логу> [рівень]")
        return

    file_path = sys.argv[1]
    logs = load_logs(file_path)

    if not logs:
        print("Немає логів для обробки.")
        return

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if len(sys.argv) > 2:
        level = sys.argv[2].upper()
        filtered = filter_logs_by_level(logs, level)

        if filtered:
            print(f"\nДеталі логів для рівня '{level}':")
            for log in filtered:
                print(f"{log['date']} {log['time']} - {log['message']}")
        else:
            print(f"\nЛоги з рівнем '{level}' не знайдені.")


if __name__ == "__main__":
    main()

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


contacts = {}


@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError
    name, phone = args
    contacts[name] = phone
    return f"Контакт '{name}' додано."


@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise ValueError
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return f"Контакт '{name}' оновлено."


@input_error
def get_phone(args, contacts):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    if name not in contacts:
        raise KeyError
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
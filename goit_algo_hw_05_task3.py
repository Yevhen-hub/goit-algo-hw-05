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

    sorted_counts = sorted(
        counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

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
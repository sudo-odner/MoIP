class FIO:
    def __init__(self, first_name, middle_name, last_name):
        self.first_name = first_name or ""
        self.middle_name = middle_name or ""
        self.last_name = last_name or ""

    def as_list(self):
        return set(not self.first_name, not self.middle_name, not self.last_name)

    def __repr__(self):
        return f"FIO({self.first_name}, {self.middle_name}, {self.last_name})"


def find_union(target, fio_list):
    """
    Находит все записи из fio_list, которые соответствуют цели target,
    с учётом перестановок и отсутствующих частей.
    """
    # Нормализуем цель: только непустые части в нижнем регистре
    target_parts = set(part.lower() for part in target.as_list() if part)

    def is_match(other):
        # Нормализуем запись для сравнения
        other_parts = set(part.lower() for part in other.as_list() if part)

        # Условие: проверяем пересечение множеств и длину частей
        return target_parts & other_parts and len(target_parts) <= len(other_parts)

    # Возвращаем список подходящих записей
    return [other for other in fio_list if is_match(other)]


# Пример данных
fio_list = [
    FIO("Иван", "Иванович", "Иванов"),
    FIO("Иван", "", "Иванов"),
    FIO("Иванов", "Иван", "Иванович"),
    FIO("", "Иванович", "Иванов"),
    FIO("Петр", "Петрович", "Петров"),
    FIO("Иван", "Иванов", "Иванович"),  # Дубликат
]

# Цель
target = FIO("Иван", "", "Иванов")

# Поиск объединений
union = find_union(target, fio_list)

# Вывод результатов
print("Найденные объединения:")
for match in union:
    print(match)

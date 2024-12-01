import json


class Book:
    """Класс, представляющий книгу в библиотеке."""

    def __init__(
            self,
            title: str,
            author: str,
            year: int,
            status: str = "в наличии"
    ) -> None:
        """
        Создание книги.

        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания.
        :param status: Статус книги (по умолчанию "в наличии").
        """
        self.id = self.generate_id()
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    @staticmethod
    def generate_id() -> int:
        """Генерация уникального ID для книги."""
        data = Library.load_data()
        if not data:
            return 1
        return max(book["id"] for book in data) + 1

    def to_dict(self) -> dict:
        """Преобразование книги в словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }


class Library:
    """Класс для управления библиотекой книг."""

    DATA_FILE = "library.json"

    @staticmethod
    def load_data() -> list[dict]:
        """Загрузка данных из файла."""
        try:
            with open(Library.DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_data(data: list[dict]) -> None:
        """Сохранение данных в файл."""
        with open(Library.DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def add_book(title: str, author: str, year: int) -> None:
        """Добавление новой книги в библиотеку."""
        book = Book(title, author, year)
        data = Library.load_data()
        data.append(book.to_dict())
        Library.save_data(data)
        print(f"Книга '{title}' добавлена с ID {book.id}.")

    @staticmethod
    def delete_book(book_id: int) -> None:
        """Удаление книги по ID."""
        data = Library.load_data()
        filtered_data = [book for book in data if book["id"] != book_id]
        if len(filtered_data) == len(data):
            print(f"Книга с ID {book_id} не найдена.")
        else:
            Library.save_data(filtered_data)
            print(f"Книга с ID {book_id} удалена.")

    @staticmethod
    def search_books(query: str, field: str) -> None:
        """Поиск книг по полю."""
        data = Library.load_data()
        results = [book for book in data if query.lower()
                   in str(book[field]).lower()]
        if results:
            print("Найденные книги:")
            for book in results:
                print(Library.format_book(book))
        else:
            print(f"Книги с {field} '{query}' не найдены.")

    @staticmethod
    def list_books() -> None:
        """Вывод всех книг."""
        data = Library.load_data()
        if data:
            print("Список всех книг:")
            for book in data:
                print(Library.format_book(book))
        else:
            print("Библиотека пуста.")

    @staticmethod
    def update_status(book_id: int, new_status: str) -> None:
        """Обновление статуса книги."""
        if new_status not in ["в наличии", "выдана"]:
            print("Некорректный статус. "
                  "Допустимые значения: 'в наличии', 'выдана'.")
            return

        data = Library.load_data()
        for book in data:
            if book["id"] == book_id:
                book["status"] = new_status
                Library.save_data(data)
                print(f"Статус книги с ID {book_id} "
                      f"обновлён на '{new_status}'.")
                return

        print(f"Книга с ID {book_id} не найдена.")

    @staticmethod
    def format_book(book: dict) -> str:
        """Форматированный вывод данных о книге."""
        return (f"ID: {book['id']},"
                f" Название: {book['title']},"
                f" Автор: {book['author']},"
                f" Год: {book['year']}, "
                f"Статус: {book['status']}")


def main():
    """Точка входа в приложение."""
    while True:
        print("\nУправление библиотекой:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выход")
        choice = input("Введите номер действия: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания: "))
            Library.add_book(title, author, year)
        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            Library.delete_book(book_id)
        elif choice == "3":
            field = input(
                "По какому полю искать (title, author, year): ").strip()
            query = input(f"Введите значение для поиска по {field}: ")
            Library.search_books(query, field)
        elif choice == "4":
            Library.list_books()
        elif choice == "5":
            book_id = int(input("Введите ID книги: "))
            new_status = input(
                "Введите новый статус (в наличии/выдана): ").strip()
            Library.update_status(book_id, new_status)
        elif choice == "6":
            print("До свидания!")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()

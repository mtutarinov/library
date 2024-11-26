import json
from collections import defaultdict
from dataclasses import dataclass
from json import JSONDecodeError
from typing import Dict, List, ItemsView, Generator
from contextlib import contextmanager

from exception import IdNotFoundException, ValueNotFoundException


@dataclass
class Book:
    """ Датаклас книга. """
    title: str
    author: str
    year: int
    id: int | None = None
    status: str = 'В наличии'


class Library:
    """
    Представляет библиотеку.

    Attributes:
        data_books: словарь с книгами
        index: индекс

    Methods:
        add_book: добавляет книгу
        delete_book: удаление книги
        search_book: ищет книгу
        change_status: изменяет статус книги
        show_books: показывает все книги в библиотеке
        close: сохраняет данные в JSON-файл при закрытии
        lock: контекстный менеджер для автоматического сохранения данных
    """
    STATUS_IN_STOCK = "В наличии"
    STATUS_OUT_OF_STOCK = "выдана"

    def __init__(self) -> None:
        """
        Инициализирует data_books данными из JSON-файла, либо пустым словарем.

        Загружает индекс.
        """
        self.data_books: Dict[int, dict] = dict()
        self.index: LibraryIndex = LibraryIndex()
        try:
            with open('data.json', 'r') as f:
                self.data_books = {int(key): value for key, value in json.load(f).items()}
                self.index.load_from_file()
        except FileNotFoundError:
            # Замалчиваем, потому что штатная ситуация при первом запуске приложения.
            pass
        except JSONDecodeError:
            print('Нечитаемый формат файла.')

    def add_book(self, book: Book) -> None:
        """ Добавляет книгу в библиотеку. Присваивает книге id, обновляет индекс."""
        if not self.data_books:
            book.id = 1
        else:
            book.id = max(self.data_books.keys()) + 1
        self.data_books[book.id]: Dict[int,dict] = {'title': book.title, 'author': book.author, 'year': book.year,
                                    'status': book.status}
        self.index.update(book)

    def delete_book(self, id: int) -> None:
        """ Удаляет книгу из библиотеки. Обновляет индекс."""
        try:
            self.data_books[id]
        except KeyError:
            raise IdNotFoundException
        book = self.data_books[id]
        title, author, year = book['title'], book['author'], book['year']
        self.data_books.pop(id)
        self.index.delete(id, title, author, year)

    def search_book(self, field: str, value: str | int) -> list:
        """Поиск книги по автору, названию или году."""
        library = self.data_books
        data = self.index.search(field, value)
        result = list()
        for id in data:
            result.append((id, library[id]))
        return result

    def change_status(self, id: int) -> None:
        """Изменение статуса книги с "в наличии" на "выдана" или наоборот."""
        try:
            book = self.data_books[id]
        except KeyError:
            raise IdNotFoundException
        if book['status'] == self.STATUS_OUT_OF_STOCK:
            book['status'] = self.STATUS_IN_STOCK
        else:
            book['status'] = self.STATUS_OUT_OF_STOCK

    def show_books(self) -> ItemsView[int, dict]:
        """ Возвращает пары id книга."""
        return self.data_books.items()

    def close(self) -> None:
        """Сохраняет данные в JSON-файл."""
        with open('data.json', 'w') as f:
            json.dump(self.data_books, f)
        self.index.close()

    @contextmanager
    def lock(self) -> Generator["Library", None, None]:
        """Контекстный менеджер."""
        try:
            yield self
        finally:
            self.close()


class LibraryIndex:
    """ Класс, который индексирует данные для более быстрого поиска книг."""
    data: Dict[str, Dict[str | int, set[int]]] = defaultdict(dict)
    gradation: Dict[str, dict] = defaultdict(dict)


    def load_from_file(self) -> None:
        """ Десериализует данные."""
        try:
            with open('index.json', 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, JSONDecodeError):
            return
        self.data['data_author'] = {key: set(value) for key, value in
                                                         data['data_author'].items()}
        self.data['data_year'] = {int(key): set(value) for key, value in
                                                       data['data_year'].items()}
        self.data['data_title'] = {key: set(value) for key, value in
                                                        data['data_title'].items()}
        self.gradation['author'] = self.data['data_author']
        self.gradation['year'] = self.data['data_year']
        self.gradation['title'] = self.data['data_title']

    def update(self, book: Book) -> None:
        """ Обновляет индекс под новую книгу."""
        data_type = [self.data['data_title'], self.data['data_author'], self.data['data_year']]
        data_book = [book.title, book.author, book.year]
        for data, key in zip(data_type, data_book):
            try:
                data[key].add(book.id)
            except KeyError:
                data[key] = {book.id}

    def delete(self, id: int, title: str, author: str, year: int) -> None:
        """Удаляет данные из индекса."""
        data_type = [self.data['data_title'], self.data['data_author'], self.data['data_year']]
        data_book = [title, author, year]
        for data, key in zip(data_type, data_book):
            if len(data[key]) == 1:
                data.pop(key)
            else:
                data[key].remove(id)

    def search(self, field: str, value: str | int)-> List[int]:
        """Поиск по индексу."""
        try:
            return self.gradation[field][value]
        except KeyError:
            return []


    def close(self) -> None:
        """Сериализует данные."""
        with open('index.json', 'w') as f:
            data = dict()
            data['data_title'] = {key: list(value) for key, value in self.data['data_title'].items()}
            data['data_author'] = {key: list(value) for key, value in self.data['data_author'].items()}
            data['data_year'] = {key: list(value) for key, value in self.data['data_year'].items()}
            json.dump(data, f)

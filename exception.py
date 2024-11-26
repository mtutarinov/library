class LibraryBaseException(Exception):
    """Базовый класс для исключений в библиотеке."""
    pass


class IdNotFoundException(LibraryBaseException):
    """Исключение, возникающее, когда id не найден."""

    def __init__(self):
        super().__init__("id не найден")


class NotANumberException(LibraryBaseException):
    """Исключение, возникающее, когда ввод не является числом."""

    def __init__(self, value):
        super().__init__(f"Введённое значение {value} - не является годом")


class NotSearchFieldException(LibraryBaseException):
    """ Исключение, возникающее если неправильно передан тип поля для поиска. """

    def __init__(self, value):
        super().__init__(f'{value}: По данному типу поля нельзя найти книгу')

class ValueNotFoundException(LibraryBaseException):
    """ Исключение возникающее, если при поиске по полю, передано несуществующее значение. """

    def __init__(self, value):
        super().__init__(f'{value}: По данному значению книга не найдена')

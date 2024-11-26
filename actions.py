from library import Book, Library
from exception import IdNotFoundException, NotANumberException, NotSearchFieldException, ValueNotFoundException


def add_book(library: Library):
    """Добавляет книгу в библиотеку."""
    title = input('Введите название книги: ')
    author = input('Ввдедите автора книги: ')
    year = input('Введите год издания: ')
    try:
        year = int(year)
    except ValueError:
        print(f'{year}: Не является годом.')
        return
    book = Book(title, author, year)
    library.add_book(book)
    print(f'Книга успешно добавлена в библиотеку. Ее id {book.id}.')


def delete_book(library: Library):
    """Удаляет книгу из библиотеки."""
    try:
        id = int(input('Введите id книги, которую хотите удалить: '))
    except ValueError:
        print('Не является числом.')
        return
    try:
        library.delete_book(id)
    except IdNotFoundException as e:
        print(e)
    else:
        print('Книга удалена')


def _search_type(field: str) -> str:
    """Переводит пользовательскую команду в техническое поле."""
    search_fields = {
        'название': 'title',
        'автор': 'author',
        'год': 'year'
    }
    try:
        return search_fields[field]
    except KeyError:
        raise NotSearchFieldException(value=field)


def search_book(library: Library):
    """Осуществляет поиск по полю."""
    print(
        'Поиск в библиотеке осуществляется по следующим типам полей: название, автор и год. Поиск по другим полям не возможен.')
    field = input('Введите тип поля по которому хотите найти книгу: ')
    try:
        field = _search_type(field)
    except NotSearchFieldException as e:
        print(e)
        return
    value = input('Введите значение поля: ')
    if field == 'year':
        try:
            value = int(value)
        except ValueError:
            print('Не является числом')
            return
    result = library.search_book(field, value)
    if not result:
        print('Книги не найдены.')
    for id, book in result:
        print(
            f"id: {id} Название: {book['title']} Автор: {book['author']} Год: {book['year']} Статус: {book['status']}")


def change_book_status(library: Library):
    """Изменяет статус книги."""
    id = input('Введите id книги: ')
    try:
        id = int(id)
    except ValueError:
        print(f'{id}: Не является числом.')
        return
    try:
        library.change_status(id)
    except IdNotFoundException as e:
        print(e)
        return
    print('Статус изменен.')


def show_books(library):
    print('Список книг в библиотеке:')
    result = library.show_books()
    for id, book in result:
        print(
            f"id: {id} Название: {book['title']} Автор: {book['author']} Год: {book['year']} Статус: {book['status']}")


action_dispatcher = {
    'create': add_book,
    'delete': delete_book,
    'search': search_book,
    'change_status': change_book_status,
    'show': show_books
}

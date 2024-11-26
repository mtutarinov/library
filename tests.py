from library import Library, Book
from exception import IdNotFoundException


def test_add_book():
    library = Library()
    library.data_books = {}
    book = Book('test', 'test', 1992)
    library.add_book(book)
    assert 1 in library.data_books
    assert len(library.data_books) == 1
    assert library.data_books[1]['title'] == 'test'
    assert library.data_books[1]['author'] == 'test'
    assert library.data_books[1]['status'] == 'В наличии'
    assert library.data_books[1]['year'] == 1992
    print('Test passed')


def test_delete_book():
    library = Library()
    library.data_books = {}
    book = Book('test', 'test', 1992)
    library.add_book(book)
    library.delete_book(1)
    assert 1 not in library.data_books
    assert library.data_books == {}
    print('Test passed')


def test_delete_book_wrong_id():
    library = Library()
    library.data_books = {}
    book = Book('test', 'test', 1992)
    library.add_book(book)
    try:
        library.delete_book(2)
    except IdNotFoundException:
        print('Test passed')


def test_show_books():
    library = Library()
    library.data_books = {}
    book_a = Book('a_test', 'a_test', 1992)
    book_b = Book('b_test', 'b_test', 1990)
    library.add_book(book_a)
    library.add_book(book_b)
    assert 1 in library.data_books
    assert 2 in library.data_books
    assert len(library.data_books) == 2
    assert library.data_books[1]['title'] == 'a_test'
    assert library.data_books[1]['author'] == 'a_test'
    assert library.data_books[1]['status'] == 'В наличии'
    assert library.data_books[1]['year'] == 1992
    assert library.data_books[2]['title'] == 'b_test'
    assert library.data_books[2]['author'] == 'b_test'
    assert library.data_books[2]['status'] == 'В наличии'
    assert library.data_books[2]['year'] == 1990
    print('Test passed')


def test_change_status_in_stock():
    library = Library()
    library.data_books = {}
    book = Book('test', 'test', 1992)
    library.add_book(book)
    assert library.data_books[1]['status'] == 'В наличии'
    library.change_status(1)
    assert library.data_books[1]['status'] == 'выдана'
    print('Test passed')


def test_change_status_out_of_stock():
    library = Library()
    library.data_books = {}
    book = Book('test', 'test', 1992)
    book.status = 'выдана'
    library.add_book(book)
    assert library.data_books[1]['status'] == 'выдана'
    library.change_status(1)
    assert library.data_books[1]['status'] == 'В наличии'
    print('Test passed')


def test_search_title_field():
    library = Library()
    library.data_books = {}
    book = Book('test_title', 'test', 1992)
    library.add_book(book)
    assert (1, library.data_books[1]) in library.search_book('title', 'test_title')
    print('Test passed')


def test_search_author_field():
    library = Library()
    library.data_books = {}
    book = Book('test', 'test_author', 1992)
    library.add_book(book)
    assert (1, library.data_books[1]) in library.search_book('author', 'test_author')
    print('Test passed')


def test_search_year_field():
    library = Library()
    library.data_books = {}
    book_a = Book('a_test', 'a_test', 1990)
    book_b = Book('b_test', 'b_test', 1990)
    library.add_book(book_a)
    library.add_book(book_b)
    assert (1, library.data_books[1]) in library.search_book('year', 1990)
    assert (2, library.data_books[2]) in library.search_book('year', 1990)
    print('Test passed')


def test_search_wrong_value():
    library = Library()
    library.data_books = {}
    book = Book('test', 'test', 1992)
    library.add_book(book)
    try:
        library.search_book('year', '2000')
    except ValueNotFoundException:
        print("Test passed")


test_add_book()
test_delete_book()
test_delete_book_wrong_id()
test_show_books()
test_change_status_in_stock()
test_change_status_out_of_stock()
test_search_title_field()
test_search_author_field()
test_search_year_field()
test_search_wrong_value()

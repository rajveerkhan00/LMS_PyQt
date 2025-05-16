class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

class BookNotAvailableError(Exception):
    pass

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, isbn):
        self.books = [book for book in self.books if book.isbn != isbn]

    def lend_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if book.is_available:
                    book.is_available = False
                    return book
                else:
                    raise BookNotAvailableError("Book already lent out")
        raise BookNotAvailableError("Book not found in library")

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.is_available = True
                return

    def __iter__(self):
        return (book for book in self.books if book.is_available)

def books_by_author(library, author_name):
    for book in library.books:
        if book.author == author_name:
            yield book

class DigitalBook(Book):
    def __init__(self, title, author, isbn, download_size):
        super().__init__(title, author, isbn)
        self.download_size = download_size

    def __str__(self):
        return f"{super().__str__()} [Download Size: {self.download_size}MB]"

class DigitalLibrary(Library):
    def add_digital_book(self, digital_book):
        self.books.append(digital_book)

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QCheckBox, QMessageBox, QTextEdit
)
from library import DigitalBook, Book, DigitalLibrary, BookNotAvailableError

lib = DigitalLibrary()

class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management System (PyQt)")
        self.setGeometry(100, 100, 500, 500)
        self.setup_ui()

    def setup_ui(self):
        # Labels and fields
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Book Title")

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Author")

        self.isbn_input = QLineEdit()
        self.isbn_input.setPlaceholderText("ISBN")

        self.ebook_checkbox = QCheckBox("Is eBook?")
        self.ebook_checkbox.stateChanged.connect(self.toggle_download_size)

        self.download_input = QLineEdit()
        self.download_input.setPlaceholderText("Download Size (MB)")
        self.download_input.setDisabled(True)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        # Buttons
        add_btn = QPushButton("Add Book")
        lend_btn = QPushButton("Lend Book")
        return_btn = QPushButton("Return Book")
        remove_btn = QPushButton("Remove Book")
        show_btn = QPushButton("Show Available Books")
        search_btn = QPushButton("Search by Author")

        # Button events
        add_btn.clicked.connect(self.add_book)
        lend_btn.clicked.connect(self.lend_book)
        return_btn.clicked.connect(self.return_book)
        remove_btn.clicked.connect(self.remove_book)
        show_btn.clicked.connect(self.show_books)
        search_btn.clicked.connect(self.search_by_author)

        # Layouts
        layout = QVBoxLayout()
        layout.addWidget(self.title_input)
        layout.addWidget(self.author_input)
        layout.addWidget(self.isbn_input)
        layout.addWidget(self.ebook_checkbox)
        layout.addWidget(self.download_input)
        layout.addWidget(add_btn)
        layout.addWidget(lend_btn)
        layout.addWidget(return_btn)
        layout.addWidget(remove_btn)
        layout.addWidget(show_btn)
        layout.addWidget(search_btn)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def toggle_download_size(self):
        self.download_input.setDisabled(not self.ebook_checkbox.isChecked())

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        isbn = self.isbn_input.text()
        is_ebook = self.ebook_checkbox.isChecked()

        if not title or not author or not isbn:
            QMessageBox.warning(self, "Missing Fields", "Please fill in all fields.")
            return

        if is_ebook:
            try:
                download_size = float(self.download_input.text())
                book = DigitalBook(title, author, isbn, download_size)
                lib.add_digital_book(book)
            except ValueError:
                QMessageBox.warning(self, "Invalid Download Size", "Enter a valid number for download size.")
                return
        else:
            book = Book(title, author, isbn)
            lib.add_book(book)

        QMessageBox.information(self, "Success", f"Book '{title}' added.")
        self.clear_inputs()

    def lend_book(self):
        isbn = self.isbn_input.text()
        try:
            lib.lend_book(isbn)
            QMessageBox.information(self, "Lend Success", f"Book with ISBN {isbn} lent out.")
        except BookNotAvailableError as e:
            QMessageBox.warning(self, "Error", str(e))

    def return_book(self):
        isbn = self.isbn_input.text()
        lib.return_book(isbn)
        QMessageBox.information(self, "Return Success", f"Book with ISBN {isbn} returned.")

    def remove_book(self):
        isbn = self.isbn_input.text()
        lib.remove_book(isbn)
        QMessageBox.information(self, "Remove Success", f"Book with ISBN {isbn} removed.")

    def show_books(self):
        self.output.clear()
        self.output.append("--- Available Books ---")
        for book in lib:
            self.output.append(str(book))

    def search_by_author(self):
        author = self.author_input.text()
        self.output.clear()
        self.output.append(f"--- Books by {author} ---")
        for book in lib.books:
            if book.author == author:
                self.output.append(str(book))

    def clear_inputs(self):
        self.title_input.clear()
        self.author_input.clear()
        self.isbn_input.clear()
        self.download_input.clear()
        self.ebook_checkbox.setChecked(False)

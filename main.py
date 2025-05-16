import sys
from PyQt5.QtWidgets import QApplication
from gui import LibraryApp

def run_app():
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()

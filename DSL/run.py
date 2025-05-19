from main_menu import MainMenu
import sys
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
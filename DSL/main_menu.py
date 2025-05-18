# main_menu.py
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QPushButton, QApplication, QTextEdit, QDialog,
                             QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from gui_interface import ChemDSL_GUI
import sys


class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ChemDSL Help")
        self.resize(800, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1b1e;
                color: #d8d8d8;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title_label = QLabel("ChemDSL Help Guide")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #61afef;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #1e1f22;
                border: none;
                border-radius: 6px;
            }
            QScrollBar:vertical {
                background: #2b2d30;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4d78cc;
                min-height: 20px;
                border-radius: 6px;
            }
        """)

        # Main help text
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setFont(QFont("Segoe UI", 11))
        help_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1f22;
                color: #d8d8d8;
                border: none;
                padding: 15px;
            }
        """)

        # Formatted help content
        help_content = """
        <h1 style="color:#61afef;">ChemDSL Documentation</h1>

        <h2 style="color:#c678dd;">Basic Syntax</h2>
        <p>ChemDSL uses a simple command-based syntax:</p>
        <ul>
            <li>Commands end with a semicolon (;)</li>
            <li>Main commands: predict, analyze, balance</li>
            <li>Chemical formulas use standard notation (H<sub>2</sub>O, NaCl, etc.)</li>
        </ul>

        <h2 style="color:#c678dd;">Command Reference</h2>
        <h3 style="color:#98c379;">predict</h3>
        <p>Predicts the outcomes of chemical reactions</p>
        <p><strong>Example:</strong> <code style="color:#e5c07b;">predict N<sub>2</sub> + O<sub>2</sub>;</code></p>

        <h3 style="color:#98c379;">analyze</h3>
        <p>Analyzes properties of elements or compounds</p>
        <p><strong>Example:</strong> <code style="color:#e5c07b;">analyze H<sub>2</sub>O;</code></p>

        <h3 style="color:#98c379;">balance</h3>
        <p>Balances chemical equations</p>
        <p><strong>Example:</strong> <code style="color:#e5c07b;">balance CH<sub>4</sub> + O<sub>2</sub> → CO<sub>2</sub> + H<sub>2</sub>O;</code></p>

        <h2 style="color:#c678dd;">Working Examples</h2>
        <p>Try these examples in the editor:</p>
        <ol>
            <li><strong>Water analysis:</strong><br>
                <code style="color:#e5c07b;">analyze H<sub>2</sub>O;</code></li>
            <li><strong>Balancing combustion:</strong><br>
                <code style="color:#e5c07b;">balance C<sub>2</sub>H<sub>6</sub> + O<sub>2</sub> → CO<sub>2</sub> + H<sub>2</sub>O;</code></li>
            <li><strong>Predict common reaction:</strong><br>
                <code style="color:#e5c07b;">predict Na + Cl<sub>2</sub>;</code></li>
            <li><strong>Analyze an element:</strong><br>
                <code style="color:#e5c07b;">analyze Fe;</code></li>
        </ol>

        <h2 style="color:#c678dd;">Interface Tips</h2>
        <ul>
            <li>Use the toolbar buttons to insert command templates</li>
            <li>Press F5 or click Run to execute your code</li>
            <li>Results appear in the right panel</li>
            <li>Execution steps show the parsing and evaluation process</li>
            <li>Use Clear button to reset all content</li>
        </ul>
        """

        help_text.setHtml(help_content)
        scroll_area.setWidget(help_text)
        layout.addWidget(scroll_area, 1)

        # Close button
        close_button = QPushButton("Close")
        close_button.setFont(QFont("Segoe UI", 11))
        close_button.setMinimumHeight(40)
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #2c5a9c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #326bbf;
            }
            QPushButton:pressed {
                background-color: #214283;
            }
        """)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)


class CreditsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ChemDSL Credits")
        self.resize(600, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1b1e;
                color: #d8d8d8;
            }
        """)
        self.setup_ui()

        if parent:
            parent.destroyed.connect(self.close)

    def setup_ui(self):
        try:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(30, 30, 30, 30)
            layout.setSpacing(20)

            # Title
            title_label = QLabel("ChemDSL Credits")
            title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
            title_label.setStyleSheet("color: #61afef;")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title_label)

            # Credit sections
            credits_text = QTextEdit()
            credits_text.setReadOnly(True)
            credits_text.setStyleSheet("""
                QTextEdit {
                    background-color: #1e1f22;
                    color: #d8d8d8;
                    border: none;
                    border-radius: 6px;
                    padding: 15px;
                }
            """)

            html_content = """
            <div style="text-align: center; margin-bottom: 20px;">
                <span style="font-size: 16px; color: #e5c07b; font-weight: bold;">Technical University of Moldova, FAF-231</span>
            </div>

            <div style="margin-bottom: 20px;">
                <p style="font-size: 14px; color: #c678dd; font-weight: bold;">Project Team:</p>
                <ul style="list-style-type: none; padding-left: 20px;">
                    <li style="margin-bottom: 8px; color: #98c379;">• Clima Marin</li>
                    <li style="margin-bottom: 8px; color: #98c379;">• Magla Alexandru</li>
                    <li style="margin-bottom: 8px; color: #98c379;">• Siminiuc Catalina</li>
                    <li style="margin-bottom: 8px; color: #98c379;">• Condrea Loredana</li>
                </ul>
            </div>

            <div style="margin-bottom: 20px;">
                <p style="font-size: 14px; color: #c678dd; font-weight: bold;">Special Thanks:</p>
                <p style="padding-left: 20px; color: #98c379;">• Cojuhari Elena</p>
                <p style="padding-left: 20px; color: #98c379;">• All the mentors who supported this project</p>
            </div>

            <div style="margin-top: 30px; text-align: center;">
                <p style="color: #56b6c2;">© 2025 ChemDSL Project</p>
            </div>
            """

            credits_text.setHtml(html_content)
            layout.addWidget(credits_text, 1)

            # Close button
            close_button = QPushButton("Close")
            close_button.setFont(QFont("Segoe UI", 11))
            close_button.setMinimumHeight(40)
            close_button.setCursor(Qt.CursorShape.PointingHandCursor)
            close_button.setStyleSheet("""
                QPushButton {
                    background-color: #2c5a9c;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 6px 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #326bbf;
                }
                QPushButton:pressed {
                    background-color: #214283;
                }
            """)
            close_button.clicked.connect(self.close)
            layout.addWidget(close_button)

        except Exception as e:
            print(f"Error setting up credits window: {e}")
            raise


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChemDSL")
        self.resize(800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1b1e;
                color: #d8d8d8;
            }
        """)
        self.setup_ui()
        self.chemdsl_window = None
        self.help_window = None
        self.credits_window = None

    def setup_ui(self):
        try:
            # Central widget
            central_widget = QWidget()
            self.setCentralWidget(central_widget)

            # Main layout
            layout = QVBoxLayout(central_widget)
            layout.setContentsMargins(50, 50, 50, 50)
            layout.setSpacing(20)

            # Title
            title_label = QLabel("ChemDSL")
            title_label.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
            title_label.setStyleSheet("color: #61afef;")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title_label)

            # Subtitle
            subtitle_label = QLabel("Chemical Domain Specific Language")
            subtitle_label.setFont(QFont("Segoe UI", 16))
            subtitle_label.setStyleSheet("color: #98c379;")
            subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(subtitle_label)

            # Add some spacing
            layout.addSpacing(50)

            # Buttons layout
            buttons_layout = QVBoxLayout()
            buttons_layout.setSpacing(20)

            # Menu buttons
            buttons = [
                {"text": "Start ChemDSL", "action": self.open_chemdsl},
                {"text": "Help", "action": self.open_help},
                {"text": "Credits", "action": self.open_credits},
                {"text": "Exit", "action": self.close}
            ]

            for button_info in buttons:
                button = QPushButton(button_info["text"])
                button.setFont(QFont("Segoe UI", 14))
                button.setMinimumHeight(60)
                button.setCursor(Qt.CursorShape.PointingHandCursor)

                # Special styling for Start button
                if button_info["text"] == "Start ChemDSL":
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #2c5a9c;
                            color: white;
                            border: none;
                            border-radius: 8px;
                            padding: 10px 20px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #326bbf;
                        }
                        QPushButton:pressed {
                            background-color: #214283;
                        }
                    """)
                elif button_info["text"] == "Exit":
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #3c2d2e;
                            color: #e06c75;
                            border: none;
                            border-radius: 8px;
                            padding: 10px 20px;
                        }
                        QPushButton:hover {
                            background-color: #4d3a3c;
                        }
                        QPushButton:pressed {
                            background-color: #5c4a4c;
                        }
                    """)
                else:
                    button.setStyleSheet("""
                        QPushButton {
                            background-color: #2b2d30;
                            color: #d8d8d8;
                            border: none;
                            border-radius: 8px;
                            padding: 10px 20px;
                        }
                        QPushButton:hover {
                            background-color: #3c3f41;
                        }
                        QPushButton:pressed {
                            background-color: #4d4d4f;
                        }
                    """)

                button.clicked.connect(button_info["action"])
                buttons_layout.addWidget(button)

            layout.addLayout(buttons_layout)
            layout.addStretch(1)

            # Version info
            version_label = QLabel("v1.0.0")
            version_label.setFont(QFont("Segoe UI", 9))
            version_label.setStyleSheet("color: #4b5263;")
            version_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            layout.addWidget(version_label)

        except Exception as e:
            print(f"Error setting up main menu: {e}")
            raise

    def open_chemdsl(self):
        try:
            if self.chemdsl_window is None or not self.chemdsl_window.isVisible():
                self.chemdsl_window = ChemDSL_GUI()
                self.chemdsl_window.show()
                self.close()  # Close the main menu window
        except Exception as e:
            print(f"Error opening ChemDSL window: {e}")

    def open_help(self):
        try:
            if self.help_window is None or not self.help_window.isVisible():
                self.help_window = HelpWindow(self)
                self.help_window.finished.connect(lambda: setattr(self, 'help_window', None))
                self.help_window.show()
        except Exception as e:
            print(f"Error opening help window: {e}")

    def open_credits(self):
        try:
            if self.credits_window is None or not self.credits_window.isVisible():
                self.credits_window = CreditsWindow(self)
                self.credits_window.finished.connect(lambda: setattr(self, 'credits_window', None))
                self.credits_window.show()
        except Exception as e:
            print(f"Error opening credits window: {e}")


def main():
    try:
        app = QApplication(sys.argv)

        # Set application styles
        app.setStyle('Fusion')

        # Create and show main menu
        main_menu = MainMenu()
        main_menu.show()

        sys.exit(app.exec())
    except Exception as e:
        print(f"Application error: {e}")
        return 1


if __name__ == "__main__":
    main()
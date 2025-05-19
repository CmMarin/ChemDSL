# gui_interface.py
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
                             QTextEdit, QTabWidget, QToolBar, QStatusBar, QLabel, QPushButton,
                             QFrame, QApplication)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QTextCursor, QColor, QTextCharFormat, QSyntaxHighlighter, QTextDocument
from DSL.parser import parse
from DSL.interpreter.evaluator_dsl import Evaluator
from DSL.lexer import tokenize
import io
import sys
import re


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        # Keyword formatting - using a more vibrant blue
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#61afef"))  # Brighter blue
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = ["predict", "balance", "analyze"]
        for word in keywords:
            pattern = r"\b{}\b".format(word)
            self.highlighting_rules.append((re.compile(pattern), keyword_format))

        # Comment formatting - using a softer green
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#98c379"))  # Softer green
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((re.compile(r"/\*.*?\*/", re.DOTALL), comment_format))

        # String formatting
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#e5c07b"))  # Amber color for strings
        self.highlighting_rules.append((re.compile(r'".*?"'), string_format))
        self.highlighting_rules.append((re.compile(r"'.*?'"), string_format))

        # Chemical element formatting
        element_format = QTextCharFormat()
        element_format.setForeground(QColor("#c678dd"))  # Purple for chemical elements
        elements = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al",
                    "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Fe", "Cu", "Zn", "Ag", "Au", "Hg", "Pb"]
        for element in elements:
            pattern = r"\b{}\d*\b".format(element)
            self.highlighting_rules.append((re.compile(pattern), element_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, format)


class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Segoe UI", 10))
        self.setMinimumHeight(32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Style for a modern flat button with hover effects
        self.setStyleSheet("""
            QPushButton {
                background-color: #2b2d30;
                color: #d8d8d8;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #3c3f41;
            }
            QPushButton:pressed {
                background-color: #4d78cc;
            }
        """)


class ChemDSL_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChemDSL IDE")
        self.resize(1300, 850)
        # Set the dark background color for the entire application
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1b1e;
                color: #d8d8d8;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        # Main central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout with some spacing
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # Splitter for left and right panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(2)  # Thinner handle
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #383a3e;
            }
            QSplitter::handle:hover {
                background-color: #4d78cc;
            }
        """)
        main_layout.addWidget(splitter)

        # Left panel (Editor)
        left_panel = QWidget()
        left_panel.setObjectName("leftPanel")
        left_panel.setStyleSheet("""
            #leftPanel {
                background-color: #1e1f22;
                border-radius: 6px;
            }
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(8, 8, 8, 8)
        left_layout.setSpacing(8)

        # Toolbar frame with rounded corners
        toolbar_frame = QFrame()
        toolbar_frame.setStyleSheet("""
            QFrame {
                background-color: #2b2d30;
                border-radius: 4px;
            }
        """)
        toolbar_layout = QHBoxLayout(toolbar_frame)
        toolbar_layout.setContentsMargins(8, 4, 8, 4)
        toolbar_layout.setSpacing(6)
        self.setup_toolbar(toolbar_layout)
        left_layout.addWidget(toolbar_frame)

        # Editor with enhanced styling
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Cascadia Code", 12))  # Modern coding font
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #d8d8d8;
                border: none;
                border-radius: 4px;
                selection-background-color: #214283;
                padding: 8px;
            }
        """)
        self.editor.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)  # No text wrapping
        self.editor.setPlaceholderText(
            "/* ChemDSL Quick Guide */\n\n"
            "1. Use toolbar buttons to insert commands\n"
            "2. Press F5 or Run button to execute\n"
            "3. View results in right panels\n\n"
            "Examples:\n"
            "predict N2 + O2;\n"
            "analyze H2O;\n"
            "balance CH4 + O2 -> CO2 + H2O;"
        )

        # Setup syntax highlighter
        self.highlighter = SyntaxHighlighter(self.editor.document())
        left_layout.addWidget(self.editor)

        # Right panel (Visualization)
        right_panel = QTabWidget()
        right_panel.setDocumentMode(True)  # Modern tab style
        right_panel.setTabPosition(QTabWidget.TabPosition.North)
        right_panel.setStyleSheet("""
            QTabWidget {
                background-color: #1e1f22;
                border-radius: 6px;
            }
            QTabWidget::pane {
                border: none;
                background-color: #1e1f22;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #2b2d30;
                color: #a9a9a9;
                border: none;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3c3f41;
                color: #d8d8d8;
            }
            QTabBar::tab:hover:!selected {
                background-color: #323437;
            }
        """)

        # Results tab
        self.visualizer = QTextEdit()
        self.visualizer.setFont(QFont("Segoe UI", 11))
        self.visualizer.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #d8d8d8;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        self.visualizer.setReadOnly(True)
        right_panel.addTab(self.visualizer, "Analysis Results")

        # Steps tab
        self.steps_text = QTextEdit()
        self.steps_text.setFont(QFont("Cascadia Code", 10))
        self.steps_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #d8d8d8;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        self.steps_text.setReadOnly(True)
        right_panel.addTab(self.steps_text, "Execution Steps")

        # Back to Main Menu Button (at the bottom of left panel)
        back_button_frame = QFrame()
        back_button_frame.setStyleSheet("""
            QFrame {
                background-color: #2b2d30;
                border-radius: 4px;
            }
        """)
        back_button_layout = QHBoxLayout(back_button_frame)
        back_button_layout.setContentsMargins(8, 4, 8, 4)

        back_button = ModernButton("Back to Main Menu")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #3c2d2e;
                color: #d8d8d8;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4d3a3c;
            }
            QPushButton:pressed {
                background-color: #5c4a4c;
            }
        """)
        back_button.clicked.connect(self.back_to_main_menu)
        back_button_layout.addWidget(back_button)

        left_layout.addWidget(back_button_frame)

        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([600, 700])

        # Status bar with modern look
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #2b2d30;
                color: #a9a9a9;
                border-top: 1px solid #383a3e;
            }
        """)
        self.status_bar.showMessage("Ready")
        self.setStatusBar(self.status_bar)

        # Use a timer to delay syntax highlighting to prevent performance issues
        self.highlight_timer = QTimer()
        self.highlight_timer.setInterval(300)  # 300ms delay - slightly more responsive
        self.highlight_timer.setSingleShot(True)
        self.highlight_timer.timeout.connect(self.delayed_highlight)
        self.editor.textChanged.connect(self.highlight_timer.start)

    def back_to_main_menu(self):
        """Method to go back to the main menu"""
        self.hide()  # Hide the current window
        # Import here to avoid circular imports
        from main_menu import MainMenu
        self.main_menu = MainMenu()
        self.main_menu.show()

    def delayed_highlight(self):
        """Delayed syntax highlighting to prevent performance issues"""
        try:
            # Just let the QSyntaxHighlighter do its work automatically
            pass
        except Exception as e:
            print(f"Highlighting error: {e}")

    def setup_toolbar(self, layout):
        commands = [
            ("Predict", "predict {};"),
            ("Analyze", "analyze {};"),
            ("Balance", "balance {} -> {};"),
            ("Clear", self.clear_all)
        ]

        for text, cmd in commands:
            btn = ModernButton(text)
            if isinstance(cmd, str):
                btn.clicked.connect(lambda _, c=cmd: self.insert_template(c))
            else:
                btn.clicked.connect(cmd)
            layout.addWidget(btn)

        # Add some spacing
        layout.addStretch(1)

        # Special styling for Run button
        run_btn = ModernButton("Run (F5)")
        run_btn.setStyleSheet("""
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
        run_btn.clicked.connect(self.run_code)
        layout.addWidget(run_btn)

    def insert_template(self, template):
        try:
            cursor = self.editor.textCursor()
            cursor.insertText(template + "\n")
            self.editor.setTextCursor(cursor)
            self.status_bar.showMessage(f"Inserted template: {template}")
        except Exception as e:
            self.status_bar.showMessage(f"Error inserting template: {str(e)}")

    def clear_all(self):
        try:
            self.editor.clear()
            self.visualizer.clear()
            self.steps_text.clear()
            self.status_bar.showMessage("Cleared all content")
        except Exception as e:
            self.status_bar.showMessage(f"Error clearing: {str(e)}")

    def run_code(self):
        try:
            code = self.editor.toPlainText().strip()
            self.steps_text.clear()
            self.visualizer.clear()

            # Add a visual indicator that execution is happening
            self.visualizer.setStyleSheet("""
                QTextEdit {
                    background-color: #1a1a1a;
                    color: #d8d8d8;
                    border: none;
                    border-radius: 4px;
                    padding: 8px;
                    border-left: 2px solid #4d78cc;
                }
            """)

            # Redirect stdout to capture steps
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()

            try:
                self.status_bar.showMessage("Executing...")

                # Show lexer tokens with colored formatting
                self.steps_text.append("<span style='color: #61afef; font-weight: bold;'>=== LEXER TOKENS ===</span>")
                tokens = tokenize(code)
                for token in tokens:
                    self.steps_text.append(
                        f"<span style='color: #98c379;'>Type:</span> <span style='color: #e5c07b;'>{token['type']:15}</span> <span style='color: #98c379;'>Value:</span> <span style='color: #c678dd;'>{token['value']}</span>")

                # Parse code
                self.steps_text.append(
                    "<br><span style='color: #61afef; font-weight: bold;'>=== PARSER OUTPUT ===</span>")
                ast = parse(code)
                self.steps_text.append(f"<span style='color: #56b6c2;'>{str(ast)}</span>")

                # Evaluate code
                self.steps_text.append(
                    "<br><span style='color: #61afef; font-weight: bold;'>=== EVALUATION STEPS ===</span>")
                evaluator = Evaluator()
                result = evaluator.evaluate(ast)

                # Add diagnostics
                self.steps_text.append(f"<br>Result type: <span style='color: #e5c07b;'>{type(result)}</span>")

                # Check if result is a dictionary with our marker
                if isinstance(result, dict) and result.get('is_analysis_result', False):
                    self.steps_text.append("Processing analysis result...")
                    self._format_analysis_result(result)
                elif isinstance(result, str) and '{' in result and '}' in result:
                    self.steps_text.append("Trying to parse dictionary string...")
                    try:
                        import ast as python_ast
                        dict_result = python_ast.literal_eval(result)
                        if isinstance(dict_result, dict) and dict_result.get('is_analysis_result', False):
                            self.steps_text.append("Successfully parsed as analysis result dictionary.")
                            self._format_analysis_result(dict_result)
                        else:
                            self.steps_text.append("String could not be parsed as an analysis result.")
                            self.visualizer.setPlainText(result)
                    except:
                        self.steps_text.append("Failed to parse as dictionary.")
                        self.visualizer.setPlainText(result)
                else:
                    self.steps_text.append("Not an analysis result, displaying as is.")
                    self.visualizer.setPlainText(str(result))

            except Exception as e:
                self.steps_text.append(f"\n<span style='color: #e06c75; font-weight: bold;'>ERROR:</span> {str(e)}")
                self.status_bar.showMessage(f"Error: {str(e)}")
                # Reset the visualizer border to normal
                self.visualizer.setStyleSheet("""
                    QTextEdit {
                        background-color: #1a1a1a;
                        color: #d8d8d8;
                        border: none;
                        border-radius: 4px;
                        padding: 8px;
                        border-left: 2px solid #e06c75;
                    }
                """)
            finally:
                captured_output = sys.stdout.getvalue()
                sys.stdout = old_stdout
                self.steps_text.append(captured_output)
                self.status_bar.showMessage("Execution completed")

                # After a successful execution, reset the visualizer style
                QTimer.singleShot(500, lambda: self.visualizer.setStyleSheet("""
                    QTextEdit {
                        background-color: #1a1a1a;
                        color: #d8d8d8;
                        border: none;
                        border-radius: 4px;
                        padding: 8px;
                    }
                """))

        except Exception as e:
            self.status_bar.showMessage(f"Unexpected error: {str(e)}")
            self.steps_text.append(f"<span style='color: #e06c75; font-weight: bold;'>Fatal error:</span> {str(e)}")

    def _format_analysis_result(self, analysis):
        try:
            # Use HTML formatting for better visual presentation
            if 'element' in analysis:
                self.visualizer.append(
                    "<div style='font-size: 16px; color: #61afef; margin-bottom: 10px; font-weight: bold;'>=== Element Analysis ===</div>")
                self.visualizer.append(
                    f"<div style='margin-left: 10px;'><b>Symbol:</b> <span style='color: #e5c07b;'>{analysis['element']}</span></div>")
                self.visualizer.append(
                    f"<div style='margin-left: 10px;'><b>Name:</b> <span style='color: #d8d8d8;'>{analysis['name']}</span></div>")
                self.visualizer.append(
                    f"<div style='margin-left: 10px;'><b>Atomic Weight:</b> <span style='color: #56b6c2;'>{analysis['atomic_weight']}</span></div>")
                self.visualizer.append(
                    f"<div style='margin-left: 10px;'><b>State at STP:</b> <span style='color: #d8d8d8;'>{analysis['state']}</span></div>")
                self.visualizer.append(
                    f"<div style='margin-left: 10px;'><b>Group:</b> <span style='color: #56b6c2;'>{analysis['group']}</span></div>")
                self.visualizer.append(
                    f"<div style='margin-left: 10px;'><b>Electronegativity:</b> <span style='color: #56b6c2;'>{analysis['electronegativity']}</span></div>")

                self.visualizer.append("<div style='margin-top: 15px; font-weight: bold;'>Common Compounds:</div>")
                for compound in analysis['common_compounds']:
                    self.visualizer.append(f"<div style='margin-left: 20px; color: #98c379;'>• {compound}</div>")

                self.visualizer.append("<div style='margin-top: 15px; font-weight: bold;'>Common Reactions:</div>")
                for reaction in analysis['common_reactions']:
                    self.visualizer.append(f"<div style='margin-left: 20px; color: #98c379;'>• {reaction}</div>")

            elif 'compound' in analysis:
                self.visualizer.append(
                    "<div style='font-size: 16px; color: #61afef; margin-bottom: 10px; font-weight: bold;'>=== Compound Analysis ===</div>")
                self.visualizer.append(
                    f"<div style='margin-left: 10px;'><b>Formula:</b> <span style='color: #e5c07b;'>{analysis['compound']}</span></div>")

                if 'name' in analysis:
                    self.visualizer.append(
                        f"<div style='margin-left: 10px;'><b>Name:</b> <span style='color: #d8d8d8;'>{analysis['name']}</span></div>")

                self.visualizer.append(
                    f"<div style='margin-left: 10px;'><b>Molar Mass:</b> <span style='color: #56b6c2;'>{analysis['molar_mass']:.2f} g/mol</span></div>")

                if 'state' in analysis:
                    self.visualizer.append(
                        f"<div style='margin-left: 10px;'><b>State at STP:</b> <span style='color: #d8d8d8;'>{analysis['state']}</span></div>")

                if 'classification' in analysis:
                    self.visualizer.append(
                        f"<div style='margin-left: 10px;'><b>Classification:</b> <span style='color: #d8d8d8;'>{analysis['classification']}</span></div>")

                self.visualizer.append("<div style='margin-top: 15px; font-weight: bold;'>Composition:</div>")
                for element, count in analysis['composition'].items():
                    self.visualizer.append(
                        f"<div style='margin-left: 20px;'><span style='color: #c678dd;'>{element}</span>: <span style='color: #56b6c2;'>{count}</span></div>")

                if analysis.get('detail_level') == 'all':
                    self.visualizer.append(
                        "<div style='margin-top: 15px; font-weight: bold;'>Physical Properties:</div>")
                    if 'density' in analysis:
                        self.visualizer.append(
                            f"<div style='margin-left: 20px;'><b>Density:</b> <span style='color: #56b6c2;'>{analysis['density']}</span></div>")
                    if 'melting_point' in analysis:
                        self.visualizer.append(
                            f"<div style='margin-left: 20px;'><b>Melting Point:</b> <span style='color: #56b6c2;'>{analysis['melting_point']} °C</span></div>")
                    if 'boiling_point' in analysis:
                        self.visualizer.append(
                            f"<div style='margin-left: 20px;'><b>Boiling Point:</b> <span style='color: #56b6c2;'>{analysis['boiling_point']} °C</span></div>")
                    if 'solubility' in analysis:
                        self.visualizer.append(
                            f"<div style='margin-left: 20px;'><b>Solubility:</b> <span style='color: #d8d8d8;'>{analysis['solubility']}</span></div>")
                    if 'acidity' in analysis:
                        self.visualizer.append(
                            f"<div style='margin-left: 20px;'><b>Acidity:</b> <span style='color: #d8d8d8;'>{analysis['acidity']}</span></div>")

                    if 'common_uses' in analysis:
                        self.visualizer.append("<div style='margin-top: 15px; font-weight: bold;'>Common Uses:</div>")
                        for use in analysis['common_uses']:
                            self.visualizer.append(f"<div style='margin-left: 20px; color: #98c379;'>• {use}</div>")

                    if 'hazards' in analysis:
                        self.visualizer.append(
                            "<div style='margin-top: 15px; font-weight: bold; color: #e06c75;'>Hazards:</div>")
                        for hazard in analysis['hazards']:
                            self.visualizer.append(f"<div style='margin-left: 20px; color: #e06c75;'>• {hazard}</div>")

            else:
                self.visualizer.append(
                    "<div style='font-size: 16px; color: #61afef; margin-bottom: 10px; font-weight: bold;'>=== Analysis Results ===</div>")
                for key, value in analysis.items():
                    if isinstance(value, dict):
                        self.visualizer.append(
                            f"<div style='margin-top: 15px; font-weight: bold;'>{key.title()}:</div>")
                        for sub_key, sub_value in value.items():
                            self.visualizer.append(
                                f"<div style='margin-left: 20px;'><b>{sub_key}:</b> <span style='color: #d8d8d8;'>{sub_value}</span></div>")
                    elif isinstance(value, list):
                        self.visualizer.append(
                            f"<div style='margin-top: 15px; font-weight: bold;'>{key.title()}:</div>")
                        for item in value:
                            self.visualizer.append(f"<div style='margin-left: 20px; color: #98c379;'>• {item}</div>")
                    else:
                        self.visualizer.append(
                            f"<div style='margin-left: 10px;'><b>{key.title()}:</b> <span style='color: #d8d8d8;'>{value}</span></div>")

            if 'detail_level' in analysis:
                self.visualizer.append(
                    f"<div style='margin-top: 15px; color: #a9a9a9; font-style: italic;'>Detail Level: {analysis['detail_level']}</div>")

        except Exception as e:
            self.visualizer.append(f"<div style='color: #e06c75;'>Error formatting results: {str(e)}</div>")
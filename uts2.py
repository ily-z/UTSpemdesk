# code_2_styled.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QGridLayout, QPushButton, QLineEdit, QMessageBox,
    QVBoxLayout, QHBoxLayout, QLabel, QTextEdit
)
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtCore import Qt


# =============================
# STYLE GLOBAL (dari code 1.py)
# =============================
LINEEDIT_STYLE = """
QLineEdit {
    background: #ffffff;
    color: #000000;
    border: 2px solid #888;
    border-radius: 7px;
    padding: 6px;
}
"""
LINEEDIT_SMALL_STYLE = """
QLineEdit {
    background: #fafafa;
    color: #444;
    border: 1px solid #bbb;
    border-radius: 4px;
    padding: 3px 5px;
}
"""
TEXTEDIT_STYLE = """
QTextEdit {
    background: #fefefe;
    border: 1px solid #ddd;
    border-radius: 4px;
    color: #333;
}
"""
BTN_STYLE = """
QPushButton {
    background: #ffffff;
    border: 2px solid #ccc;
    border-radius: 7px;
}
QPushButton:hover {
    background: #f0f0f0;
}
"""
BTN_OP = "background:#2196F3; color:white; border-radius:7px;"
BTN_EQ = "background:#4CAF50; color:white; border-radius:7px;"
BTN_CLR = "background:#f44336; color:white; border-radius:7px;"
BTN_INFO = "background:#ff9800; color:white; border-radius:7px;"
BTN_BK = "background:#9c27b0; color:white; border-radius:7px;"


# =============================
# MAIN CLASS
# =============================
class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator PyQt6 (Styled)")
        self.setGeometry(400, 200, 300, 400)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tabs
        self.grid_tab = QWidget()
        self.combo_tab = QWidget()
        self.group_tab = QWidget()

        self.tabs.addTab(self.grid_tab, "Grid Layout")
        self.tabs.addTab(self.combo_tab, "Kombinasi Layout")
        self.tabs.addTab(self.group_tab, "Nama Kelompok")

        # Setup tiap tab
        self.setup_grid_tab()
        self.setup_combo_tab()
        self.setup_group_tab()

        # Menu
        self.create_menu()

    # =============================
    # TAB 1: GRID LAYOUT
    # =============================
    def setup_grid_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(7, 7, 7, 7)
        layout.setSpacing(7)

        # LineEdit kecil (jejak)
        self.history_display = QLineEdit()
        self.history_display.setReadOnly(True)
        self.history_display.setFixedHeight(23)
        self.history_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.history_display.setFont(QFont("Arial", 10))
        self.history_display.setStyleSheet(LINEEDIT_SMALL_STYLE)
        layout.addWidget(self.history_display)

        # Display utama
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.display.setReadOnly(True)
        self.display.setFixedHeight(47)
        self.display.setStyleSheet(LINEEDIT_STYLE)
        layout.addWidget(self.display)

        # Log riwayat
        self.history_log = QTextEdit()
        self.history_log.setReadOnly(True)
        self.history_log.setFixedHeight(80)
        self.history_log.setStyleSheet(TEXTEDIT_STYLE)
        layout.addWidget(self.history_log)

        # Grid tombol angka dan operator
        grid = QGridLayout()
        grid.setSpacing(7)

        # Tombol angka sesuai code 1 (0–8)
        numbers = [
            ('7', 0, 0), ('8', 0, 1),
            ('5', 1, 0), ('6', 1, 1),
            ('2', 2, 0), ('4', 2, 1),
            ('0', 3, 0), ('1', 3, 1),
        ]
        for text, row, col in numbers:
            btn = QPushButton(text)
            btn.setFixedSize(53, 40)
            btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            btn.setStyleSheet(BTN_STYLE)
            btn.clicked.connect(lambda checked, t=text: self.add_to_display(t))
            grid.addWidget(btn, row, col)

        # Operator
        operators = [
            ('+', 0, 2), ('-', 1, 2),
            ('*', 2, 2), ('/', 3, 2),
            ('=', 4, 2)
        ]
        for text, row, col in operators:
            btn = QPushButton(text)
            btn.setFixedSize(53, 40)
            btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            if text == "=":
                btn.setStyleSheet(BTN_EQ)
                btn.clicked.connect(self.calculate)
            else:
                btn.setStyleSheet(BTN_OP)
                btn.clicked.connect(lambda checked, t=text: self.add_to_display(t))
            grid.addWidget(btn, row, col)

        layout.addLayout(grid)

        # Tombol bawah (Info, Clear, Backspace)
        hbox = QHBoxLayout()
        btn_info = QPushButton("Info")
        btn_info.setStyleSheet(BTN_INFO)
        btn_info.clicked.connect(self.show_info)
        btn_clear = QPushButton("Clear")
        btn_clear.setStyleSheet(BTN_CLR)
        btn_clear.clicked.connect(self.clear_all)
        btn_back = QPushButton("⌫")
        btn_back.setStyleSheet(BTN_BK)
        btn_back.clicked.connect(self.backspace)

        for b in [btn_info, btn_clear, btn_back]:
            b.setFixedHeight(33)
            hbox.addWidget(b)

        layout.addLayout(hbox)
        self.grid_tab.setLayout(layout)

    # =============================
    # TAB 2: KOMBINASI LAYOUT
    # =============================
    def setup_combo_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(7, 7, 7, 7)
        layout.setSpacing(7)

        self.display_combo = QLineEdit()
        self.display_combo.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display_combo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.display_combo.setStyleSheet(LINEEDIT_STYLE)
        self.display_combo.setReadOnly(True)
        layout.addWidget(self.display_combo)

        # Kombinasi tombol vertikal dan horizontal
        grid = QGridLayout()
        grid.setSpacing(7)

        buttons = [
            ('7', 0, 0), ('8', 0, 1),
            ('5', 1, 0), ('6', 1, 1),
            ('2', 2, 0), ('4', 2, 1),
            ('0', 3, 0), ('1', 3, 1),
            ('+', 0, 2), ('-', 1, 2),
            ('*', 2, 2), ('/', 3, 2),
            ('=', 4, 2)
        ]
        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.setFixedSize(53, 40)
            btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            if text == "=":
                btn.setStyleSheet(BTN_EQ)
                btn.clicked.connect(self.calculate_combo)
            elif text in ['+', '-', '*', '/']:
                btn.setStyleSheet(BTN_OP)
                btn.clicked.connect(lambda checked, t=text: self.add_combo(t))
            else:
                btn.setStyleSheet(BTN_STYLE)
                btn.clicked.connect(lambda checked, t=text: self.add_combo(t))
            grid.addWidget(btn, row, col)

        layout.addLayout(grid)

        hbox = QHBoxLayout()
        btn_clear = QPushButton("Clear")
        btn_clear.setStyleSheet(BTN_CLR)
        btn_clear.setFixedHeight(33)
        btn_clear.clicked.connect(lambda: self.display_combo.clear())
        hbox.addWidget(btn_clear)

        layout.addLayout(hbox)
        self.combo_tab.setLayout(layout)

    # =============================
    # TAB 3: NAMA KELOMPOK
    # =============================
    def setup_group_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        title = QLabel("Daftar Anggota Kelompok")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        members = [
            "220411100108 Umar Muchtar Khaidzar",
            "220411100181 Muhammad Ilyas Zaini",
            "230411100102 Tria Desy Nurhaliza",
            "230411100156 Kamila Mulya Fadila",
            "230411100157 Aliya Zulfa Syafitri",
            "230411100184 Nadiatul Khoir"
        ]
        for m in members:
            lbl = QLabel(m)
            lbl.setFont(QFont("Arial", 11))
            lbl.setStyleSheet("color:#222; background:#fff; border:1px solid #eee; border-radius:6px; padding:4px;")
            layout.addWidget(lbl)

        layout.addStretch()
        self.group_tab.setLayout(layout)

    # =============================
    # MENU
    # =============================
    def create_menu(self):
        menu = self.menuBar()
        operasi = menu.addMenu("Operasi")

        for op, label in [('+', "Tambah (+)"), ('-', "Kurang (-)"),
                          ('*', "Kali (*)"), ('/', "Bagi (/)"), ('=', "Hitung (=)")]:
            action = QAction(label, self)
            if op == '=':
                action.triggered.connect(self.calculate)
            else:
                action.triggered.connect(lambda checked, t=op: self.add_to_display(t))
            operasi.addAction(action)

    # =============================
    # LOGIKA
    # =============================
    def add_to_display(self, text):
        self.display.setText(self.display.text() + text)
        self.history_display.setText(self.display.text())

    def calculate(self):
        try:
            expr = self.display.text()
            result = str(eval(expr))
            self.display.setText(result)
            self.history_log.append(f"{expr} = {result}")
        except Exception:
            self.display.setText("Error")

    def add_combo(self, text):
        self.display_combo.setText(self.display_combo.text() + text)

    def calculate_combo(self):
        try:
            expr = self.display_combo.text()
            result = str(eval(expr))
            self.display_combo.setText(result)
        except Exception:
            self.display_combo.setText("Error")

    def clear_all(self):
        self.display.clear()
        self.history_display.clear()
        self.history_log.clear()

    def backspace(self):
        current = self.display.text()
        self.display.setText(current[:-1])
        self.history_display.setText(self.display.text())

    def show_info(self):
        QMessageBox.information(
            self, "Info",
            "Kalkulator PyQt6\nDidesain mirip dengan gaya Code 1"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout, QPushButton, QLineEdit,
    QTabWidget, QTextEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QFont


# ================================ KALKULATOR ================================
class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(7, 7, 7, 7)
        main_layout.setSpacing(7)

        # --- Display atas (history singkat) ---
        self.history_display = QLineEdit()
        self.history_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.history_display.setReadOnly(True)
        self.history_display.setFixedHeight(23)
        self.history_display.setFont(QFont("Arial", 10))
        self.history_display.setStyleSheet("""
            QLineEdit {
                background: #fafafa;
                color: #444;
                border: 1px solid #bbb;
                border-radius: 4px;
                padding: 3px 5px;
            }
        """)
        main_layout.addWidget(self.history_display)

        # --- Display utama ---
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(47)
        self.display.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.display.setStyleSheet("""
            QLineEdit {
                background: #ffffff;
                color: #000000;
                border: 2px solid #888;
                border-radius: 7px;
                padding: 7px;
            }
        """)
        main_layout.addWidget(self.display)

        # --- Log history penuh ---
        self.history_log = QTextEdit()
        self.history_log.setReadOnly(True)
        self.history_log.setFixedHeight(80)
        self.history_log.setStyleSheet("""
            QTextEdit {
                background: #fefefe;
                border: 1px solid #ddd;
                border-radius: 4px;
                color: #333;
            }
        """)
        main_layout.addWidget(self.history_log)

        # --- Grid tombol angka ---
        grid = QGridLayout()
        grid.setSpacing(7)

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
            btn.setStyleSheet("""
                QPushButton {
                    background: #ffffff;
                    border: 2px solid #ccc;
                    border-radius: 7px;
                }
                QPushButton:hover {
                    background: #f0f0f0;
                }
            """)
            btn.clicked.connect(lambda _, t=text: self.add_to_display(t))
            grid.addWidget(btn, row, col)

        # --- Grid tombol operator ---
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
                btn.setStyleSheet("background:#4CAF50; color:white; border-radius:7px;")
            else:
                btn.setStyleSheet("background:#2196F3; color:white; border-radius:7px;")
            btn.clicked.connect(lambda _, t=text: self.handle_operator(t))
            grid.addWidget(btn, row, col)

        main_layout.addLayout(grid)

        # --- Tombol bawah (Backspace saja, tanpa Clear) ---
        hbox = QHBoxLayout()

        self.btn_back = QPushButton("⌫")
        self.btn_back.setStyleSheet("background:#9c27b0; color:white; border-radius:7px;")
        self.btn_back.setFixedHeight(33)

        # Timer untuk long press
        self.backspace_timer = QTimer()
        self.backspace_timer.setSingleShot(True)
        self.backspace_timer.timeout.connect(self.clear_all)

        self.btn_back.pressed.connect(self.start_backspace_timer)
        self.btn_back.released.connect(self.handle_backspace_release)

        hbox.addWidget(self.btn_back)
        main_layout.addLayout(hbox)

        self.setLayout(main_layout)

    # ================== FUNCTION ==================
    def add_to_display(self, text):
        self.display.setText(self.display.text() + text)
        self.history_display.setText(self.display.text())

    def handle_operator(self, op):
        if op == "=":
            try:
                expression = self.display.text()
                result = str(eval(expression))

                if self.history_log.toPlainText():
                    lines = self.history_log.toPlainText().split("\n")
                    last_line = lines[-1]
                    if "=" in last_line:
                        last_result = last_line.split("=")[-1].strip()
                        if not expression.startswith(last_result):
                            lines = lines[:-1]
                            self.history_log.setPlainText("\n".join(lines))

                self.history_display.setText(expression + " =")
                self.display.setText(result)
                self.history_log.append(f"{expression} = {result}")

            except Exception:
                self.display.setText("Error")
        else:
            self.display.setText(self.display.text() + op)
            self.history_display.setText(self.display.text())

    def clear_all(self):
        self.display.clear()
        self.history_display.clear()
        self.history_log.clear()

    def backspace_display(self):
        current_text = self.display.text()
        if current_text:
            new_text = current_text[:-1]
            self.display.setText(new_text)
            self.history_display.setText(new_text)

    def start_backspace_timer(self):
        # mulai timer (1 detik)
        self.backspace_timer.start(1000)

    def handle_backspace_release(self):
        if self.backspace_timer.isActive():
            # kalau dilepas sebelum 1 detik -> backspace
            self.backspace_timer.stop()
            self.backspace_display()
        # kalau ditahan >=1 detik -> clear_all otomatis


# ================================ TAB MAHASISWA ================================
class MahasiswaTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        daftar = (
            "220411100108 Umar Muchtar Khaidzar\n"
            "220411100181 Muhammad Ilyas Zaini\n"
            "230411100102 Tria Desy Nurhaliza\n"
            "230411100156 Kamila Mulya Fadila\n"
            "230411100157 Aliya Zulfa Syafitri\n"
            "230411100184 Nadiatul Khoir"
        )

        text_widget = QTextEdit()
        text_widget.setReadOnly(True)
        text_widget.setText(daftar)
        text_widget.setStyleSheet("""
            QTextEdit {
                background: #fdfdfd;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 8px;
                font-size: 11pt;
                font-family: Arial;
            }
        """)

        layout.addWidget(text_widget)
        self.setLayout(layout)


# ================================ MAIN WINDOW ================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator Desktop - PyQt6")
        self.setGeometry(300, 200, 300, 400)

        self.calculator = Calculator()
        self.mahasiswa_tab = MahasiswaTab()

        tabs = QTabWidget()
        tabs.addTab(self.calculator, "Kalkulator")
        tabs.addTab(self.mahasiswa_tab, "Mahasiswa")
        self.setCentralWidget(tabs)

        # Menu Bar
        menubar = self.menuBar()
        operasi_menu = menubar.addMenu("Operasi Matematika")

        tambah = QAction("Tambah (+)", self)
        kurang = QAction("Kurang (-)", self)
        kali = QAction("Kali (*)", self)
        bagi = QAction("Bagi (/)", self)
        sama_dengan = QAction("Samadengan (=)", self)

        tambah.triggered.connect(lambda: self.calculator.handle_operator("+"))
        kurang.triggered.connect(lambda: self.calculator.handle_operator("-"))
        kali.triggered.connect(lambda: self.calculator.handle_operator("*"))
        bagi.triggered.connect(lambda: self.calculator.handle_operator("/"))
        sama_dengan.triggered.connect(lambda: self.calculator.handle_operator("="))

        for action in [tambah, kurang, kali, bagi, sama_dengan]:
            operasi_menu.addAction(action)


# ================================ RUN APP ================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

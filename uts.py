import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout, QPushButton, QLineEdit,
    QTabWidget, QMessageBox, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Jejak perhitungan (atas)
        self.history_display = QLineEdit()
        self.history_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.history_display.setReadOnly(True)
        self.history_display.setFixedHeight(35)
        self.history_display.setFont(QFont("Arial", 12))
        self.history_display.setStyleSheet("""
            QLineEdit {
                background: #fafafa;
                color: #444;
                border: 1px solid #bbb;
                border-radius: 6px;
                padding: 4px 8px;
            }
        """)
        main_layout.addWidget(self.history_display)

        # Layar kalkulator utama (angka besar)
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(70)
        self.display.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.display.setStyleSheet("""
            QLineEdit {
                background: #ffffff;
                color: #000000;
                border: 2px solid #888;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        main_layout.addWidget(self.display)

        # Kotak riwayat lengkap
        self.history_log = QTextEdit()
        self.history_log.setReadOnly(True)
        self.history_log.setFixedHeight(120)
        self.history_log.setStyleSheet("""
            QTextEdit {
                background: #fefefe;
                border: 1px solid #ddd;
                border-radius: 6px;
                color: #333;
            }
        """)
        main_layout.addWidget(self.history_log)

        # Grid tombol angka & operator
        grid = QGridLayout()
        grid.setSpacing(10)

        numbers = [
            ('7', 0, 0), ('8', 0, 1),
            ('5', 1, 0), ('6', 1, 1),
            ('3', 2, 0), ('4', 2, 1),
            ('1', 3, 0), ('2', 3, 1),
            ('0', 4, 0, 1, 2)
        ]

        for item in numbers:
            if len(item) == 3:
                text, row, col = item
                rowspan, colspan = 1, 1
            else:
                text, row, col, rowspan, colspan = item

            btn = QPushButton(text)
            btn.setFixedSize(80, 60)
            btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background: #ffffff;
                    border: 2px solid #ccc;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background: #f0f0f0;
                }
            """)
            btn.clicked.connect(lambda checked, t=text: self.add_to_display(t))
            grid.addWidget(btn, row, col, rowspan, colspan)

        operators = [
            ('+', 0, 2), ('-', 1, 2),
            ('*', 2, 2), ('/', 3, 2),
            ('=', 4, 2)
        ]

        for text, row, col in operators:
            btn = QPushButton(text)
            btn.setFixedSize(80, 60)
            btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            if text == "=":
                btn.setStyleSheet("background:#4CAF50; color:white; border-radius:10px;")
            else:
                btn.setStyleSheet("background:#2196F3; color:white; border-radius:10px;")
            btn.clicked.connect(lambda checked, t=text: self.handle_operator(t))
            grid.addWidget(btn, row, col)

        main_layout.addLayout(grid)

        # Tombol tambahan (horizontal)
        hbox = QHBoxLayout()
        btn_info = QPushButton("Info")
        btn_info.setStyleSheet("background:#ff9800; color:white; border-radius:10px;")
        btn_info.setFixedHeight(50)
        btn_info.clicked.connect(self.show_info)

        btn_clear = QPushButton("Clear")
        btn_clear.setStyleSheet("background:#f44336; color:white; border-radius:10px;")
        btn_clear.setFixedHeight(50)
        btn_clear.clicked.connect(self.clear_all)

        btn_back = QPushButton("⌫")
        btn_back.setStyleSheet("background:#9c27b0; color:white; border-radius:10px;")
        btn_back.setFixedHeight(50)
        btn_back.clicked.connect(self.backspace_display)

        hbox.addWidget(btn_info)
        hbox.addWidget(btn_clear)
        hbox.addWidget(btn_back)
        main_layout.addLayout(hbox)

        self.setLayout(main_layout)

    def add_to_display(self, text):
        self.display.setText(self.display.text() + text)
        self.history_display.setText(self.display.text())

    def handle_operator(self, op):
        if op == "=":
            try:
                expression = self.display.text()
                result = str(eval(expression))

                # --- sinkronisasi riwayat ---
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

    def show_info(self):
        QMessageBox.information(
            self,
            "Info",
            "Kalkulator Desktop - Angka 0-8"
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator Desktop - PyQt6")
        self.setGeometry(300, 200, 350, 600)

        self.calculator = Calculator()
        tabs = QTabWidget()
        tabs.addTab(self.calculator, "Kalkulator")
        self.setCentralWidget(tabs)

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

        help_menu = menubar.addMenu("Help")
        about_action = QAction("Tentang", self)

        about_text = (
            "Aplikasi Kalkulator Desktop - PyQt6\n\n"
            "Dibuat oleh:\n"
            "- 220411100108 Umar Muchtar Khaidzar\n"
            "- 220411100181 Muhammad Ilyas Zaini\n"
            "- 230411100102 Tria Desy Nurhaliza\n"
            "- 230411100156 Kamila Mulya Fadila\n"
            "- 230411100157 Aliya Zulfa Syafitri\n"
            "- 230411100184 Nadiatul Khoir"
        )

        about_action.triggered.connect(
            lambda: QMessageBox.information(self, "Tentang", about_text)
        )
        help_menu.addAction(about_action)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

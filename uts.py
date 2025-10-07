import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout, QPushButton, QLineEdit,
    QTabWidget, QTextEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QFont


# ======================================================================
# Widget minimum → class CalculatorBase sebagai widget utama kalkulator
# ======================================================================
class CalculatorBase(QWidget):
    def __init__(self, styled=False):
        super().__init__()
        self.styled = styled
        self.initUI()

    def initUI(self):
        # ==============================================================
        # KOMBINASI LAYOUT
        # QVBoxLayout → Layout Vertikal utama (dari atas ke bawah)
        # ==============================================================
        main_layout = QVBoxLayout()

        # ==============================================================
        # LineEdit → Display Atas (History Singkat)
        # ==============================================================
        self.history_display = QLineEdit()
        self.history_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.history_display.setReadOnly(True)
        self.history_display.setFixedHeight(23)
        self.history_display.setFont(QFont("Arial", 10))

        if self.styled:
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

        # ==============================================================
        # LineEdit → Display Utama (Input/Output)
        # ==============================================================
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(47)
        self.display.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        if self.styled:
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

        # ==============================================================
        # Widget minimum tambahan → Log History Penuh
        # ==============================================================
        self.history_log = QTextEdit()
        self.history_log.setReadOnly(True)
        self.history_log.setFixedHeight(80)

        if self.styled:
            self.history_log.setStyleSheet("""
                QTextEdit {
                    background: #fefefe;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    color: #333;
                }
            """)
        main_layout.addWidget(self.history_log)

        # ==============================================================
        # Grid → Tombol Angka (Disusun dalam Grid Layout)
        # ==============================================================
        grid = QGridLayout()
        numbers = [
            ('7', 0, 0), ('8', 0, 1),
            ('5', 1, 0), ('6', 1, 1),
            ('2', 2, 0), ('4', 2, 1),
            ('0', 3, 0), ('1', 3, 1),
        ]

        for text, row, col in numbers:
            # Button angka
            btn = QPushButton(text)
            btn.setFixedSize(53, 40)
            btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))

            if self.styled:
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

        # ==============================================================
        # Grid → Tombol Operator
        # ==============================================================
        operators = [
            ('+', 0, 2), ('-', 1, 2),
            ('*', 2, 2), ('/', 3, 2),
            ('=', 4, 2)
        ]

        for text, row, col in operators:
            # Button operator
            btn = QPushButton(text)
            btn.setFixedSize(53, 40)
            btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))

            if self.styled:
                if text == "=":
                    btn.setStyleSheet("background:#4CAF50; color:white; border-radius:7px;")
                else:
                    btn.setStyleSheet("background:#2196F3; color:white; border-radius:7px;")

            btn.clicked.connect(lambda _, t=text: self.handle_operator(t))
            grid.addWidget(btn, row, col)

        main_layout.addLayout(grid)

        # ==============================================================
        # KOMBINASI LAYOUT
        # QHBoxLayout → Layout Horizontal (untuk tombol Backspace)
        # Ditaruh di dalam VBox (kombinasi vertikal + horizontal)
        # ==============================================================
        hbox = QHBoxLayout()
        self.btn_back = QPushButton("⌫")

        if self.styled:
            self.btn_back.setStyleSheet("background:#9c27b0; color:white; border-radius:7px;")

        self.btn_back.setFixedHeight(33)

        # Timer untuk long press (tekan lama = clear all)
        self.backspace_timer = QTimer()
        self.backspace_timer.setSingleShot(True)
        self.backspace_timer.timeout.connect(self.clear_all)

        self.btn_back.pressed.connect(self.start_backspace_timer)
        self.btn_back.released.connect(self.handle_backspace_release)

        hbox.addWidget(self.btn_back)          # Tombol Backspace horizontal
        main_layout.addLayout(hbox)            # HBox dimasukkan ke VBox utama

        # ==============================================================
        # Set Layout Utama (VBox)
        # ==============================================================
        self.setLayout(main_layout)

    # ==================================================================
    # Function
    # ==================================================================
    def add_to_display(self, text):
        """Menambahkan angka ke display"""
        self.display.setText(self.display.text() + text)
        self.history_display.setText(self.display.text())

    def handle_operator(self, op):
        """Operasi matematika"""
        if op == "=":
            try:
                expression = self.display.text()
                result = str(eval(expression))

                # Cegah duplikasi hasil di log
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
        """Menghapus semua isi display & history"""
        self.display.clear()
        self.history_display.clear()
        self.history_log.clear()

    def backspace_display(self):
        """Menghapus satu karakter terakhir"""
        current_text = self.display.text()
        if current_text:
            new_text = current_text[:-1]
            self.display.setText(new_text)
            self.history_display.setText(new_text)

    def start_backspace_timer(self):
        """Mulai hitung waktu untuk long press"""
        self.backspace_timer.start(1000)

    def handle_backspace_release(self):
        """Jika dilepas sebelum 1 detik → hapus 1 angka"""
        if self.backspace_timer.isActive():
            self.backspace_timer.stop()
            self.backspace_display()


# ======================================================================
# Tab Mahasiswa
# ======================================================================
class MahasiswaTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Daftar NIM dan Nama
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
        layout.addWidget(text_widget)
        self.setLayout(layout)


# ======================================================================
# Main Window dengan Tab dan Menu
# ======================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator Desktop - PyQt6")
        self.setGeometry(300, 200, 300, 400)

        # ==============================================================
        # Tab → ada 3 tab: Kalkulator, Kombinasi Layout, Mahasiswa
        # ==============================================================
        self.calculator_default = CalculatorBase(styled=False)   
        self.calculator_styled = CalculatorBase(styled=True)     
        self.mahasiswa_tab = MahasiswaTab()                      

        tabs = QTabWidget()
        tabs.addTab(self.calculator_default, "Kalkulator")
        tabs.addTab(self.calculator_styled, "Kombinasi LayOut")
        tabs.addTab(self.mahasiswa_tab, "Mahasiswa")
        self.setCentralWidget(tabs)

        # ==============================================================
        # Menu → Operasi Matematika
        # ==============================================================
        menubar = self.menuBar()
        operasi_menu = menubar.addMenu("Operasi Matematika")

        tambah = QAction("Tambah (+)", self)
        kurang = QAction("Kurang (-)", self)
        kali = QAction("Kali (*)", self)
        bagi = QAction("Bagi (/)", self)
        sama_dengan = QAction("Samadengan (=)", self)

        tambah.triggered.connect(lambda: self.calculator_default.handle_operator("+"))
        kurang.triggered.connect(lambda: self.calculator_default.handle_operator("-"))
        kali.triggered.connect(lambda: self.calculator_default.handle_operator("*"))
        bagi.triggered.connect(lambda: self.calculator_default.handle_operator("/"))
        sama_dengan.triggered.connect(lambda: self.calculator_default.handle_operator("="))

        for action in [tambah, kurang, kali, bagi, sama_dengan]:
            operasi_menu.addAction(action)


# ======================================================================
# Run Aplikasi
# ======================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

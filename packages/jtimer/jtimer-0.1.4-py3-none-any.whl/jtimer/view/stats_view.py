from enum import Enum
from PyQt6.QtWidgets import QVBoxLayout, QTableWidgetItem, QTableWidget, QWidget
from datetime import datetime, timedelta


class WeekDay(Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6


class StatsView(QWidget):
    def __init__(self, timers: dict):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.tableWidget = QTableWidget()
        layout.addWidget(self.tableWidget)

        self.tableWidget.setRowCount(len(timers.keys()) + 1)
        self.tableWidget.setColumnCount(8)
        self.setGeometry(1400, 1200, 8 * 105, ((len(timers.keys())) * 44) + 100)
        self.build_headers()
        row_counter = 1
        for key in timers.keys():
            self.add_timer(row_counter, key, timers[key])
            row_counter += 1

    def build_headers(self):
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Name"))
        now = datetime.now()
        column_index = 7
        for i in range(0, 7):
            title = WeekDay((now - timedelta(days=i)).weekday()).name
            self.tableWidget.setItem(0, column_index, QTableWidgetItem(title))
            column_index -= 1

    def add_timer(self, index: int, name: str, data):
        self.tableWidget.setItem(index, 0, QTableWidgetItem(name))
        for i in range(1, 8):
            self.tableWidget.setItem(index, i, QTableWidgetItem(data[i - 1]))

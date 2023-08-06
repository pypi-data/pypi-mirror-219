from PyQt6.QtWidgets import (
    QBoxLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QWidget,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

from jtimer.controller import ControllerInterface as Controller
from jtimer.view import ADD_ICON, CHART_ICON
from jtimer.view.timer_widget import TimerWidget
from jtimer.model.timer import Timer


class TimersView(QWidget):
    def __init__(self, controller: Controller):
        super().__init__()
        self.timer_widgets = {}
        self.controller = controller
        main_layout = QVBoxLayout()

        self.timer_list = QVBoxLayout()
        self.timer_list.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.timer_list.setSpacing(0)
        main_layout.addLayout(self.build_menu())
        main_layout.addLayout(self.timer_list)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(main_layout)
        self.refresh()

    def build_menu(self) -> QBoxLayout:
        menu = QHBoxLayout()
        menu.setAlignment(Qt.AlignmentFlag.AlignLeft)
        menu.setSpacing(2)
        menu.setContentsMargins(6, 3, 6, 3)

        add_button = QPushButton()
        add_button.setFixedSize(30, 30)
        add_button.setIcon(QIcon(ADD_ICON))
        add_button.clicked.connect(self.add_button_click)

        self.lineEdit = QLineEdit("⏱️")

        view_stats_button = QPushButton()
        view_stats_button.setIcon(QIcon(CHART_ICON))
        view_stats_button.setFixedSize(30, 30)
        view_stats_button.clicked.connect(self.controller.show_stats)

        menu.addWidget(add_button)
        menu.addWidget(self.lineEdit)
        menu.addWidget(view_stats_button)
        return menu

    def add_button_click(self):
        name = f"{self.lineEdit.text()}"
        self.controller.new_timer(name)

    def add_timer(self, new_timer: Timer):
        widget = TimerWidget(new_timer, self.controller)
        self.timer_list.addWidget(widget)
        self.timer_widgets[new_timer.name] = widget
        self.refresh()

    def delete_timer(self, timer: str):
        widget = self.timer_widgets[timer]
        self.timer_list.removeWidget(widget)
        self.timer_widgets.pop(timer, None)
        self.refresh()

    def refresh(self):
        self.resize(QSize(300, (len(self.timer_widgets.keys()) * 35)))

from tkinter import EventType
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QLineEdit, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer, Qt
from datetime import timedelta, datetime
from jtimer.model.time_event import TimeEvent, TimeEventType
from jtimer.model.timer import Timer
from jtimer.view import DELETE_ICON, PLAY_ICON, PAUSE_ICON
from jtimer.controller import ControllerInterface as Controller

DEFAULT_RESOLUTION_SECONDS = 1
DEFAULT_RESOLUTION_MS = DEFAULT_RESOLUTION_SECONDS * 1000


class NameLabel(QLineEdit):
    def __init__(self, name, controller: Controller):
        super().__init__(name)
        self.timer_name = name
        self.controller = controller

    def focusOutEvent(self, e):
        self.controller.update_timer(self.timer_name, self.text())


class TimerWidget(QWidget):
    def __init__(self, timer: Timer, controller: Controller):
        super().__init__()
        self.instance = timer
        self.controller = controller
        self.layout = QHBoxLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(6, 3, 6, 3)
        self.name_label = NameLabel(timer.name, self.controller)

        self.value_label = QLabel(str(timer.get_delta_str()))
        self.button = QPushButton()
        self.button.setIcon(QIcon(PLAY_ICON))
        self.resolution_ms = DEFAULT_RESOLUTION_MS
        self.resolution_delta = timedelta(seconds=DEFAULT_RESOLUTION_SECONDS)

        self.button.clicked.connect(self.on_button_clicked)

        delete_button = QPushButton()
        delete_button.setIcon(QIcon(DELETE_ICON))
        delete_button.clicked.connect(self.delete)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.button)
        self.layout.addWidget(delete_button)
        self.layout.addWidget(self.value_label)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.sleeper = QTimer(self)
        self.sleeper.timeout.connect(self.update_timer)
        if self.is_active():
            self.sleeper.start(self.resolution_ms)
            self.button.setIcon(QIcon(PAUSE_ICON))
        self.setLayout(self.layout)

    def on_button_clicked(self):
        event_time = datetime.now()
        if self.is_active():
            self.instance.state = 0
            self.sleeper.stop()
            self.button.setIcon(QIcon(PLAY_ICON))
            self.add_event(TimeEventType.STOP, event_time)
        else:
            self.instance.state = 1
            self.sleeper.start(self.resolution_ms)
            self.button.setIcon(QIcon(PAUSE_ICON))
            self.add_event(TimeEventType.START, event_time)

    def update_timer(self):
        self.instance.delta += self.resolution_delta
        self.value_label.setText(str(self.instance.get_delta_str()))

    def is_active(self):
        return self.instance.state

    def add_event(self, event_type: EventType, event_time: datetime):
        event = TimeEvent(event_type, event_time)
        self.instance.events.append(event)
        self.controller.add_event(self.instance.name, event)

    def delete(self):
        if self.is_active():
            self.on_button_clicked()
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        self.setParent(None)
        self.controller.delete_timer(self.instance.name)

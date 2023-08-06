import argparse
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from jtimer.controller.timer_controller import TimerController
from jtimer.dao import DAO


def create_path(file: str):
    path = Path(file)
    if not path.parent.exists():
        path.parent.mkdir()


def start():
    parser = argparse.ArgumentParser(
        prog="jtimer",
        description="John's Timer - desktop app for tracking time",
        epilog="Text at the bottom of help",
    )
    parser.add_argument(
        "-d",
        "--db",
        dest="db",
        default="/tmp/jtimer/jtimer.db",
        help="location of database (/tmp/jtimer/jtimer.db)",
    )
    args = parser.parse_args()
    App = QApplication([])

    create_path(args.db)
    controller = TimerController(DAO(args.db))
    App.exit(App.exec())


if __name__ == "__main__":
    start()

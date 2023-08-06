from datetime import date, datetime
import sqlite3
from importlib import resources
from jtimer.model.time_event import TimeEvent, TimeEventType
from jtimer.model.timer import Timer

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class DAO:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        conn = self.connect()
        if not conn.execute(
            "SELECT name FROM sqlite_master WHERE name = 'timer'"
        ).fetchone():
            with resources.open_text("resources", "schema.sql") as f:
                conn.executescript(f.read())
            conn.commit()
        conn.close()
        self.next_id = 0

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_name)

    def create_timer(self, name: str) -> Timer:
        conn = self.connect()
        id = self.next_id
        conn.execute(f"INSERT INTO timer VALUES (:id, :name)", {"id": id, "name": name})
        conn.commit()
        conn.close()
        self.next_id += 1
        return Timer(id, name, [])

    def update_timer(self, timer: Timer) -> Timer:
        conn = self.connect()
        conn.execute(
            f"UPDATE timer SET name = :name WHERE id = :id",
            {"name": timer.name, "id": timer.id},
        )
        conn.commit()
        conn.close()
        return timer

    def delete_timer(self, timer: Timer) -> int:
        conn = self.connect()
        conn.execute(f"DELETE FROM timer WHERE id = :id", {"id": timer.id})
        conn.execute(f"DELETE FROM time_event WHERE timer_id = :id", {"id": timer.id})
        conn.commit()
        conn.close()
        return 1

    def get_all_timer_names(self) -> list:
        conn = self.connect()
        results = conn.execute(f"SELECT distinct(name) from timer").fetchall()
        conn.close()
        return [result[0] for result in results]

    def get_all_timer_objects(self, reporting=False) -> list:
        conn = self.connect()
        objects = []
        results = conn.execute(f"SELECT id, name from timer").fetchall()
        conn.close()
        for result in results:
            id = result[0]
            name = result[1]
            events = []
            if reporting:
                events = self.get_all_events(id)
            else:
                events = self.get_all_events_for_today(id)
            timer = Timer(id, name, events)
            objects.append(timer)
        self.next_id = len(objects) - 1
        return objects

    def create_event(self, timer: Timer, event: TimeEvent) -> TimeEvent:
        conn = self.connect()
        conn.execute(
            f"INSERT INTO time_event VALUES (:timer_id, :type, :created)",
            {"timer_id": timer.id, "type": event.type.name, "created": event.created},
        )
        conn.commit()
        conn.close()
        return event

    def get_all_events_for_day(self, id: int, day: date) -> list:
        conn = self.connect()
        results = conn.execute(
            f"SELECT type, created from time_event where timer_id=:id AND DATE(created) == DATE(:day) ORDER BY created",
            {"id": id, "day": str(day)},
        ).fetchall()
        conn.close()
        # print("day", day, "events", results)
        return [
            TimeEvent(TimeEventType[event[0]], datetime.fromisoformat(event[1]))
            for event in results
        ]

    def get_all_events_for_today(self, id: int):
        return self.get_all_events_for_day(id, date.today())

    def get_all_events(self, id: int) -> list:
        conn = self.connect()
        results = conn.execute(
            f"SELECT type, created from time_event where timer_id=:id ORDER BY created",
            {"id": id},
        ).fetchall()
        conn.close()
        return [
            TimeEvent(TimeEventType[event[0]], datetime.fromisoformat(event[1]))
            for event in results
        ]

    def get_last_event(self, id: int) -> TimeEvent:
        conn = self.connect()
        event = conn.execute(
            f"SELECT type, MAX(created) from time_event where timer_id=:id", {"id": id}
        ).fetchone()
        conn.close()
        if event and event[0]:
            return TimeEvent(TimeEventType[event[0]], datetime.fromisoformat(event[1]))
        return None

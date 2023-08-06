from datetime import timedelta, date, datetime

from jtimer.model.time_event import TimeEvent, TimeEventType


def eod(day: date):
    return datetime.combine(day, datetime.max.time())


def sod(day: date):
    return datetime.combine(day, datetime.min.time())


def happened_on_day(event: TimeEvent, day: date) -> bool:
    return event.created > sod(day) and event.created < eod(day)


def sum_events(events: list) -> timedelta:
    total = timedelta()
    if events:
        last_event: TimeEvent = events[-1]
        for i, event in enumerate(events):
            if event.type == TimeEventType.STOP:
                start_event: TimeEvent = events[i - 1]
                if start_event.type == TimeEventType.START:
                    start_event_time = start_event.created
                    stop_event_time = event.created
                    delta = stop_event_time - start_event_time
                    total += delta
        if last_event.type == TimeEventType.START and happened_on_day(
            last_event, date.today()
        ):
            total += datetime.now() - last_event.created
    return total

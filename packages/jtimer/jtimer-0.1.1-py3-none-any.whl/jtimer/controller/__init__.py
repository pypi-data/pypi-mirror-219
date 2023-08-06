from jtimer.model.time_event import TimeEvent


class ControllerInterface:
    def new_timer(self, name: str):
        pass

    def update_timer(self, name: str, new_name: str):
        pass

    def delete_timer(self, name: str):
        pass

    def add_event(self, type: str, event: TimeEvent):
        pass

    def show_stats(self):
        pass

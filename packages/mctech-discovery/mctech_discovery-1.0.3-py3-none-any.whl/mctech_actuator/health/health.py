from typing import Any, Union


class Status:
    def __init__(self, code: int, description: str):
        self.code = code
        self.description = description

    def compareTo(self, s):
        if self == s:
            return 0

        if not s:
            return 1
        if self.code < s.code:
            return -1
        elif self.code < s.code:
            return 1
        return 0


Status.UP = 'UP'
Status.DOWN = 'DOWN'
Status.SARTING = 'STARTING'
Status.OUT_OF_SERVICE = 'OUT_OF_SERVICE'
Status.UNKNOWN = 'UNKNOWN'


class Health:
    def __init__(self, status: Status, details: dict):
        self.status = status
        self.details = dict(details) if details else {}

    def to_json(self):
        json = {
            'status': self.status.code,
            'description': self.status.description
        }

        for key, value in self.details.items():
            if 'to_json' in value:
                json[key] = value.to_json()
            else:
                json[key] = value
        return json

    @staticmethod
    def unknown(description: str):
        status = Status(Status.UNKNOWN, description)
        return HealthBuilder(status)

    @staticmethod
    def down(description: str):
        status = Status(Status.DOWN, description)
        return HealthBuilder(status)

    @staticmethod
    def up(description: str):
        status = Status(Status.UP, description)
        return HealthBuilder(status)

    @staticmethod
    def out_of_service(description: str):
        status = Status(Status.OUT_OF_SERVICE, description)
        return HealthBuilder(status)

    @staticmethod
    def status(code: str, description: str):
        _status = Status(code, description)
        return HealthBuilder(_status)


class HealthBuilder:
    def __init__(self, status: Union[str, Status], details):
        self.status(status)
        self._details = dict(details) if details else {}

    def status(self, status: Union[str, Status] = None):
        if status:
            if isinstance(status, Status):
                self._status = status
            else:
                self._status = Status(status)
        return self

    def down(self, message: str):
        self._status = Status(Status.DOWN, message)
        return self

    def add_detail(self, name: str, item: Any):
        self._details.set(name, item)
        return self

    def build(self):
        return Health(self._status, self._details)


Health.Builder = HealthBuilder

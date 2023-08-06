import abc


class Indicator:
    @property
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def health():
        pass

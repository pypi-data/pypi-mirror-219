# export
from .health import Health, Status, CompositeHealthIndicator, Indicator
from .actuator.actuator_router import create_actuator_route

from .health import manager


class DefaultIndicator(Indicator):

    @property
    def name(self):
        return 'application'

    def health(self):
        return Health.up().build()


manager.add_indicator(DefaultIndicator())

from .composite_health_indicator import CompositeHealthIndicator
from .health import Health


class HealthManager:
    def __init__(self):
        self._indicator = CompositeHealthIndicator()
        self._metrics = []

    def get_metrics(self):
        return self._metrics

    def add_metric(self, metric):
        self._metrics.append(metric)

    def get_health(self):
        return self._indicator.health()

    def add_indicator(self, indicator):
        holder = IndicatorHolder(indicator)
        self._indicator.add_indicator(indicator.name, holder)


class IndicatorHolder:
    def __init__(self, indicator):
        self.name = None
        self.indicator = indicator

    def health(self):
        try:
            h = self.indicator.health()
        except RuntimeError as e:
            h = Health.down(e.name + ':' + e.message).build()
        return h


manager = HealthManager()

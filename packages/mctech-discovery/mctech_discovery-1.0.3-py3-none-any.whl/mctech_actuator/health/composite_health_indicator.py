from typing import Dict, Any, List
from .health import Health, Status


class CompositeHealthIndicator:
    def __init__(self, indicators: Dict[str, Any] = None):
        self._indicators = dict(indicators) if indicators else {}
        self._healthAggregator = HealthAggregator()

    def add_indicator(self, name: str, indicator):
        self._indicators[name] = indicator

    def health(self) -> Health:
        healths: Dict[str, Health] = {}
        for key, value in self._indicators.items():
            healths.set(key, value.health())
        return self._healthAggregator.aggregate(healths)


statusOrder = ['DOWN', 'OUT_OF_SERVICE', 'UP', 'UNKNOWN']


def aggregate_status(candidates: List[Status]):
    # Only sort those status instances that we know about
    filteredCandidates: List[Status] = []
    for candidate in candidates:
        if next(
                filter(lambda code: candidate.code == code, statusOrder),
                None):
            filteredCandidates.append(candidate)

    # If no status is given return UNKNOWN
    if len(filteredCandidates) == 0:
        return Status.UNKNOWN

    if len(filteredCandidates) == 1:
        return filteredCandidates[0]

    # Sort given Status instances by configured order
    sorted(filteredCandidates, key=compare)
    return filteredCandidates[0]


def compare(s1, s2):
    i1 = statusOrder.index(s1.code)
    i2 = statusOrder.index(s2.code)
    if i1 < i2:
        return -1
    elif i1 > i2:
        return 1
    return s1.compareTo(s2)


def aggregate_details(healths: Dict[str, Health]) -> Dict[str, Any]:
    return dict(healths)


class HealthAggregator:
    def aggregate(healths: Dict[str, Health]) -> Health:
        statusCandidates = []
        for health in healths.values():
            statusCandidates.append(health.status)
        status = aggregate_status(statusCandidates)
        details = aggregate_details(healths)
        return Health.Builder(status, details).build()

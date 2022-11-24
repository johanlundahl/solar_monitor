import abc
from pytils import validator


class State(metaclass=abc.ABCMeta):

    def __init__(self):
        self.panel_checker = validator.Checker().any()
        self.panel_checker.add_rule(lambda x: x.energy == 0,
                                    'Panel is out of order, 0 production.')
        self.panel_checker.add_rule(lambda x: x.efficiency < 60,
                                    'Panel has low efficiency.')

    @abc.abstractmethod
    def on_event(self, reading):
        pass

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.__class__.__name__


class NormalState(State):

    def on_event(self, panel):
        is_alarm = self.panel_checker.validate(panel)
        if is_alarm:
            return TriggeredState()
        return self


class AlarmState(State):

    def on_event(self, panel):
        is_alarm = self.panel_checker.validate(panel)
        if not is_alarm:
            return NormalState()
        return self


class TriggeredState(State):

    def on_event(self, panel):
        is_alarm = self.panel_checker.validate(panel)
        if not is_alarm:
            return NormalState()
        return AlarmState()

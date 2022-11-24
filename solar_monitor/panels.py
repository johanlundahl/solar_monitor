from jsonpath_ng.ext import parse
from solar_monitor.alarms import NormalState, AlarmState, TriggeredState


class PanelParser():

    def __init__(self, json_data):
        self._json_data = json_data

    def solar_objects(self):
        solar_expr = parse("$..children[?(@.data.id)].data")
        return solar_expr.find(self._json_data)

    def panel_objects(self, objects):
        for p in objects:
            if 'Module' in p.value['name']:
                yield p.value['name'], p.value['id']

    def energy_for_id(self, id):
        path1 = '$..["{}"]'.format(id)
        energy_expr = parse(path1)
        energy = energy_expr.find(self._json_data)
        return energy[0].value['unscaledEnergy']


class PanelDirector():

    def __init__(self, parser):
        self._parser = parser

    def build_panels(self):
        solar_objs = self._parser.solar_objects()
        panels = []
        for name, id in self._parser.panel_objects(solar_objs):
            energy = self._parser.energy_for_id(id)
            panel = Panel(name, id, energy)
            panels.append(panel)
        return panels


class Panel:

    def __init__(self, name=None, id=None, energy=None):
        self._name = name
        self._id = id
        self._energy = energy
        self._alarm_state = NormalState()
        self._efficiency = None

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = value
        self._alarm_state = self._alarm_state.on_event(self)

    @property
    def efficiency(self):
        return self._efficiency

    def set_efficiency(self, value):
        self._efficiency = value
        self._alarm_state = self._alarm_state.on_event(self)

    @property
    def alarm(self):
        return isinstance(self._alarm_state, (AlarmState, TriggeredState))

    @property
    def triggered(self):
        return isinstance(self._alarm_state, TriggeredState)

    @property
    def alarm_state(self):
        return self._alarm_state

    def alarm_raised(self):
        self._alarm_state = self._alarm_state.on_event(self)

    def __repr__(self):
        return (f'Panel({self._name}, {self._id}, {self._energy}, '
                f'{self._efficiency}%, {self._alarm_state})')

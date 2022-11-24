from solar_monitor.handlers import PersistHandler, AlarmHandler
from solar_monitor.handlers import EfficiencyHandler


class PanelManager:

    def __init__(self, panel_url, max_energy_value, alarm_url):
        self.save_panel_url = panel_url
        self.max_energy_value = max_energy_value
        self.alarm_url = alarm_url

        persist_handler = PersistHandler(url=panel_url)
        alarmHandler = AlarmHandler(persist_handler, alarm_url)
        efficiencyHandler = EfficiencyHandler(alarmHandler, max_energy_value)
        self.first_command = efficiencyHandler

    def handle(self, panel):
        self.delegate(panel)

    def delegate(self, panel):
        self.first_command.handle(panel)

import abc
import logging
from pytils import slack


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, next_command=None):
        self._next = next_command

    def handle(self, sensor):
        self.process(sensor)
        if self.proceed:
            self._next.handle(sensor)

    @property
    def proceed(self):
        return self._next is not None

    @abc.abstractmethod
    def process(self, sensor):
        pass


class EfficiencyHandler(Handler):

    def __init__(self, next_command=None, max_energy_value=None):
        self._next = next_command
        self._max_energy_value = max_energy_value

    def process(self, panel):
        logging.info(f'{type(self).__name__} processing of {str(panel)}')
        panel.set_efficiency(round((panel.energy/self._max_energy_value)*100))


class PersistHandler(Handler):

    def __init__(self, next_command=None, url=None):
        self._next = next_command
        self._url = url

    def process(self, panel):
        logging.info(f'{type(self).__name__} processing of {str(panel)}')
        # status_code, data = http.post_json(self._url, panel.to_json())
        # if status_code != 200:
        #    logging.error((f'Status code {status_code} ',
        #                   f'when POST\'ing {panel.to_json()}'))


class AlarmHandler(Handler):

    def __init__(self, next_command=None, slack_webhook_url=''):
        self._next = next_command
        self._slack_webhook_url = slack_webhook_url

    def process(self, panel):
        logging.info(f'{type(self).__name__} processing of {panel}')
        if panel.triggered:
            self.raise_alarm(panel)
            panel.alarm_raised()

    def raise_alarm(self, panel):
        message = (f'Warning {panel.name}! '
                   f'Solar panel produced {panel.energy}Wh which is '
                   f'{panel.efficiency}% of best producing panel.')
        slack.post(self._slack_webhook_url, message)

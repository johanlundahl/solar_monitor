from pytils import config
from solar_monitor.panels import PanelParser, PanelDirector
from solar_monitor.proxy import power_details
from solar_monitor.manager import PanelManager


cfg = config.init()


def run():
    status_code, json_data = power_details(cfg.integration.solar_url,
                                           cfg.integration.username,
                                           cfg.integration.password)

    parser = PanelParser(json_data)
    director = PanelDirector(parser)
    panels = director.build_panels()

    max_value = max(panels, key=lambda x: x.energy)
    manager = PanelManager('url-to-persistance', max_value.energy,
                           cfg.slack_url)

    for panel in panels:
        manager.handle(panel)

        if panel.alarm:
            print(panel)


if __name__ == '__main__':
    run()

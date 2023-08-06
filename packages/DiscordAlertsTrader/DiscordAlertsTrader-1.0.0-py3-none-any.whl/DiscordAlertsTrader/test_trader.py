import os

from DiscordAlertsTrader.brokerages import get_brokerage
from DiscordAlertsTrader.configurator import cfg, channel_ids
from DiscordAlertsTrader.alerts_trader import AlertsTrader
bksession = get_brokerage()

trader = AlertsTrader( brokerage=bksession, cfg=cfg, update_portfolio=False)
trader.update_orders()

import logging
import logging.config
import sys
import signal
from .util import logger

from ha_mqtt_discoverable import Settings, __version__

from discoverable_garage_door.config import Config, config
from discoverable_garage_door.cover import CoverInfo, Cover, Settings
from discoverable_garage_door.gpio import Gpio

mqtt_settings = Settings.MQTT(
    host=config.mqtt_broker.host,
    username=config.mqtt_broker.username,
    password=config.mqtt_broker.password,
    discovery_prefix=config.mqtt_broker.discovery_prefix,
    state_prefix=config.mqtt_broker.state_prefix,
)
doors: [Cover] = []
for door in config.gpio.doors:
    doors.append(
        Cover.cover(mqtt=mqtt_settings, gpio_config=config.gpio, door_config=door)
    )

try:
    signal.pause()
except KeyboardInterrupt:
    print("\nStopping ...")
    for door in doors:
        door.cleanup()

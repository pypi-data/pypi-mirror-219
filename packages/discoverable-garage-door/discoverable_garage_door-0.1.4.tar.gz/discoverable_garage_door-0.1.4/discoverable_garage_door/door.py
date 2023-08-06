from .util import logger
from ha_mqtt_discoverable import EntityInfo
from .config import DoorInfo
from .gpio import Gpio, gpio


class Door:
    door_config: DoorInfo
    button_push_duration: float
    contact_pullup: bool

    def __init__(
        cls,
        button_push_duration_ms: int,
        contact_pullup: bool,
        door_config: DoorInfo = None,
    ):
        logger.debug(
            f"Door({button_push_duration_ms}, {contact_pullup}, {door_config})"
        )
        cls.door_config = door_config
        cls.button_push_duration = button_push_duration_ms / 1000
        cls.contact_pullup = contact_pullup
        gpio.setButtonMode(door_config.button_pin)

    def pushButton(cls):
        gpio.pushButtonFor(cls.door_config.button_pin, cls.button_push_duration)

    def close(cls):
        gpio.pushButtonFor(cls.door_config.button_pin, cls.button_push_duration)

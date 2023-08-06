from __future__ import annotations
from enum import Enum
import json
import logging
import logging.config
from typing import Optional
from .util import logger

from ha_mqtt_discoverable import (
    DeviceInfo,
    Discoverable,
    EntityInfo,
    Subscriber,
    Settings,
)
from .config import Config
from .button import Button
from .contact import Contact

"""
# Example configuration.yaml entry
mqtt:
  button:
    - unique_id: bedroom_switch_reboot_btn
      name: "Restart Bedroom Switch"
      command_topic: "home/bedroom/switch1/commands"
      payload_press: "restart"
      availability:
        - topic: "home/bedroom/switch1/available"
      qos: 0
      retain: false
      entity_category: "config"
      device_class: "restart"
"""


class CoverState(Enum):
    OPENING = "opening"
    OPEN = "open"
    CLOSING = "closing"
    CLOSED = "closed"


class CoverInfo(EntityInfo):
    """Specific information for cover"""

    component: str = "cover"
    enabled_by_default: Optional[bool] = True
    name: str = "My Garage Door"
    object_id: Optional[str] = "my-garage-door-"
    unique_id: Optional[str] = "abc-cba"
    device_class: Optional[str] = "garage"
    value: str = CoverState.OPEN.name

    payload_open: str = "open"
    """The payload to send to trigger the open action."""
    payload_close: Optional[str] = None
    """The payload to send to trigger the close action."""
    payload_stop: str = "stop"
    """The payload to send to trigger the stop action."""
    payload_opening: str = "opening"
    """The the opening state."""
    payload_closed: str = "closed"
    """The the closing state."""
    payload_closing: str = "closing"
    """The the closing state."""
    retain: Optional[bool] = None
    """If the published message should have the retain flag on or not"""


contacts = {}


class Cover(Subscriber[CoverInfo]):
    """Implements an MQTT button:
    https://www.home-assistant.io/integrations/cover.mqtt
    """

    global contacts

    def __init__(
        cls,
        mqtt: Settings.MQTT,
        gpio_config: Config.GPIO,
        door_config: Config.GPIO.Door,
    ):
        cover_info = CoverInfo(name=door_config.name, device_class="garage")
        cover_settings = Settings(mqtt=mqtt, entity=cover_info)
        button = Button(door_config, gpio_config)
        opened_contact = Contact(door_config.opened_contact_pin, gpio_config)
        opened_contact.addEventHandler(Cover.opened_contact_callback)
        closed_contact = Contact(door_config.closed_contact_pin, gpio_config)
        closed_contact.addEventHandler(Cover.closed_contact_callback)
        super().__init__(
            cover_settings,
            command_callback=Cover.cover_button_callback,
            user_data=button,
        )
        cls.cover_info = cover_info
        cls.cover_settings = cover_settings
        cls.button = button
        cls.opened_contact = opened_contact
        cls.closed_contact = closed_contact
        opened_contact.input()
        closed_contact.input()
        cls.open()
        contacts[door_config.opened_contact_pin] = (cls, opened_contact)
        contacts[door_config.closed_contact_pin] = (cls, closed_contact)
        cls.state = CoverState.OPEN
        cls.post_value_if_changed()

    def open(cls):
        cls._send_action(state=cls._entity.payload_open)

    def close(cls):
        cls._send_action(state=cls._entity.payload_close)

    def stop(cls):
        cls._send_action(state=cls._entity.payload_stop)

    def _send_action(cls, state: str) -> None:
        if state in [
            cls._entity.payload_open,
            cls._entity.payload_close,
            cls._entity.payload_stop,
        ]:
            state_message = state
            logger.info(
                f"Sending {state_message} command to {cls._entity.name} using {cls.state_topic}"
            )
            cls._state_helper(state=state_message)

    def _update_state(cls, state) -> None:
        raise Error()

    def cleanup(cls):
        cls.button.cleanup()
        cls.opened_contact.cleanup()
        cls.closed_contact.cleanup()

    def post_value_if_changed(cls):
        if cls.opened_contact.value == cls.closed_contact.value:
            new_state = CoverState.OPENING
        elif cls.opened_contact.value:
            new_state = CoverState.OPEN
        else:
            new_state = CoverState.CLOSED
        if cls.state == new_state:
            return
        cls.set_attributes("value", new_state.value)

    def set_attributes(cls, name, value):
        logger.debug(f"set_attributes {name}, {value}")
        cls._entity.value = value
        cls.value = value
        logger.debug({"value": cls._entity.value})
        super().set_attributes(attributes={"value": cls._entity.value})
        cls._send_action(state=cls.value)

    def _send_action(cls, state: str) -> None:
        logger.info(
            f"Sending {state} command to {cls._entity.name} using {cls.state_topic}"
        )
        super()._state_helper(state=state)

    def cover_contact_callback(cls, opened_contact: bool):
        contact = cls.opened_contact if opened_contact else cls.closed_contact
        contact.input()
        logger.debug(f"contact state: {contact.value}")
        cls.post_value_if_changed()

    @staticmethod
    def opened_contact_callback(pin: int):
        cover, contact = contacts[pin]
        logger.debug(f"opened contact pulsed: {contact}")
        cover.cover_contact_callback(True)

    @staticmethod
    def closed_contact_callback(pin: int):
        cover, contact = contacts[pin]
        logger.debug(f"closed contact pulsed: {contact}")
        cover.cover_contact_callback(False)

    @staticmethod
    def cover_button_callback(client: Client, user_data, message: MQTTMessage):
        cover_payload = message.payload.decode()
        logging.info(f"Received {cover_payload} from HA with {user_data}")
        user_data.pushButtonFor()

    @staticmethod
    def cover(
        mqtt: Settings.MQTT, gpio_config: Config.GPIO, door_config: Config.GPIO.Door
    ) -> Cover:
        return Cover(mqtt, gpio_config, door_config)

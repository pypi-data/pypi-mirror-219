import RPi.GPIO as GPIO

from ha_mqtt_discoverable import EntityInfo


class GpioInfo(EntityInfo):
    button_push_duration: int = 500
    contact_bounce_time_ms: int = 200
    contact_pullup: bool = True


class DoorInfo(EntityInfo):
    button_pin: int = 22
    closed_contact_pin: int = 27
    opened_contact_pin: int = 27


class Gpio:
    pass

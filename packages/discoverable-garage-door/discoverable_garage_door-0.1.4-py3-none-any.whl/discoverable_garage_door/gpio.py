from __future__ import annotations
import asyncio
from .util import logger
from .config import Config, GpioInfo, config
import RPi.GPIO as GPIO


class Gpio:
    gpioInfo: GpioInfo = None

    def __init__(cls, gpioInfo: GpioInfo = None):
        cls.gpioInfo = gpioInfo
        logger.debug(f"GPIO.setmode(GPIO.BOARD)")
        GPIO.setmode(GPIO.BOARD)

    @staticmethod
    def gpio(gpioInfo: GpioInfo = None) -> Gpio:
        return Gpio(gpioInfo)

    @staticmethod
    def setButtonMode(pin: int):
        logger.debug(f"GPIO.setup({pin}, GPIO.OUT)")
        GPIO.setup(pin, GPIO.OUT)

    @staticmethod
    def setSwitchMode(pin: int):
        logger.debug(f"GPIO.setup({pin}, GPIO.IN)")
        GPIO.setup(pin, GPIO.IN)

    @staticmethod
    async def releaseButtonAfterWait(pin: int, wait: float):
        logger.debug(f"await asyncio.sleep({wait})")
        await asyncio.sleep(wait)
        logger.debug(f"Gpio.releaseButton({pin})")
        Gpio.releaseButton(pin)

    @staticmethod
    def pushButton(pin: int):
        logger.debug(f"GPIO.output({pin}, GPIO.HIGH)")
        GPIO.output(pin, GPIO.HIGH)

    @staticmethod
    def pushButtonFor(pin: int, duration: float):
        logger.debug(f"Gpio.pushButton({pin})")
        Gpio.pushButton(pin)
        logger.debug(f"Gpio.releaseButtonAfterWait({pin}, {duration})")
        asyncio.run(Gpio.releaseButtonAfterWait(pin, duration))

    @staticmethod
    def releaseButton(pin: int):
        logger.debug(f"gpio.output({pin}, GPIO.LOW)")
        GPIO.output(pin, GPIO.LOW)

    @staticmethod
    def cleanup():
        logger.debug(f"GPIO.cleanup()")
        GPIO.cleanup()


gpio = Gpio(config.gpio)

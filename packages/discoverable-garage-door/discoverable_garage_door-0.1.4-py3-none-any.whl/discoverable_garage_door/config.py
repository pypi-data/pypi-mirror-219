from __future__ import annotations
from os.path import isfile, exists, dirname, abspath
from os import environ
import os
import io
import yaml
import json
from typing import Optional, List
from pydantic import BaseModel, PositiveInt
from pydantic_yaml import YamlModel
from .util import logger


class MQTT(BaseModel):
    host: str = "hastings.attlocal.net"
    username: str = "homeassistant"
    password: str = ""
    discovery_prefix: str = "homeassistant"
    state_prefix: str = "hmd"


class DoorInfo(BaseModel):
    name: str = "My Door"
    button_pin: int = 18
    opened_contact_pin: int = 27
    closed_contact_pin: int = 17


class GpioInfo(BaseModel):
    button_push_duration_ms: int = 500
    contact_bounce_time_ms: int = 200
    contact_pullup: bool = True
    doors: list["DoorInfo"] = []


class Config(YamlModel):
    mqtt_broker: MQTT = MQTT()
    gpio: GpioInfo = GpioInfo()

    @staticmethod
    def _readfile(filepath) -> Config:
        config_file = abspath(filepath)
        logger.debug(f"importing logfile from file: {config_file}")
        with open(config_file, "r", encoding="utf-8") as f:
            return Config.parse_raw(f.read(), proto="yaml")

    @staticmethod
    def _config(filepath: str = None, string: str = None) -> Config:
        config: Config = None
        if string:
            logger.debug("importing logfile from string")
            config = Config.parse_raw(string)
        elif filepath:
            if isfile(filepath) and exists(filepath):
                config = Config._readfile(filepath)
            raise FileNotFoundError(filepath)
        else:
            config_file = abspath(".config.yaml")
            if isfile(config_file) and exists(config_file):
                config = Config._readfile(config_file)
            else:
                config_file = abspath(dirname(__file__) + "/.config.yaml")
                if isfile(config_file) and exists(config_file):
                    config = Config._readfile(config_file)
                else:
                    config = Config()
        if len(config.gpio.doors) == 0:
            config.gpio.doors.append(DoorInfo())
        return config

    @staticmethod
    def config() -> Config:
        config_filepath: str = None
        if "config" in environ:
            config_filepath = environ["config"]
        return Config._config(filepath=config_filepath)


config = Config.config()

"""
config:
  mqtt_broker:
    host: 192.168.1.143
    username: homeassistant
    password: wu2veeJoi5ox5ooP8wai9ich0oothaepaeg5keteu4mahwui9iexai7uNufae1sa
    discovery_prefix: homeassistant
    state_prefix: hmd
  gpio:
    button_push_duration_ms: 500
    contact_bounce_time_ms: 200
    contact_pullup: true
    doors:
      - button_pin: 18
        closed_contact_pin: 27
        name: main garage door
        opened_contact_pin: 17
"""

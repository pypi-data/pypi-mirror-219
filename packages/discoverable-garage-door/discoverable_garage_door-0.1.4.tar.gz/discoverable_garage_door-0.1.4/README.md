# discoverable-garage-door

[![GitHub](https://img.shields.io/github/license/AixNPanes/discoverable-garage-door)](https://opensource.org/license/apache-2-0/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/AixNPanes/discoverable-garage-door/main.svg)](https://github.com/AixNPanes/discoverable-garage-door)

A python 3 module that takes advantage of Home Assistant's MQTT discovery protocol via ha-mqtt-discoverable to create a Raspberry PI GPIO garage door implementation.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Requirements](#requirements)
  - [Raspberry PI](#raspberry-pi)
  - [Debian](#debian)
  - [Python](#python)
- [Installing](#installing)
  - [installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
  - [Format](#format)
- [Version History](#version-history)
  - [Version 0.1.1 - Complete build config](#version-011---complete-build-config)
  - [Version 0.1.2 - Add Lovelace UI exampe](#version-012---add-lovelace-ui-exampe)
  - [Version 0.1.3 - Rename logger.conf](#version-013---rename-loggerconf)
  - [Version 0.1.4 - Get test bed operating](#version-014---get-test-bed-operating)
- [Uses ha-mqtt-discoverable](#uses-ha-mqtt-discoverable)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->
## Requirements

### Raspberry PI

discoverable_garage_door is designed to run on a PI Zero, Pi 3B+ or PI 4B it may run on other models.

### Debian

discoverable_garage_door is designed to run on Debian Bullseye it may run on other versions.

### Python

dicscverable_garage_door runs on Python 3.10 or later.

## Installing

### installation

`pip install discoverable_garage_door` - not yet implemented

## Usage

python3 -m discoverable_garage_door

## Configuration
a logger configuration file (logger.conf) may be placed in the current directory

a yaml-format configuration file may (.config.yaml) may be placed in the current directory or be specified by the 'config' environment variable


### Format

Example:
```py
    mqtt_broker:
      host: local-broker.local
      username: homeassistant
      password: password
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
```

<p><strong><em>mqtt_broker.host - </em></strong>the name or address of the MQTT broker<br></p>
<p><strong><em>mqtt_broker.username - </em></strong>the username to use to connect with the MQTT broker<br></p>
<p><strong><em>mqtt_broker.password - </em></strong>the password to use to connect with the MQTT broker<br></p>
<p><strong><em>mqtt_broker.discovery_prefix - </em></strong>the prefix to use to publish messages to the MQTT broker, hormally homeassistant<br></p>
<p><strong><em>mqtt_broer.state_prefix - </em></strong>the prefix to use to subscribe messages to the MQTT broker<br></p>
<p><strong><em>gpio.button_push_duration_ms - </em></strong>the length of time in milliseconds that garage door button is virtually pressed, default 500 (ms)<br></p>
<p><strong><em>gpio.contact_bounce_time_ms - </em></strong>the length of time to use to debounce the GPIO inputs, normally 200 (ms)<br></p>
<p><strong><em>gpio.contact_pullup - </em></strong>whether to use a pullup for the GPIO inputs(true) or whether a pullup will be externally used (false)<br></p>
<p><strong><em>gpio.doors - </em></strong>a list of door descriptions<br></p>
<p><strong><em>door.name - </em></strong>the name of the garage door<br></p>
<p><strong><em>door.button_pin - </em></strong>the number of the pin used for the button (GPIO numbering)<br></p>
<p><strong><em>door.closed_contact_pin - </em></strong>the number of the pin used for the closed contact (GPIO numbering)<br></p>
<p><strong><em>door.opened_contact_pin - </em></strong>the number of the pin used for the opened contact (GPIO numbering)<br></p>

## Version History

### Version 0.1.1 - Complete build config

### Version 0.1.2 - Add Lovelace UI exampe

### Version 0.1.3 - Rename logger.conf

### Version 0.1.4 - Get test bed operating

## Uses ha-mqtt-discoverable

- [ha-mqtt-discoverable-cli](https://github.com/unixorn/ha-mqtt-discoverable-cli) 

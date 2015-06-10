# Pocketsphinx post processor

| Input type                  | Output type                 |
|-----------------------------|-----------------------------|
| Tuple(new_value, old_value) | Tuple(new_value, old_value) |

## Category

GPIO

## Description

Filters out GPIO sensors' outputs. This is to avoid flooding the nervous system with information when potentially Minion doesn't need to know about the state of a GPIO pin at all times. It typically allows the output of the [continuous GPIO sensor](/minion/sensing/gpio/pigpio) to only react on changes, when outcome is high only or low only, or a combination of those.

This means it is quite easy to trigger a command only when e.g. the pin changed from low to high.

## Classes

### minion.sensing.postprocessors.gpio.filters.ChangeOnly

Raises a `DataUnavaible` exception if new and old values are equal. Only change will be passed on to the next processor (or the nervous system). This is actually a [StateChange](/minion/sensing/postprocessors/state) post processor

### minion.sensing.postprocessors.gpio.filters.HighOnly

Raises a `DataUnavaible` exception if new value is low.

### minion.sensing.postprocessors.gpio.filters.LowOnly

Raises a `DataUnavaible` exception if new value is high.

## Installation

At this stage, the GPIO post processors are used in conjunction with the [Pigpio](http://abyz.co.uk/rpi/pigpio/python.html) daemon, although they are actually build in an agnostic way: as long as the sensor can provide a tuple as new_value, old_value, these filter can be used.

The post processor itself does not have any other requirements

## Configuration

These post processors do not require configuration

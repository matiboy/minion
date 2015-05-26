# Minion: A voice controlled personal assistant framework for distributed systems

Minion makes it easy to create a **personal assistant system**, likely **controlled by voice** that can gather data via sensors, interpret them via commands and react accordingly using actuators.

It is built to be **distributed** so the sensors and actuators can be **spread over several locations**, and to be **simple** enough to run on single-board computers such as the [Raspberry Pi](https://www.raspberrypi.org/) or the [Banana Pi](http://www.lemaker.org/) - minions love bananas...

Configuration is handled via a **JSON file**, which makes it easy to read without requiring much programming knowledge. Minion also has a simple web based dashboard - codename "Big Boss" - to help you manage the various Minion configurations. It is however a work in progress at the moment.

## Current release v0.1.0 "Just-above-the-crossbar"

![alt text](http://media4.giphy.com/media/h7FwW161xjopW/giphy.gif "Slightly off football kick")

This is the very first release of Minion. It is not exactly according to plan, it's clunky, but it goes **just above the crossbar** so it will do.

## Why Minion?

Without going into the awesomeness of home automation and voice control, why create another framework? There are great tools out there - a few listed [here](http://diyhacking.com/best-voice-recognition-software-for-raspberry-pi/). None served my purpose, here are a few reasons why:

1. Distributed: other frameworks do not seem to want to communicate between devices. Minion can be installed on a device in the kitchen, another Minion instance in your room, and leave the Minion brain somewhere in the living room. Thanks to the Nervous System, sensors can communicate to the brain, the brain can send commands to actuators, regardless of their location;

2. Modular: it has to be very easy to create new modules and to integrate them into Minion. We hope the architecture selected allows for that. Coming soon is a [Yeoman](http://yeoman.io/) generator to allow contributors to quickly scaffold a sensor, command or actuator;

3. Configurable: while basic configuration is available in all the other tools, more complex combinations seem to be limited. Minion allows for complex configuration so you can have for example 2 microphone listeners with different sensitivity, one for activation commands via Pocketsphinx and one for more complex ones via Google Speech API. You can easily have one room with always on listening but also a mobile app on which you need to press to issue commands;

4. Agnostic (mostly): One of the most advanced tool available Jasper is [specifically designed for the Raspberry Pi](http://jasperproject.github.io/documentation/hardware/). While we are huge fans of the Pi, Minion aims to work on any OS, using **your** preferred tools. If you like [SoX](http://sox.sourceforge.net/) more than [FFmpeg](https://www.ffmpeg.org/) to record, it needs to be possible. Minion is written in Python and its modular architecture means that it is OS and library agnostic.

## Architecture
Minion requires 4 components to function fully:

- one or more sensors: ears (microphone), eyes (rss reader) or other (GPS location, temperature reader, anything else)
- a brain which understands a list of commands sent by the sensors' signals
- actuators (hands, mouth) to react when the brain says so
- and very importantly, a nervous system to pass messages along

## Getting started

### Clone the repo

```
  $ git clone https://github.com/matiboy/minion.git
```

### Install requirements

Install basic requirements using the command

```
  $ pip install -r requirements.txt
```

In the near future, modules will be independent so that you will only go through the hassle of installing e.g. `sox` if you are using the `SelectiveMicrophoneListener` but for now hopefully you don't run into too many installation issues.

### Create a config

The easiest way is to start by copying a config from one of the examples

## Sensors

### Audio

## Post processors

### Audio

#### Pocketsphinx

| Input type  | Audio data (wav, 1 channel) |
|-------------|-----------------------------|
| Output type | Text                        |

[Pocketsphinx](http://cmusphinx.sourceforge.net/) is one of the choices of speech to text post processors. It's main advantage is that the speech to text process is handled locally on the same device. This means that it is very fast compared to the Google API or API.ai processors.

You may want to use [this tool](http://www.speech.cs.cmu.edu/tools/lmtool-new.html) to create your own language model and dictionary.

## Testing

Tests can be run using [Nose](https://nose.readthedocs.org/en/latest/). Install Nose in your virtual environment and from the root of Minion's folder, run

```
  $ nosetests
```

## Issues

Feel free to submit issues and enhancement requests.

## Contributing

In general, we follow the "fork-and-pull" Git workflow.

1. Fork the repo on GitHub
2. Commit changes to a branch in your fork
3. Submit pull request

Please make sure to rebase your branch onto the latest before submitting

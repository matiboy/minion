# Minion: A voice controlled personal assistant framework for distributed systems

Minion makes it easy to create a **personal assistant system**, likely **controlled by voice** that can gather data via sensors, interpret them via commands and react accordingly using actuators.

It is built to be **distributed** so the sensors and actuators can be **spread over several locations**, and to be **simple** enough to run on single-board computers such as the [Raspberry Pi](https://www.raspberrypi.org/) or the [Banana Pi](http://www.lemaker.org/) - minions love bananas...

Configuration is handled via a **JSON file**, which makes it easy to read without requiring programming knowledge.

## Current release v0.1.0 "Just-above-the-crossbar"

![alt text](http://media4.giphy.com/media/h7FwW161xjopW/giphy.gif "Slightly off football kick")

This is the very first release of Minion. It is not exactly according to plan, it's clunky, but it goes **just above the crossbar** so it will do.

## Architecture
Minion works similar to a minion (or a human), it requires 4 components to function fully:

- one or more sensors: ears (microphone), eyes (rss reader) or other (GPS location, temperature reader, anything else)
- a brain which understands a list of commands sent by the sensors' signals
- actuators (hands, mouth) to react when the brain says so
- and very importantly, a nervous system to pass messages along

## Getting started

### Clone the repo

Very soon, Minion will be available to install via `pip` but for now, simply clone the repo 

```
  $ git clone https://github.com/matiboy/minion.git
```

### Install requirements

Use `pip install -r requirements.txt` to install all requirements.

In the near future, modules will be independent so that you will only go through the hassle of installing e.g. `sox` if you are using the `SelectiveMicrophoneListener` but for now hopefully you don't run into too many installation issues.

### Create a config

The easiest way is to start by copying



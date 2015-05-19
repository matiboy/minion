"""Minion

Usage:
  minion.py (run|setup) [-d | --debug]
  minion.py (-h | --help)
  minion.py --version

Options:
  -h --help     Show this screen.
  -d --debug    Log debug information to stderr
  --version     Show version.

"""
from __future__ import print_function
from docopt import docopt
import clint.textui
import json
import logging
import minion.core
import minion.core.setup
import minion.core.components.exceptions
import minion.core.utils.console
import minion.core.utils.functions
import minion.core.utils.module_loading
import minion.understanding.errors
import multiprocessing
import os
import sys


def run(settings):
    # Rise, minion
    my_minion = minion.core.Minion()

    with clint.textui.indent(4):
        # Ativate the communication system
        try:
            nerve_settings = settings['nerve']
        except KeyError:
            minion.core.utils.console.console_error('You must provide a nervous system')
            sys.exit(2)

        minion.core.utils.console.console_info('Attaching nervous system')
        my_minion.attach_nervous_system(nerve_settings)

        # Start all the sensors
        sensor_details = settings.get('sensors', [])

        if sensor_details.__len__():
            minion.core.utils.console.console_info('Found {} sensors'.format(sensor_details.__len__()))
            # Might raise NameConflict if two sensors have the same name
            my_minion.attach_sensors(*sensor_details)
        else:
            minion.core.utils.console.console_warn('No sensor found')

        # Start all the actuators
        actuators_details = settings.get('actuators', [])
        if actuators_details.__len__():
            minion.core.utils.console.console_info('Found {} actuators'.format(actuators_details.__len__()))

            # Might raise NameConflict if two actuators have the same name
            my_minion.attach_actuators(*actuators_details)
        else:
            minion.core.utils.console.console_warn('No actuator found')

        # Setup all the commands
        commands_details = settings.get('commands', [])

        if commands_details.__len__():
            minion.core.utils.console.console_info('Found {} commands'.format(commands_details.__len__()))

            # Might raise NameConflict if two commands have the same name
            my_minion.attach_commands(*commands_details)
        else:
            minion.core.utils.console.console_warn('No command found')
    minion.core.utils.console.console_success('Minion is alive and well')
    my_minion.loop()


def main(argv):
    settings = os.getenv('MINION_SETTINGS', 'minion.json')
    options = docopt(__doc__)

    # By default log only info
    level = logging.INFO

    if options['--debug']:
        minion.core.utils.console.console_warn('Logging level set to DEBUG')
        level = logging.DEBUG

    multiprocessing.log_to_stderr(level)

    if options['--version']:
        minion.core.utils.console.console_success('0.1.0')
        sys.exit(0)

    if options['run']:
        try:
            with open(settings) as settings_file:
                settings = json.load(settings_file)
        except IOError:
            minion.core.utils.console.console_error('Settings file not found: {}. Set the environment variable MINION_SETTINGS to the correct path'.format(settings))
            sys.exit(1)
        except ValueError:
            minion.core.utils.console.console_error('Settings file could not be parsed: {}.'.format(settings))
            sys.exit(1)
        minion.core.utils.console.console_info('Starting minion instance run')
        run(settings)

    elif options['setup']:
        minion.core.setup.setup(settings)


if __name__ == '__main__':
    main(sys.argv[1:])

import minion.core.components

defines = {
    minion.core.components.Types.ACTUATOR: [
        {
            'name': 'Raspberry Pi GPIO On then Off',
            'class': 'minion.acting.gpio.pigpio.pigpio.OnThenOff',
            'default_channel': 'minion:gpio',
            'description': '''
# Raspberry Pi GPIO actuator to turn a pin on then back off
# Availability: Raspberry Pi and the likes
#
# WARNING: To avoid having to run Minion as sudo (required to control GPIO pins), please use a GPIO daemon such as http://abyz.co.uk/rpi/pigpio/index.html
#
            ''',
            'setup': [
                {
                    'name': 'pin',
                    'default': 14,
                    'type': 'input',
                    'message': 'GPIO pin number'
                },
                {
                    'name': 'delay',
                    'default': 1.0,
                    'type': 'input',
                    'message': 'Delay before turning back off'
                }
            ],
            'requirements': ('pigpio',)
        }
    ]
}

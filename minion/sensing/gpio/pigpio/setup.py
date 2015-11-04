import minion.core.components

defines = {
    minion.core.components.Types.ACTUATOR: [
        {
            'name': 'Raspberry Pi GPIO Reader',
            'class': 'minion.sensing.gpio.pigpio.pigpio.Reader',
            'description': '''
<h3>Raspberry Pi GPIO sensor</h3>
<h4>Availability: Raspberry Pi and the likes</h4>
<h4>Description</h4>
<p>Raspberry Pi GPIO sensor to read the current value from a GPIO pin</p>
<p>WARNING: To avoid having to run Minion as sudo (required to control GPIO pins), please use a GPIO daemon such as <a href="http://abyz.co.uk/rpi/pigpio/index.html">Pigpio</a></p>
<h4>Pull up or down</h4>
<p>Please read <a href="http://raspi.tv/2013/rpi-gpio-basics-6-using-inputs-and-outputs-together-with-rpi-gpio-pull-ups-and-pull-downs">RPi GPIO basics</a> if you are unclear about pull down or up</p>
<h4>Sensor trigger</h4>
<p>Please use the corresponding post processors if you want the sensor to trigger only on HIGH, LOW or on value changes</p>
<p>For example if you wish the corresponding command to be broadcasted only when the pin changes to HIGH, you can use a combination of (in that order) the ChangeOnly followed by HighOnly post processors</p>
            ''',
            'setup': [
                {
                    'name': 'pin',
                    'default': 14,
                    'type': 'input',
                    'message': 'GPIO pin number'
                },
                {
                    'name': 'period',
                    'default': 1,
                    'type': 'input',
                    'message': 'Sensing period'
                },
                {
                    'name': 'pull_up_or_down',
                    'default': 'PUD_OFF',
                    'type': 'select',
                    'choices': ['PUD_OFF', 'PUD_DOWN', 'PUD_UP'],
                    'message': 'Pull up or down'
                }
            ],
            'requirements': ('pigpio',)
        }
    ]
}

import minion.core.components

defines = {
    minion.core.components.Types.ACTUATOR: [
        {
            'name': 'Pyglet wav player',
            'class': 'minion.acting.mouth.wavplayer.pyglet.PygletPlayer',
            'default_channel': 'minion:play'
        }
    ]
}

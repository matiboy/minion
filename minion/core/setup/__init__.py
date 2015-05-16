import importlib
import inquirer
import json
import minion.acting
import minion.core.components
import minion.core.utils
import minion.nerve
import minion.sensing
import minion.understanding
import pip
import pkgutil
import sys

class QuestionCancelled(Exception):
    pass

MAIN_QUESTIONS = ['Set up nervous system', 'Add/remove sensors', 'Add/remove commands', 'Add/remove actuators', "Nothing, I'm done!"]

NEXT = [
    'nervous_system',
    'amend_sensors',
    'amend_commands',
    'amend_actuators',
    None
]

modules = {
    minion.core.components.Types.ACTUATOR: [],
    minion.core.components.Types.COMMAND: [],
    minion.core.components.Types.NERVOUS_SYSTEM: [],
    minion.core.components.Types.POST_PROCESSOR: [],
    minion.core.components.Types.PRE_PROCESSOR: [],
    minion.core.components.Types.SENSOR: [],
}

def noop(*args):
    pass


def discover():
    minion.core.utils.console.console_info('Discovering Minion modules')
    global modules

    for importer, name, is_package in pkgutil.walk_packages(onerror=noop):
        # Ignore non packages
        if not is_package:
            continue

        # Components should have a setup file
        setup = '{}.setup'.format(name)
        try:
            mod = importlib.import_module(setup)
        # Continue regardless of what error happened
        except:
            continue

        # If minion related, should have a defines dictionary
        if hasattr(mod, 'defines'):
            defines = mod.defines
            # Go through all the types
            for t in modules.keys():
                modules[t].extend(defines.get(t, []))


def main_question(settings, isnew):
    # TODO Update questions with a tick on nervous system and a count on the rest
    if isnew:
        message = 'We suggest you go through each of the 4 steps below one by one'
    else:
        message = 'What would you like to do?'

    questions = (
        inquirer.List(
            'main',
            message=message,
            choices=MAIN_QUESTIONS
        ),
    )

    answer = inquirer.prompt(questions)['main']

    index = MAIN_QUESTIONS.index(answer)

    return NEXT[index]


def get_defined_components(component_type):
    components_defined = {x['name']: x for x in modules[component_type]}
    choices = components_defined.keys() + ['Cancel']
    return choices, components_defined


def prompt_or_cancel(choices, message, cancel_message):
    questions = (
        inquirer.List(
            'choice',
            message=message,
            choices=choices
        ),
    )
    answers = inquirer.prompt(questions)
    choice = answers['choice']
    # Handle cancellation
    if choice == choices[-1]:
        minion.core.utils.console.console_warn(cancel_message)
        raise QuestionCancelled

    return choice


def setup_component(component, default):
    try:
        minion.core.utils.console.console_info(component['description'])
    except KeyError:
        minion.core.utils.console.console_warn('Adding component cancelled')
    questions = [inquirer.Text('name', message='Please name this component (leave blank to cancel)', default=lambda answers: default)]
    name = inquirer.prompt(questions)['name']
    if not name:
        raise QuestionCancelled

    questions = component.get('questions', [])
    configuration_answers = inquirer.prompt(questions)
    config = {
        'name': name,
        'class': component['class'],
    }

    process_answers = component.get('process_answers', lambda x, y: x)
    configuration = process_answers(configuration_answers, component)

    # Only keep if we have anything to save
    if configuration.keys().__len__():
        config['configuration'] = configuration

    return config


def install_requirements(component):
    requirements = component.get('requirements', [])
    if requirements.__len__():
        minion.core.utils.console.console_info('Installing requirements')
    for package in requirements:
        pip.main(['install', package])


def remove_component(settings, key):
    component_settings = settings.get(key, [])
    choices = [x['name'] for x in component_settings] + ['Cancel']
    questions = (inquirer.List('choice', message='Which component would you like to remove?', choices=choices),)
    answer = inquirer.prompt(questions)['choice']
    if answer == choices[-1]:
        minion.core.utils.console.console_warn('No component was removed')
        raise QuestionCancelled

    filtered_settings = filter(lambda x: x['name'] != answer, component_settings)
    settings[key] = filtered_settings
    minion.core.utils.console.console_success('Component <{}> removed'.format(answer))


def add_or_remove(settings, key):
    type_settings = settings.get(key, [])
    if type_settings.__len__():
        questions = (inquirer.List('add_or_remove', choices=['Add', 'Remove']),)
        choice = inquirer.prompt(questions)['add_or_remove']

        if choice == 'Remove':
            # Will raise questions cancelled
            remove_component(settings, key)
            return 1
    return None

def amend_actuators(settings, isnew):
    actuator_settings = settings.get('actuators', [])

    try:
        removed = add_or_remove(settings, 'actuators')
    except QuestionCancelled:
        return 1
    else:
        # This means we went into remove and successed in it
        if removed is not None:
            # so back up
            return None

    choices, actuators = get_defined_components(minion.core.components.Types.ACTUATOR)

    choice = prompt_or_cancel(choices, 'Please choose an actuator', 'Adding of actuator cancelled')

    actuator = actuators[choice]
    # Ask
    try:
        added_component_settings = setup_component(actuator, choice)
    except QuestionCancelled:
        return 1

    # Specifically for actuators, ask for channel
    questions = (inquirer.Text('channels', message='Which channels should this actuator listen to? (use default if unsure. use comma-separated values if more than one channel)', default=actuator.get('default_channel', '')),)

    added_component_settings['channels'] = inquirer.prompt(questions)['channels'].replace(' ', '').split(',')
    actuator_settings.append(added_component_settings)

    # Install required python packages
    install_requirements(actuator)

    minion.core.utils.console.console_success('Actuator successfully added')
    return 1


def amend_sensors(settings, isnew):
    sensor_settings = settings.get('sensors', [])

    try:
        removed = add_or_remove(settings, 'sensors')
    except QuestionCancelled:
        return 1
    else:
        # This means we went into remove and successed in it
        if removed is not None:
            # so back up
            return None

    choices, sensors = get_defined_components(minion.core.components.Types.SENSOR)

    choice = prompt_or_cancel(choices, 'Please choose an sensor', 'Adding of sensor cancelled')

    sensor = sensors[choice]
    # Ask
    try:
        added_component_settings = setup_component(sensor, choice)
    except QuestionCancelled:
        return 1

    actuator_settings.append(added_component_settings)

    # Install required python packages
    install_requirements(sensor)

    minion.core.utils.console.console_success('Sensor successfully added')
    return 1


def nervous_system(settings, isnew):
    choices, nervous_systems_defined = get_defined_components(minion.core.components.Types.NERVOUS_SYSTEM)
    if settings.get('nerve'):
        minion.core.utils.console.console_warn('Nervous system <{}> is already configured'.format(settings.get('nerve')['name']))

    choice = prompt_or_cancel(choices, 'Please choose a nervous system', 'Setting up of nervous system cancelled')

    nervous_system = nervous_systems_defined[choice]
    # Ask
    settings['nerve'] = setup_component(nervous_system, choice)

    # Install required python packages
    install_requirements(nervous_system)

    minion.core.utils.console.console_success('Nervous system set up')
    return None


def write_settings(filename, settings):
    with open(filename, 'w') as f:
        json.dump(settings, f, indent=2)


def setup(settings_file):
    isnew = False
    try:
        with open(settings_file, 'r') as s:
            settings = json.load(s)
        minion.core.utils.console.console_info('Setting up minion instance')
    except IOError:
        minion.core.utils.console.console_info('Setting up new minion instance')
        settings = {}
        isnew = True
    except ValueError:
        minion.core.utils.console.console_error('Unable to parse existing minion setup')
        sys.exit(2)

    # Discover all minion related modules
    discover()

    # ask the main question
    next = main_question(settings, isnew)
    while next is not None:
        # What to do?
        next = globals()[next]
        # This could also be recurring
        stop = False
        while not stop:
            try:
                level_2_answer = next(settings, isnew)
            except QuestionCancelled:
                break
            else:
                write_settings(settings_file, settings)
                # This means stop this level
                if level_2_answer is None:
                    stop = True

        next = main_question(settings, isnew)

    minion.core.utils.console.console_success('Done setting up minion. Run `python minion.py run` to get started')
    sys.exit(0)

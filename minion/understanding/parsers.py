import re


class NoopParser(object):
    def parse(self, original_command, *commands):
        return original_command, commands


class RegexpParser(object):
    def __init__(self, regexp, *flags):
        self.regexp = re.compile(regexp, *flags)

    def parse(self, original_command, *commands):
        pass
from __future__ import absolute_import
import minion.understanding.base
import minion.understanding.operations
import minion.core.components.exceptions
import re


class PrefixRemover(minion.understanding.base.RedirectCommand):
    configuration = {} # Temporarily needed until we completely move to get_action
    threaded = False

    def __init__(self, name, configuration, preprocessors=[]):
        super(PrefixRemover, self).__init__(name, configuration, preprocessors)

        if not self.expressions.__len__():
            self.expressions = [re.compile('^{} *'.format(self.get_prefix()))]

    def _get_output(self, original):
        _, _, after_removal = original.partition(self.get_prefix())

        return after_removal.strip()

    @minion.core.utils.functions.configuration_getter
    def get_prefix(self):
        return None

    @minion.core.utils.functions.configuration_getter
    def get_channel(self):
        return 'minion:command'

    @minion.core.utils.functions.configuration_getter
    def get_action(self):
        return self.get_channel()

    def _validate_configuration(self):
        self.requires_configuration_key('prefix')
        self.requires_non_empty_configuration('prefix')

class PrefixAdder(minion.understanding.base.RedirectCommand):
    threaded = False

    @minion.core.utils.functions.configuration_getter
    def get_prefix(self):
        return None

    @minion.core.utils.functions.configuration_getter
    def get_channel(self):
        return 'minion:command'

    def _validate_configuration(self):
        self.requires_configuration_key('prefix')
        self.requires_non_empty_configuration('prefix')

    def _get_output(self, original):
        return '{prefix}{original}'.format(prefix=self.get_prefix(), original=original)





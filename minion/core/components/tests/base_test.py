from __future__ import absolute_import
import unittest
import minion.core.components
import minion.core.components.exceptions
import sure  # though lint complains that it's never used this is needed


class BaseComponentConfigurationMethods(unittest.TestCase):
    def setUp(self):
        self.component = minion.core.components.BaseComponent('a name', {
            'a': 42,
            'b': 23,
            'c': 'lalala'
            })

    def test_get_configuration_exists(self):
        """ Should return the correct value """
        self.component.get_configuration('a').should.equal(42)
        self.component.get_configuration('c').should.equal('lalala')

    def test_get_configuration_default_provided(self):
        """ Should return the value if default value """
        self.component.get_configuration('a', 1).should.equal(42)
        self.component.get_configuration('d', 1).should.equal(1)

    def test_get_configuration_default_not_provided(self):
        """ Should return the none if invalid key and no default value """
        self.component.get_configuration('d').should.be.none

    def test_get_configuration_dict_exists(self):
        """ Should return the correct values """
        self.component.get_configuration_dict('a', 'c').should.eql({
            'a': 42,
            'c': 'lalala'
            })

    def test_get_configuration_dict_default_provided(self):
        """ Should use none if invalid key """
        self.component.get_configuration_dict('b', 'd').should.eql({
            'b': 23,
            'd': None
            })

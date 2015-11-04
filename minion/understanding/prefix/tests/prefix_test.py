import unittest
from .. import prefix
import minion.core.components.exceptions
import minion.understanding.exceptions
import sure # though lint complains that it's never used this is needed


class PrefixRemoverConfiguration(unittest.TestCase):
    def test_no_prefix(self):
        """Should raise if no prefix or empty prefix"""
        prefix.PrefixRemover.when.called_with('somename', {}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)
        prefix.PrefixRemover.when.called_with('somename', {'prefix': ''}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_ok(self):
        """Should not raise"""
        prefix.PrefixRemover.when.called_with('somename', {'prefix': 'a'}).should_not.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_automatically_created_expression(self):
        """Should auto create expression equivalent to '^<prefix> *'"""
        p = prefix.PrefixRemover('somename', {'prefix': 'abc'})
        p.matches.when.called_with('abc bla').should_not.throw(minion.understanding.exceptions.DoesNotMatch)
        p.matches.when.called_with('dd abc bla').should.throw(minion.understanding.exceptions.DoesNotMatch)
        p.matches.when.called_with('ab c bla').should.throw(minion.understanding.exceptions.DoesNotMatch)


class PrefixRemoverProcess(unittest.TestCase):
    def test_processed_data(self):
        p = prefix.PrefixRemover('dsada', {'prefix': 'harlo'})
        p._get_output('harlo is it me you re looking for').should.equal('is it me you re looking for')

    def test_action(self):
        """Action should be taken from config if available"""
        p = prefix.PrefixRemover('dsada', {'prefix': 'harlo', 'action': 'minion:hfdjsk', 'channel': 'yunotalktome'})
        p.get_action().should.equal('minion:hfdjsk')

    def test_action_channel(self):
        """Action should be taken from channel if action not available"""
        p = prefix.PrefixRemover('dsada', {'prefix': 'harlo', 'channel': 'yunotalktome'})
        p.get_action().should.equal('yunotalktome')

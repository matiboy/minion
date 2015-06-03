import unittest
from .. import pigpio
import mock
import minion.core.components.exceptions
import sure # though lint complains that it's never used this is needed


class SignatureConfiguration(unittest.TestCase):
    def test_no_api_key(self):
        """Should raise if no secret passed"""
        signature.SignaturePostProcessor.when.called_with('somename', {}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_ok(self):
        """Should not raise if secret passed"""
        signature.SignaturePostProcessor.when.called_with('somename', {'secret': 'abc'}).should_not.throw(minion.core.components.exceptions.ImproperlyConfigured)


class HashableData(unittest.TestCase):
    def setUp(self):
        self.pp = signature.SignaturePostProcessor('somename', {'secret': 'hello'})

    def test_hashes_correctly(self):
        d = werkzeug.datastructures.MultiDict([('a', 'b'), ('b', 'c')])
        self.pp._get_hashable_data(d).should.equal('a=b&b=c')

    def test_hashes_alphabetical(self):
        d = werkzeug.datastructures.MultiDict([('d', 'b'), ('b', 'c'), ('a', 'c'), ('g', 'k'), ('e', 'hello')])
        self.pp._get_hashable_data(d).should.equal('a=c&b=c&d=b&e=hello&g=k')

    def test_hashes_ignores_signature(self):
        d = werkzeug.datastructures.MultiDict([('d', 'b'), ('b', 'c'), ('a', 'c'), ('signature', 'k'), ('e', 'hello')])
        self.pp._get_hashable_data(d).should.equal('a=c&b=c&d=b&e=hello')


class ProcessData(unittest.TestCase):
    def setUp(self):
        self.pp = signature.SignaturePostProcessor('somename', {'secret': 'hello'})

    def test_dict_missing_values(self):
        """Post data needs to contain signature and salt"""
        d = werkzeug.datastructures.MultiDict([('a', 'b'), ('b', 'c')])
        self.pp.process.when.called_with(d).should.throw(minion.sensing.exceptions.DataReadError)
        d = werkzeug.datastructures.MultiDict([('a', 'b'), ('signature', 'c')])
        self.pp.process.when.called_with(d).should.throw(minion.sensing.exceptions.DataReadError)

    def test_good_dict(self):
        """Post data has signature and salt"""
        # We're not, at this stage, testing the actual hash comparison
        # TODO Having to mock 2 methods might be a sign that we should have a _validate_data method instead?
        with mock.patch.object(self.pp, '_compare_hashes') as ch:
            with mock.patch.object(self.pp, 'hash'):
                ch.return_value = True
                d = werkzeug.datastructures.MultiDict([('a', 'b'), ('signature', 'c'), ('salt', 'pepper')])
                self.pp.process.when.called_with(d).should_not.throw(minion.sensing.exceptions.DataReadError)

    def test_matches_signature(self):
        """Should match signature when correct"""
        with mock.patch.object(self.pp, 'hash') as h:
            h.return_value = 'wellhellothere'
            d = werkzeug.datastructures.MultiDict([('a', 'b'), ('signature', 'wellhellothere'), ('salt', 'pepper')])
            self.pp.process.when.called_with(d).should_not.throw(minion.sensing.exceptions.DataReadError)

    def test_doesnt_match_signature(self):
        """Should raise when mismatch signature"""
        with mock.patch.object(self.pp, 'hash') as h:
            h.return_value = 'somesignature'
            d = werkzeug.datastructures.MultiDict([('a', 'b'), ('signature', 'adifferentsignature'), ('salt', 'pepper')])
            self.pp.process.when.called_with(d).should.throw(minion.sensing.exceptions.DataReadError)

    def test_full_process(self):
        """Should work when correct"""
        d = werkzeug.datastructures.MultiDict([('a', 'b'), ('timestamp', 1400000), ('channel', 'minion:proximity'), ('signature', 'JDJhJDEyJGdzNUlrZFdpekM1b0tmQnZ6MjNpMGUvZlptUlBneHdDZkFvM0pRQTRlZ2xEQTZQb2ZJdWQ2'), ('salt', '$2a$12$gs5IkdWizC5oKfBvz23i0e')])
        self.pp.process.when.called_with(d).should_not.throw(minion.sensing.exceptions.DataReadError)
        self.pp.process(d).should.eql(d)

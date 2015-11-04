import unittest
from .. import speechtotext
import mock
import minion.core.components.exceptions
import requests
import sure # though lint complains that it's never used this is needed


class SpeechToTextConfiguration(unittest.TestCase):
    def test_no_api_key(self):
        """Should raise if no api key passed"""
        speechtotext.ApiaiSpeechToText.when.called_with('somename', {}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_empty_key(self):
        """Should raise if empty api key passed"""
        speechtotext.ApiaiSpeechToText.when.called_with('somename', {'CLIENT_ACCESS_TOKEN': ''}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_no_sub(self):
        """Should raise if no SUBSCRIBTION_KEY passed"""
        speechtotext.ApiaiSpeechToText.when.called_with('somename', {'CLIENT_ACCESS_TOKEN': 'a'}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_empty_sub(self):
        """Should raise if empty SUBSCRIBTION_KEY passed"""
        speechtotext.ApiaiSpeechToText.when.called_with('somename', {'CLIENT_ACCESS_TOKEN': 'a', 'SUBSCRIBTION_KEY': ''}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_ok(self):
        """Should not raise if SUBSCRIBTION_KEY and CLIENT_ACCESS_TOKEN passed"""
        speechtotext.ApiaiSpeechToText.when.called_with('somename', {'CLIENT_ACCESS_TOKEN': 'a', 'SUBSCRIBTION_KEY': 'b'}).should_not.throw(minion.core.components.exceptions.ImproperlyConfigured)

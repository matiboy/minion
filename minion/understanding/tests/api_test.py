import unittest
from .. import api
import mock
import minion.core.components.exceptions
import requests
import sure # though lint complains that it's never used this is needed

known_data = 'http://jsonplaceholder.typicode.com/users'

class APICommandConfiguration(unittest.TestCase):
    def test_no_url(self):
        """Should raise if no url passed"""
        api.APICommand.when.called_with('somename', {}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_empty_url(self):
        """Should raise if no url passed"""
        api.APICommand.when.called_with('somename', {'url': ''}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_url(self):
        """Should not raise if no url passed"""
        api.APICommand.when.called_with('somename', {'url': 'a'}).should_not.throw(minion.core.components.exceptions.ImproperlyConfigured)


class JsonAPICommandConfiguration(unittest.TestCase):
    def test_no_url(self):
        """Should raise if no url passed"""
        api.JsonAPICommand.when.called_with('somename', {}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_empty_url(self):
        """Should raise if no url passed"""
        api.JsonAPICommand.when.called_with('somename', {'url': ''}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_no_jsonpath(self):
        """Should raise if no json_path passed"""
        api.JsonAPICommand.when.called_with('somename', {'url': 'a'}).should.throw(minion.core.components.exceptions.ImproperlyConfigured)

    def test_ok(self):
        """Should not raise"""
        api.JsonAPICommand.when.called_with('somename', {'url': 'a', 'json_path': 'dsadas'}).should_not.throw(minion.core.components.exceptions.ImproperlyConfigured)


class JsonParser(unittest.TestCase):
    def setUp(self):
        self.response = requests.get(known_data)

    def test_parse_when_gets_data_fails(self):
        """Parse returns None if json can't be parsed"""
        parser = api.JsonParser('a')
        parser.get_data = mock.Mock(side_effect=ValueError)
        parser.parse(self.response).should.be.none

    def test_gets_data(self):
        """Gets data correctly"""
        parser = api.JsonParser('a')
        parser.get_data(self.response).should.be.a('list')

    def test_parses_data_according_to_json_path(self):
        """Parses correctly"""
        parser = api.JsonParser('$[0]')
        parsed = parser.parse(self.response)
        parsed.should.be.a('list')
        parsed.should.have.length_of(1)

    def test_parses_data_according_to_json_path2(self):
        """Parses correctly 2"""
        parser = api.JsonParser('$[1].company.bs')
        parsed = parser.parse(self.response)[0]
        parsed.should.be.equal('synergize scalable supply-chains')

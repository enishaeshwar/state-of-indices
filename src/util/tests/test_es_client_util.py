from unittest import TestCase
from unittest.mock import Mock

from src.util import es_client_util as es_util


class TestClass(TestCase):
    def test_get_aliases(self):
        es_client = Mock()
        aliases = {'media-1642933600': {'aliases': {'media--read': {'is_write_index': False}, 'media--write': {'is_write_index': True}}}}
        es_client.indices.get_alias.return_value = aliases
        actual = es_util.get_es_aliases(es_client)
        self.assertEqual(actual, aliases, "Returned alias does not match")

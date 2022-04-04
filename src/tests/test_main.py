from unittest import TestCase
from unittest.mock import Mock

from src.index_state import get_count_of_docs, get_alias_state, process_index
from src.util import es_client_util as es_util


class TestClass(TestCase):

    def test_get_doc_count_valid(self):
        index_data = [{'epoch': '1649046208', 'timestamp': '04:23:28', 'count': '10'}]
        count = get_count_of_docs(index_data)
        self.assertEqual('10', count, "Returned doc count does not match")

    def test_get_doc_count_not_present(self):
        index_data = [{'epoch': '1649046208', 'timestamp': '04:23:28'}]
        count = get_count_of_docs(index_data)
        self.assertEqual(None, count, "Returned doc count does not match")

    def test_get_doc_count_empty(self):
        index_data = [{'epoch': '1649046208', 'timestamp': '04:23:28', 'count': ''}]
        count = get_count_of_docs(index_data)
        self.assertEqual('', '', "Returned doc count does not match")

    def test_get_alias_state_true(self):
        aliases = {'media--read': {'is_write_index': False}, 'media--write': {'is_write_index': True}}
        is_read_write_enabled = get_alias_state(aliases)
        self.assertEqual(True, is_read_write_enabled, "Returned is_read_write_enabled_true does not match")

    def test_get_alias_state_false(self):
        aliases = {'media--read': {'is_write_index': False}}
        is_read_write_enabled = get_alias_state(aliases)
        self.assertEqual(False, is_read_write_enabled, "Returned is_read_write_enabled_false does not match")

    def test_get_alias_state_invalid(self):
        aliases = {'test--read': {}}
        is_read_write_enabled = get_alias_state(aliases)
        self.assertEqual(False, is_read_write_enabled, "Returned is_read_write_enabled_invalid does not match")

    def test_get_alias_state_no_aliases(self):
        aliases = {}
        is_read_write_enabled = get_alias_state(aliases)
        self.assertEqual(False, is_read_write_enabled, "Returned is_read_write_enabled_invalid does not match")

    def test_process_index1(self):
        es_client = Mock()
        all_indices = {'media-1642933600': {'aliases': {'media--read': {'is_write_index': False}, 'media--write': {'is_write_index': True}}}, 'media-1641833637': {'aliases': {'media--read': {'is_write_index': False}}}}
        index = 'media-1642933600'
        data = {'index_name': 'media-1642933600', 'index_type': 'media', 'creation_time_epoch': '1642933600', 'creation_time_utc': '2022-01-23 10:26:40', 'doc_count': '10', 'is_read_write_enabled': 'True'}
        es_client.cat.count.return_value = [{'epoch': '1649048917', 'timestamp': '05:08:37', 'count': '10'}]
        result = process_index(all_indices, es_client, index)
        self.assertEqual(data, result, "Returned data for process_index match")

    def test_process_index2(self):
        es_client = Mock()
        all_indices = {'media-1642933600': {'aliases': {'media--read': {'is_write_index': False}, 'media--write': {'is_write_index': True}}}, 'media-1641833637': {'aliases': {'media--read': {'is_write_index': False}}}}
        index = 'media-1641833637'
        data = {'index_name': 'media-1641833637', 'index_type': 'media', 'creation_time_epoch': '1641833637', 'creation_time_utc': '2022-01-10 16:53:57', 'doc_count': '5', 'is_read_write_enabled': 'False'}
        es_client.cat.count.return_value = [{'epoch': '1649048917', 'timestamp': '05:08:37', 'count': '5'}]
        result = process_index(all_indices, es_client, index)
        self.assertEqual(data, result, "Returned data for process_index match")
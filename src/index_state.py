import json
import sys
from loguru import logger
import time

from src.util import common_util as common_util, es_client_util as es_util

# Config file base path
BASEPATH = ""
CONFIG_FILE_PATH = BASEPATH + "config/config.yaml"


def get_count_of_docs(index_data):
    """
    Get count of documents for index
    :param index_data:
    :return: count
    """
    index_data_dict = index_data[0]
    count = index_data_dict.get("count")
    return count


def get_alias_state(aliases):
    """
    Get state of index aliases
    :param aliases: Aliases for an index
    :return: is an index has read and write enabled
    """
    read_alias = False
    write_alias = False

    values = list(aliases.values())

    for val in values:
        if not val.get('is_write_index'):
            read_alias = True
        if val.get('is_write_index'):
            write_alias = True

    if read_alias and write_alias:
        return True
    return False


def process_index(all_indices, es_client, index):
    """
    Get the number of documents, timestamp, aliases etc.
    :param all_indices: List fo all indices
    :param es_client: Elastic search connection object
    :param index: Current index
    :return: json data with details on number of docs, timestamp etc
    """
    data = {}
    # Get index name, timestamp
    index_content_type = index.split('-')[0]
    index_creation_time_epoch = index.split('-')[1]
    index_creation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(index_creation_time_epoch)))
    # Get count of docs
    index_data = es_util.get_es_index_count(es_client, index)
    count = get_count_of_docs(index_data)
    # Get aliases and alias state
    aliases = all_indices.get(index).get('aliases')
    is_read_write_enabled = get_alias_state(aliases)
    # Create response object
    data["index_name"] = index
    data["index_type"] = index_content_type
    data["creation_time_epoch"] = index_creation_time_epoch
    data["creation_time_utc"] = index_creation_time
    data["doc_count"] = count
    data["is_read_write_enabled"] = str(is_read_write_enabled)
    return data


def get_state_of_indices(es_client):
    """
    Get state of all indices
    :param es_client: Elastic Search client
    :return: state_of_indices
    """
    state_of_indices = {}
    data_list = []

    all_indices = es_util.get_es_aliases(es_client)
    for index in all_indices:
        data = process_index(all_indices, es_client, index)
        data_list.append(data.copy())

    state_of_indices["state_of_indices"] = data_list
    return json.dumps(state_of_indices, indent=4)


def run_process(env):
    """
    Run process to get state of indices
    :param env: environment
    :return: None
    """
    config = common_util.get_config(CONFIG_FILE_PATH, env)
    logger.info(f"Config loaded:{config}")

    es_client = es_util.get_es_client(config.get('elasticsearch'))
    if es_client is None:
        logger.error(f"Failed to get ES client")
        return

    state_of_indices = get_state_of_indices(es_client)
    if state_of_indices is None:
        logger.error("Index fetch failed")
        return
    logger.info(state_of_indices)


if __name__ == "__main__":
    env = sys.argv[1]
    run_process(env)

import random
import string
import sys

import yaml
from elasticsearch import Elasticsearch
from loguru import logger
import uuid


def get_config(filepath, env):
    """
    Get config daya
    :param filepath: config file path
    :param env: environment
    :return: config data as dict
    """
    config_data = None
    with open(filepath, "r") as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
            config_data = cfg.get(env)
        except yaml.YAMLError as exc:
            print(exc)
    return config_data


def get_es_client(es_config):
    """
    Get elastic search client
    :param es_config: Elastic search config data
    :return: Elastic search connection object
    """
    es_client = None
    try:
        es_client: Elasticsearch = Elasticsearch(
            f"http://{es_config.get('host')}:{es_config.get('port')}",
            timeout=es_config.get('connection-timeout-ms')
        )
        es_client.info()
    except Exception as e:
        logger.error(f"Failed to connect to Elasticsearch. Config:{es_config}")
    return es_client


def get_es_aliases(es_client):
    """
    Return all aliases
    :param es_client: Elastic Search client
    :return: Index aliases
    """
    alias_list = es_client.indices.get_alias(index="*")
    return alias_list


def create_index(index_data, es_client):
    """
    Create an index
    :param index_data: Index data
    :param es_client: Elastic search connection object
    :return: None
    """
    try:
        es_client.indices.create(index=index_data["name"])
        for alias in index_data["aliases"]:
            es_client.indices.put_alias(index=index_data["name"], name=alias["name"],
                                        body={"is_write_index": alias["write-enabled"]})
        logger.info(f"Index {index_data['name']} created successfully. Index Data:{index_data}")
    except Exception as e:
        logger.error(f"Failed to create index. Error:{e}")


def create_indices(indices_to_create, es_client):
    """
    Create indices
    :param indices_to_create: list of indices to create
    :param es_client: Elastic search connection object
    :return: None
    """
    aliases = get_es_aliases(es_client)
    logger.info(f"Present Aliases:{aliases}")
    for index_data in indices_to_create:
        if index_data.get('name') in aliases.keys():
            logger.info(f"Index {index_data.get('name')} is already created.")
        else:
            create_index(index_data, es_client)
            populate_random_documents(index_data.get("name"), index_data.get("number-of-docs"), es_client)


def populate_random_documents(index, num_docs, es_client):
    """
    Populate documents to index
    :param index: Name of index
    :param num_docs: Number of docs
    :param es_client: Elastic search connection object
    :return:
    """
    for i in range(0, num_docs):
        doc_to_index = get_random_doc()
        response = es_client.index(
            index=index,
            id=doc_to_index["id"],
            body=doc_to_index
        )
        logger.debug(f"Successfully indexed document:{doc_to_index}, Response:{response}")


def get_random_doc():
    """
    Create a document
    :return: json document
    """
    return {"id": str(uuid.uuid4()),
            "data": ''.join(random.choices(string.ascii_letters + string.digits, k=10))}


def cleanup_es(indices_to_cleanup, es_client):
    """
    Delete indices
    :param indices_to_cleanup: indices to delete
    :param es_client: Elastic search connection object
    :return: None
    """
    for index in indices_to_cleanup:
        es_client.indices.delete(index=index["name"], ignore=[400, 404])


def populate_es(env, config_filepath):
    """
    Populate ES with test indices, insert documents, add aliases
    :param env: environment
    :param config_filepath: path of the config file
    :return:
    """
    config = get_config(config_filepath, env)
    logger.info(f"Config loaded:{config}")
    es_client = get_es_client(config.get('elasticsearch'))

    if es_client is None:
        logger.error(f"Failed to get ES client")
        return
    logger.info(f"ES client:{es_client}")
    # cleanup_es(config["indices"],es_client)
    create_indices(config.get('indices'), es_client)


if __name__ == "__main__":
    populate_es("local", sys.argv[1])

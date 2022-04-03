import random
import string

from elasticsearch import Elasticsearch
from loguru import logger
import uuid

from src import es_client_util as es_util
from src import common_util as common_util

# Config file base path
BASEPATH = "../"
CONFIG_FILE_PATH = BASEPATH + "config/populate_es_config.yaml"


def get_es_client(es_config) -> Elasticsearch:
    """
    Get elastic search client
    :param es_config:
    :return: connection object
    """
    es_client = None
    try:
        es_client: Elasticsearch = Elasticsearch(
            es_config.get('host', "localhost"),
            port=es_config.get('port', 9200),
            timeout=es_config.get('connection-timeout-ms', 30000),
        )
        es_client.info()
    except Exception as e:
        logger.error(f"Failed to connect to Elasticsearch. Config:{es_config}")
    return es_client


def get_es_aliases(es_client):
    alias_list = es_client.indices.get_alias(index="*")
    return alias_list


def create_index(index_data, es_client):
    try:
        es_client.indices.create(index=index_data["name"])
        for alias in index_data["aliases"]:
            es_client.indices.put_alias(index=index_data["name"], name=alias["name"],
                                        body={"is_write_index": alias["write-enabled"]})
        logger.info(f"Index {index_data['name']} created successfully. Index Data:{index_data}")
    except Exception as e:
        logger.error(f"Failed to create index. Error:{e}")


def create_indices(indices_to_create, es_client):
    aliases = get_es_aliases(es_client)
    logger.info(f"Present Aliases:{aliases}")
    for index_data in indices_to_create:
        if index_data.get('name') in aliases.keys():
            logger.info(f"Index {index_data.get('name')} is already created.")
        else:
            create_index(index_data, es_client)
            populate_random_documents(index_data.get("name"), index_data.get("number-of-docs"), es_client)


def populate_random_documents(index, num_docs, es_client):
    for i in range(0, num_docs):
        doc_to_index = get_random_doc()
        response = es_client.index(
            index=index,
            id=doc_to_index["id"],
            body=doc_to_index
        )
        logger.debug(f"Successfully indexed document:{doc_to_index}, Response:{response}")


def get_random_doc():
    return {"id": str(uuid.uuid4()),
            "data": ''.join(random.choices(string.ascii_letters + string.digits, k=10))}


def cleanup_es(indices_to_cleanup, es_client):
    for index in indices_to_cleanup:
        es_client.indices.delete(index=index["name"], ignore=[400, 404])


def populate_es(env: str):
    config = common_util.get_config(CONFIG_FILE_PATH, env)
    logger.info(f"Config loaded:{config}")
    es_client = es_util.get_es_client(config.get('elasticsearch'))

    if es_client is None:
        logger.error(f"Failed to get ES client")
        return
    logger.info(f"ES client:{es_client}")
    # cleanup_es(config["indices"],es_client)
    create_indices(config.get('indices'), es_client)


if __name__ == "__main__":
    populate_es("local")

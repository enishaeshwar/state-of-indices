from elasticsearch import Elasticsearch


def get_es_client(es_config):
    """
    Get Elastic Search client
    :param es_config: Config data
    :return: Elastic Search connection object
    """
    es_client = Elasticsearch(
        es_config.get('clustername'),
        port=es_config.get('port'),
        timeout=es_config.get('timeout')
    )
    return es_client


def get_es_aliases(es_client):
    aliases = []
    alias_list = es_client.indices.get_alias(index="*")
    for x in alias_list:
        aliases.append(x)
    return aliases


def get_es_index_count(es_client, index_name):
    return es_client.cat.count(index_name, params={"format": "json"})


def get_index_name_and_age(es_client):
    return None
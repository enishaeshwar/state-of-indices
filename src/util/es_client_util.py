from elasticsearch import Elasticsearch


def get_es_client_old(es_config):
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


def get_es_client(es_config):
    es_client: Elasticsearch = Elasticsearch(
            f"http://{es_config.get('host')}:{es_config.get('port')}",
            timeout=es_config.get('connection-timeout-ms')
        )
    return es_client


def get_es_aliases(es_client):
    """
    Return all aliases
    :param es_client: Elastic Search client
    :return: Index aliases
    """
    aliases = es_client.indices.get_alias(index="*")
    return aliases


def get_es_index_count(es_client, index_name):
    """
    Get count of documents in index
    :param es_client: Elastic Search client
    :param index_name: Index name
    :return: count of documents
    """
    return es_client.cat.count(index_name, params={"format": "json"})


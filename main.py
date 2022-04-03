import sys
import yaml
import logging as log

from elasticsearch import Elasticsearch

# Config file base path
BASEPATH = ""
CONFIG_FILE_PATH = BASEPATH + "config.yaml"

# Initialize logger
log.basicConfig(level=log.INFO)


def get_es_client(es_config):
    """
    Get elastic search client
    :param es_config:
    :return: connection object
    """
    es_client = Elasticsearch(
        es_config.get('clustername'),
        port = es_config.get('port'),
        timeout = es_config.get('timeout')
    )
    return es_client


def get_config():
    """
    Initialize global variables, config, connection objects etc
    :return: Config object
    """
    # Load Property file
    cfg = None
    with open(CONFIG_FILE_PATH, "r") as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            print(exc)
    return cfg


def init(env):
    config = get_config()
    config_data = config.get(env)
    print(config_data)
    es_client = get_es_client(config_data.get('elasticsearch'))
    print(es_client)


def run_process(env):
    log.info("Initialize configs and connections")
    init(env)


if __name__ == "__main__":
    env = sys.argv[1]
    run_process(env)



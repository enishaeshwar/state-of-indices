import sys
import yaml
import logging as log

import es_client_util as es_util

# Config file base path
BASEPATH = ""
CONFIG_FILE_PATH = BASEPATH + "config.yaml"

# Initialize logger
log.basicConfig(level=log.INFO)


def get_config():
    """
    Get config data
    :return: config data
    """
    cfg = None
    with open(CONFIG_FILE_PATH, "r") as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            print(exc)
    return cfg


def run_process(env: str):
    log.info("Get config...")
    config = get_config()
    config_data = config.get(env)
    print(config_data)
    log.info("Get config completed.")

    log.info("Get ES connection...")
    es_client = es_util.get_es_client(config_data.get('elasticsearch'))
    print(es_client)
    log.info("Get ES connection completed.")

    log.info("Get list of all indices...")
    aliases = es_util.get_es_aliases(es_client)
    print(aliases)
    log.info("Get all indices done.")

    # log.info("Get name and age of all indices...")
    # aliases = es_util.get_index_name_and_age(es_client)
    # print(aliases)
    # log.info("Get name and age of all indices completed.")

    for index in aliases:
        print(es_util.get_es_index_count(es_client, index))


if __name__ == "__main__":
    env = sys.argv[1]
    run_process(env)

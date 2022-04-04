import yaml


def get_config(filepath, env):
    """
    Parse config.yaml and return environment specific config data
    :param filepath: config file path
    :param env: environment
    :return: dictionary of config_data
    """
    config_data = None
    with open(filepath, "r") as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
            config_data = cfg.get(env)
        except yaml.YAMLError as exc:
            print(exc)
    return config_data

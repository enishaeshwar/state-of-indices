import yaml


def get_config(filepath, env):
    """
    Get config data
    :return: config data
    """
    cfg = None
    with open(filepath, "r") as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
            config_data = cfg.get(env)
        except yaml.YAMLError as exc:
            print(exc)
    return config_data
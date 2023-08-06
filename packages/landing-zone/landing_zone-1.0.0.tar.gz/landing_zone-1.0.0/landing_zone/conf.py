import yaml


def get_target_conf(conf_file):
    target_executable = ""
    target_functions = []
    target_arguments = []

    with open(conf_file, 'r') as f:
        data_loaded = yaml.safe_load(f)
        target_executable = data_loaded['target']

        target_arguments = data_loaded["arguments"]

        target_functions = data_loaded['functions']

    return target_executable, target_arguments, target_functions

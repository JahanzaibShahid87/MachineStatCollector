"""Configuration accessor.

Kept separate to avoid circular dependencies and code duplication
"""

import ConfigParser

config = None
CONFIG_FILES = {
    "prod": "settings.ini",
    "test": "features/settings_test.ini"
}


def load_settings(env="prod"):
    """Loads the settings file into the config object.

    :param env: The environment for which to load the settings
    :type env: str
    :return: None
    """
    global config
    config = ConfigParser.SafeConfigParser()
    config.read(CONFIG_FILES.get(env))


def get(section, option=None, boolean=False, integer=False, floating=False, items=False):
    """
    Wrapper to the SafeConfigParser.get method.

    Arguments, results and exceptions are the same as this method.
    :param section: The section of the config file
    :type section: str
    :param option: The option to select from the given section
    :type option: str
    :param boolean: Indicates whether to read the specified property as a
    Boolean
    :type boolean: bool
    :param integer: Indicates whether to read the specified property as an Int
    :type integer: bool
    :param floating: Indicates whether to read the specified property as a float
    :type boolean: bool
    """
    if boolean:
        return_value = config.getboolean(section, option)
    elif integer:
        return_value = config.getint(section, option)
    elif floating:
        return_value = config.getfloat(section, option)
    elif items:
        return_value = config.items(section)
    else:
        return_value = config.get(section, option)
    return return_value


load_settings()

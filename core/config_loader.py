import configparser
import os

CONFIG_FILE = "config/config.ini"


def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        config["Settings"] = {"interval": "15"}
        config["Games"] = {
            "game1": "BlackDesert64.exe",
            "game2": "cs2.exe"
        }
        config_dir = os.path.dirname(CONFIG_FILE)
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
        print(f"[INFO] Created {CONFIG_FILE}")
    config.read(CONFIG_FILE)
    return config

def save_config(config):
    config_dir = os.path.dirname(CONFIG_FILE)
    if config_dir and not os.path.exists(config_dir):
        os.makedirs(config_dir)
    with open(CONFIG_FILE, "w") as f:
        config.write(f)
    print(f"[INFO] Updated {CONFIG_FILE}")

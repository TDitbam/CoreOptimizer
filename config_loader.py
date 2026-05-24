import configparser
import os

CONFIG_FILE = "config.ini"


def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        config["Settings"] = {"interval": "15"}
        config["Games"] = {
            "game1": "BlackDesert64.exe",
            "game2": "cs2.exe"
        }
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
        print(f"[INFO] Created {CONFIG_FILE}")
    config.read(CONFIG_FILE)
    return config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        config.write(f)
    print(f"[INFO] Updated {CONFIG_FILE}")

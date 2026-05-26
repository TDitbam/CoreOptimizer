import os
import configparser
import pytest
from core.config_loader import load_config, CONFIG_FILE, get_targets

def test_config_creation(tmp_path):
    """Test that config.ini is created if it doesn't exist."""
    # Change directory to tmp_path to avoid messing with real config.ini
    os.chdir(tmp_path)
    
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        
    # load_config will create the file
    load_config()
        
    assert os.path.exists(CONFIG_FILE)
    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    assert "Settings" in config
    assert "Targets" in config
    assert config["Settings"]["interval"] == "5"

def test_config_loading(tmp_path):
    """Test loading an existing config."""
    os.chdir(tmp_path)
    
    config = configparser.ConfigParser()
    config["Settings"] = {"interval": "30"}
    config["Targets"] = {"test_game.exe": "HIGH"}
    
    # Ensure config directory exists for the test if needed
    config_dir = os.path.dirname(CONFIG_FILE)
    if config_dir and not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    with open(CONFIG_FILE, "w") as f:
        config.write(f)
        
    loaded_config = load_config()
    assert loaded_config["Settings"]["interval"] == "30"
    targets = dict(get_targets(loaded_config))
    assert targets["test_game.exe"] == "HIGH"

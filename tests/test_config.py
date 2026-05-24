import os
import configparser
import pytest
from core.config_loader import load_config, CONFIG_FILE

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
    assert "Games" in config
    assert config["Settings"]["interval"] == "15"

def test_config_loading(tmp_path):
    """Test loading an existing config."""
    os.chdir(tmp_path)
    
    config = configparser.ConfigParser()
    config["Settings"] = {"interval": "30"}
    config["Games"] = {"test_game": "notepad.exe"}
    
    # Ensure config directory exists for the test if needed
    config_dir = os.path.dirname(CONFIG_FILE)
    if config_dir and not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    with open(CONFIG_FILE, "w") as f:
        config.write(f)
        
    loaded_config = load_config()
    assert loaded_config["Settings"]["interval"] == "30"
    assert loaded_config["Games"]["test_game"] == "notepad.exe"

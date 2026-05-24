import os
import configparser
import pytest
from config_loader import load_config, CONFIG_FILE

def test_config_creation(tmp_path):
    """Test that config.ini is created if it doesn't exist."""
    # Change directory to tmp_path to avoid messing with real config.ini
    os.chdir(tmp_path)
    
    # We expect sys.exit() or similar if we use the original load_config as it calls exit()
    # Let's mock the CONFIG_FILE path if possible, but load_config uses a global.
    # For now, we verify the logic inside load_config.
    
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        
    # Since load_config calls exit(), we use pytest.raises(SystemExit)
    with pytest.raises(SystemExit):
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
    
    with open(CONFIG_FILE, "w") as f:
        config.write(f)
        
    loaded_config = load_config()
    assert loaded_config["Settings"]["interval"] == "30"
    assert loaded_config["Games"]["test_game"] == "notepad.exe"

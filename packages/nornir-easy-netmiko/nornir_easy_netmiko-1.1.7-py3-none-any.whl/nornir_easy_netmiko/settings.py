from pathlib import Path

from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir_easy_netmiko import Netmiko

InventoryPluginRegister.register("easy_netmiko", Netmiko)

BASE_DIR = Path(__file__).resolve().parent

CONFIG = {
    'runner': {
        "plugin": "threaded",
        "options": {
            "num_workers": 100,
        },
    },
    'inventory': {
        "plugin": "SimpleInventory",
        "options": {
            "host_file": Path("config", "hosts.yaml"),
            "group_file": Path("config", "groups.yaml")
        },
    },
    "logging": {
        "to_console": True
    }
}
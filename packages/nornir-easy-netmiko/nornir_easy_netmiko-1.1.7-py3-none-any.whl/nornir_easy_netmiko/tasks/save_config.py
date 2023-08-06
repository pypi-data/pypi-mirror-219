from nornir import InitNornir
from config.settings import CONFIG
from nornir_easy_netmiko import netmiko_save_config

nr = InitNornir(**CONFIG).with_processors()
nr = nr.filter(platform='hp_comware')

nr.run(
    task=netmiko_save_config,
)
from nornir import InitNornir
from settings import CONFIG
from nornir_easy_netmiko import netmiko_send_command
from processor import Match_processor

nr = InitNornir(**CONFIG).with_processors([Match_processor()])


results = nr.run(
    task=netmiko_send_command,
    command_string='dis device manu'
)
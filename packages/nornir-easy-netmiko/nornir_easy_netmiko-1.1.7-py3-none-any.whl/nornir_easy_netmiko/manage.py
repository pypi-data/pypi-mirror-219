import argparse
from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir_easy_netmiko import Netmiko
from config.settings import BASE_DIR
from pathlib import Path

if __name__ == "__main__":
    InventoryPluginRegister.register("easy_netmiko", Netmiko)

    parser = argparse.ArgumentParser(description="Nornir task runner.")
    parser.add_argument("subcommand")
    parser.add_argument("task", help="Task filename.")

    args = parser.parse_args()
    if args.subcommand == 'run':
        task_path = Path(BASE_DIR, "tasks", args.task+".py")

        try:
            with open(task_path, 'r') as file:
                code = file.read()
                exec(code)
        except FileNotFoundError:
            print(
                f"Couldn't run task '{args.task}'. You must confirm '{args.task}.py' "
                 "in 'tasks/' directory."
            )
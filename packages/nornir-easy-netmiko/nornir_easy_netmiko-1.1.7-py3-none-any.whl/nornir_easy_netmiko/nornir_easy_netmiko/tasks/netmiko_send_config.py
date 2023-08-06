from typing import Any, List, Optional
from nornir.core.task import Result, Task
from nornir_easy_netmiko.connections import CONNECTION_NAME
from nornir_easy_netmiko.errors import error_handle
from jinja2 import Template, StrictUndefined
import io

def commands_render(data, config_commands):
    new_config_commands = []
    for c in config_commands:
        template = Template(c, undefined=StrictUndefined, trim_blocks=True)
        new_config_commands.append(template.render(data['data']))
    return new_config_commands

def file_render(data, config_file):
    with io.open(config_file, "rt", encoding="utf-8") as cfg_file:
        template = Template(cfg_file.read(), undefined=StrictUndefined, trim_blocks=True)
        new_config_commands = template.render(data['data']).strip().split('\n')
    return new_config_commands

@error_handle
def netmiko_send_config(
    task: Task,
    config_commands: Optional[List[str]] = None,
    config_file: Optional[str] = None,
    enable: bool = True,
    dry_run: Optional[bool] = None,
    **kwargs: Any
) -> Result:
    """
    Execute Netmiko send_config_set method (or send_config_from_file)

    Arguments:
        config_commands: Commands to configure on the remote network device.
        config_file: File to read configuration commands from.
        enable: Attempt to enter enable-mode.
        dry_run: Whether to apply changes or not (will raise exception)
        kwargs: Additional arguments to pass to method.

    Returns:
        Result object with the following attributes set:
          * result (``str``): string showing the CLI from the configuration changes.
    """
    net_connect = task.host.get_connection(CONNECTION_NAME, task.nornir.config)

    # netmiko_send_config does not support dry_run
    dry_run = task.is_dry_run(dry_run)
    if dry_run is True:
        raise ValueError("netmiko_send_config does not support dry_run")

    if enable:
        net_connect.enable()

    if config_commands:
        new_config_commands = commands_render(task.host.dict(), config_commands)
        result = net_connect.send_config_set(config_commands=new_config_commands, **kwargs)
    elif config_file:
        new_config_commands = file_render(task.host.dict(), config_file)
        result = net_connect.send_config_set(config_commands=new_config_commands, **kwargs)
    else:
        raise ValueError("Must specify either config_commands or config_file")

    return Result(host=task.host, result=result, changed=True)

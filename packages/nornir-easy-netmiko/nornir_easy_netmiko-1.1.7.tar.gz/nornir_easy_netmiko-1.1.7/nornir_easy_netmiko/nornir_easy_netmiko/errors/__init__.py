import logging
from netmiko.exceptions import NetMikoAuthenticationException, NetmikoTimeoutException
from jinja2.exceptions import UndefinedError
from nornir.core.task import Result
from functools import wraps

logger = logging.getLogger("nornir")

def error_handle(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        task = args[0]
        host = task.host
        base_string = f"{host.name}({host.hostname}:{host.port})"
        try:
            result = func(*args, **kwargs)
            logger.info(f"{base_string} excute <{task}> success.")
            return result
        except NetMikoAuthenticationException as e:
            logger.warning(f"{base_string} user/password invaild.")
            return Result(host, exception=e, failed=True)
        except NetmikoTimeoutException as e:
            logger.warning(f"{base_string} connect timeout.")
            return Result(host, exception=e, failed=True)
        except UndefinedError as e:
            logger.warning(f"{base_string} {e}")
            return Result(host, exception=e, failed=True)
    return wrapper
            
                

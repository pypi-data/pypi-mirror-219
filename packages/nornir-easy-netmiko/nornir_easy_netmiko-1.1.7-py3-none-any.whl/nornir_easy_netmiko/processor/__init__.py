import re
import csv
import time
import logging
from config.settings import BASE_DIR
from os import path, mkdir
from pathlib import Path
from nornir.core.inventory import Host
from nornir.core.task import Task, AggregatedResult, Result, MultiResult

logger = logging.getLogger('nornir')

# writerow(row)
def csv_writer(path, data) -> None:
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def save_outputs(save_path, filename, outputs) -> None:
    if not path.exists(save_path):
        mkdir(save_path)
    with open(Path(save_path, filename), 'a', encoding='utf8') as f:
        for o in outputs:
            f.write(o)

class Match_processor:
    # 任务开始运行时执行的动作
    def task_started(self, task: Task) -> None:
        self.save_path = Path(BASE_DIR, 'save', f'{time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime())}')

    # 任务运行结束后执行的动作
    def task_completed(self, task: Task, result: AggregatedResult) -> None:
        pass

    # 任务分配给单台主机运行时执行的动作
    def task_instance_started(self, task: Task, host: Host) -> None:
        pass

    # 任务分配给单台主机运行完成后执行的动作
    def task_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        if not result.exception:
            output = result.result
            cmd = result.command_string
            # 保存回显
            save_outputs(self.save_path, f'{host.name}({host.hostname}).txt', output)
            # 收集 MAC 地址
            if cmd == 'dis device manu':
                value = re.search(r'([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}', output)
                value = value.group() if value else None
                csv_writer(
                    Path(BASE_DIR, 'save', 'result.scv'), 
                    [host.name, host.hostname, value]
                )

    # 子任务开始运行时执行的动作
    def subtask_instance_started(self, task: Task, host: Host) -> None:
        pass

    # 子任务结束运行时执行的动作
    def subtask_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        pass
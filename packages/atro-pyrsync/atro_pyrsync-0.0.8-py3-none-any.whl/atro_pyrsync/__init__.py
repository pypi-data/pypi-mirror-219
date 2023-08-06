import os
import subprocess
from pathlib import Path

from pylog import set_logger

from pyrsync.helpers import wrap_in_double_quotes


def rsync(source: Path, destination: Path, options: list[str] = [], exclusions: list[str] = [], cwd=os.getcwd(), logger=set_logger()):
    log_msg = f"Running rsync from {source.as_posix()} to {destination.as_posix()}"
    if len(options) == 1:
        log_msg += f" with option {options[0]}"
    elif len(options) > 1:
        log_msg += f" with options {', '.join(options)}"
    exclusion_command = []
    if len(exclusions) > 0:
        if len(exclusions) == 1:
            log_msg += f" excluding {exclusions[0]}"
        else:
            log_msg += f" excluding {', '.join(exclusions)}"

        exclusion_command = [f'--exclude="{exclusion}"' for exclusion in exclusions]

    logger.info(log_msg)
    command_list = [
        "rsync",
        *options,
        wrap_in_double_quotes(str(source) + "/"),
        wrap_in_double_quotes(str(destination) + "/"),
        *exclusion_command,
    ]
    command = " ".join(command_list)
    logger.info("Command ran: '" + command + "'")
    output = subprocess.run(command, cwd=cwd, shell=True, capture_output=True)
    logger.debug("Rsync output: " + output.stdout.decode())
    if output.stderr:
        logger.error("Rsync error: " + output.stderr.decode())
    if output.returncode != 0:
        raise Exception("Rsync failed")

# Copyright (c) 2022 Star Lab, Inc.

"""
This module contains utilties for working with systemd services.
"""

import subprocess
from subprocess import CalledProcessError
from subprocess import STDOUT
import time
from datetime import datetime
from typing import Dict
import warnings


def _convert_datetime_to_journalctl_timestamp(date_time: datetime) -> str:
    """
    Converts the specified datetime object into a timestamp string in a format
    consumable by the 'journalctl' Linux command (example: 2021-01-22 16:05:00)
    """
    return date_time.strftime("%Y-%m-%d %H:%M:%S.%f")


def get_service_properties(service_name: str) -> Dict[str, str]:
    """
    Returns a dictionary of the current systemd service properties for the specified
    service
    """
    try:
        command_line = ["systemctl", "show", service_name]
        command_output = subprocess.check_output(command_line, text=True)
    except (OSError, CalledProcessError) as exception:
        # Prevent exception stack backtrace deep into the standard library
        # implementation
        raise exception from None

    service_properties = {}
    for line in command_output.splitlines():
        key, value = line.split("=", maxsplit=1)
        key = key.strip()
        value = value.strip()
        service_properties[key] = value

    return service_properties


def get_service_log(service_name: str, since_datetime: datetime) -> str:
    """
    Returns the service's logs since the specified datetime
    """
    since_timestamp = _convert_datetime_to_journalctl_timestamp(since_datetime)

    command_line = [
        "journalctl",
        "-u",
        service_name,
        "--since",
        since_timestamp,
    ]

    try:
        command_output = subprocess.check_output(command_line, text=True)
    except (OSError, CalledProcessError) as exception:
        raise exception from None

    return command_output


def does_service_exist(service_name: str) -> bool:
    """
    Determines whether the specified service exists on the current system
    """
    try:
        command_line = ["systemctl", "status", service_name]
        subprocess.check_output(command_line, stderr=STDOUT)
    except FileNotFoundError:
        return False  # No systemctl at all
    except OSError as exception:
        warnings.warn(f"Could not run systemctl: {exception}")
        return False
    except CalledProcessError as exception:
        service_does_not_exist = exception.returncode == 4
        if service_does_not_exist:
            return False

    return True


def start_service(service_name: str) -> None:
    """
    Starts the specified systemd service, raising an exception on error
    """
    try:
        command_line = ["systemctl", "start", service_name]
        subprocess.check_output(command_line, stderr=STDOUT)
    except CalledProcessError as exception:
        raise exception from None


def restart_service(service_name: str, check: bool = False) -> None:
    """
    Restarts the specified systemd service, raising an exception on error
    only if check=True
    """
    try:
        command_line = ["systemctl", "restart", service_name]
        subprocess.run(command_line, capture_output=True, check=check)
    except CalledProcessError as exception:
        raise exception from None


def stop_service(service_name: str) -> None:
    """
    Stops the specified systemd service, raising an exception on error
    """
    try:
        command_line = ["systemctl", "stop", service_name]
        subprocess.check_output(command_line, stderr=STDOUT)
    except (OSError, CalledProcessError) as exception:
        raise exception from None


def reload_all_service_settings() -> None:
    """
    Reloads the service settings for all systemd services, from their
    corresponding unit files
    """
    try:
        command_line = ["systemctl", "daemon-reload"]
        subprocess.check_output(command_line, stderr=STDOUT)
    except (OSError, CalledProcessError) as exception:
        raise exception from None

    # Because of a systemd-related race condition, if we later attempt to
    # start the service too soon after executing "systemctl daemon-reload",
    # then the kernel never emits system call audit logging. This sleep
    # addresses that problem.
    time.sleep(5)


def is_system_using_systemd() -> bool:
    try:
        result = subprocess.run(
            ["systemctl", "is-system-running"], text=True, stdout=subprocess.PIPE
        )
    except OSError:
        return False  # Likely not installed at all

    status = result.stdout.strip()
    return status not in ("offline", "unknown")

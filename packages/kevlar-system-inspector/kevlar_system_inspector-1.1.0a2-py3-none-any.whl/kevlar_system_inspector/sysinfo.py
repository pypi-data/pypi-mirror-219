import platform
import re
from multiprocessing import cpu_count
from typing import Dict


def read_os_release() -> Dict[str, str]:
    try:
        os_release = open("/etc/os-release", "r")
    except OSError:
        return {}

    release = {}
    for line in os_release:
        m = re.match(r"""([^=]+)=(["']?)(.+)(\2)$""", line)
        if m:
            release[m.group(1)] = m.group(3).strip()
    return release


def get_cpu_name() -> str:
    try:
        cpuinfo = open("/proc/cpuinfo", "r")
    except OSError:
        return "unknown"

    with cpuinfo:
        for line in cpuinfo:
            m = re.match(r"model name\s*:\s*(.*)", line)
            if m:
                return m.group(1).strip()

    return "unknown"


def get_system_info() -> Dict[str, str]:
    info = {}

    release = read_os_release()
    if "PRETTY_NAME" in release:
        info["Operating System"] = release["PRETTY_NAME"]
    else:
        name = release.get("NAME", "unknown OS")
        ver = release.get("VERSION", "unknown version")
        info["Operating System"] = f"{name}, {ver}"

    info["Kernel"] = " ".join([platform.release(), platform.version()])
    info["Architecture"] = platform.machine()
    info["CPU"] = f"{get_cpu_name()} x {cpu_count()}"
    return info

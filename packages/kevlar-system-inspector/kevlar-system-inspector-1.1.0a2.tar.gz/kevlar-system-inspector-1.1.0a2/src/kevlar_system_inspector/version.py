VERSION = "1.1.0a2"


def is_full_version() -> bool:
    try:
        import kevlar_system_inspector_extras  # noqa: 401
    except ImportError:
        return False
    return True


def get_version() -> str:
    ver = VERSION
    if not is_full_version():
        ver += " Lite"
    return ver

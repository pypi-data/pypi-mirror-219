def dict_to_string(data: dict, multi=False) -> str:
    """Convert a dict to a string"""
    return "".join(f"{key}: {value}\n" for key, value in data.items()) if multi else \
        "".join(f"{key}: {value}" for key, value in data.items())

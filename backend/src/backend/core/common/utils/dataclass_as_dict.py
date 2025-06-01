from dataclasses import asdict, is_dataclass


def to_dict(dataclass_obj):
    if not is_dataclass(dataclass_obj):
        raise ValueError
    return {k: v for k, v in asdict(dataclass_obj).items()}


def iter_items(dataclass_obj):
    if not is_dataclass(dataclass_obj):
        raise ValueError
    return ((k, v) for k, v in asdict(dataclass_obj).items())
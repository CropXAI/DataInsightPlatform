RULES = {
    "id": {
        "unique": True,
        "not_null": True,
    },
    "manufacturer": {
        "not_null": True,
        "max_length": 255,
    },
    "nitrogen_perc": {
        "not_null": False,
        "range": (0, 100),
        "type": float,
    },
    "phosphorus_perc": {
        "not_null": False,
        "range": (0, 100),
        "type": float,
    },
    "kalium_perc": {
        "not_null": False,
        "range": (0, 100),
        "type": float,
    },
    "sulfur_perc": {
        "not_null": False,
        "type": float,
    },
    "link_to_product": {
        "not_null": True,
        "is_url": True,
    },
    "name": {
        "not_null": True,
        "max_length": 255,
        "unique": True,
    },
}

from __future__ import annotations

from typing import Any

translate_property_map = {
    "editable": "develop",
    "ref": "rev",
    "index": "source",
}


def translate_properties(properties: dict[str, Any]) -> dict[str, Any]:
    key_list = list(properties.keys())
    for k in key_list:
        if k in translate_property_map:
            properties[translate_property_map[k]] = properties.pop(k)
    return properties

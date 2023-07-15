from typing import Any, Dict

translate_property_map = {
    "editable": "develop",
    "ref": "rev",
    "index": "source",
}


def translate_properties(properties: Dict[str, Any]) -> Dict[str, Any]:
    key_list = list(properties.keys())
    for k in key_list:
        if k in translate_property_map:
            properties[translate_property_map[k]] = properties.pop(k)
    return properties

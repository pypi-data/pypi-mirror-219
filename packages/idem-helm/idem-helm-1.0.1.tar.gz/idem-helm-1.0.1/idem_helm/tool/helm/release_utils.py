from typing import Any
from typing import Dict

import yaml


def convert_raw_release_to_present(
    hub, release_metadata, release_values
) -> Dict[str, Any]:
    if not release_metadata:
        return None

    result = {"resource_id": release_metadata["name"]}
    skip_attributes = [
        "app_version",
        "status",
        "revision",
        "updated",
    ]
    for key, value in release_metadata.items():
        if not key in skip_attributes:
            result[key] = value

    if release_values:
        if isinstance(release_values, dict):
            result["values"] = release_values
        elif release_values.rstrip():
            result["values"] = yaml.load(release_values.rstrip(), Loader=yaml.Loader)

    return result

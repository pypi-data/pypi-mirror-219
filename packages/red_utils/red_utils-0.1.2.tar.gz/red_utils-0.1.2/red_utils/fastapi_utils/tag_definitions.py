"""Define custom FastAPI endpoint tags.

The tags_metadata object can be imported by the main FastAPI app.
As endpoints are created, their metadata can be defined here as
a list object.
"""
from __future__ import annotations

## Add metadata to tags assigned throughout the app. If a router/endpoint's tags match
#  any of these, the description and other metadata will be applied on the docs page.
#  This tags_metadata can be imported and extended with tags_metadata.append(new_tags_dict).
#
#  You can also create a new list of tags ([{"name": ..., "description": ...}, ...]) and join
#  them with tags_metadata = tags_metadata + new_tags_list
tags_metadata = [
    {
        "name": "default",
        "description": "Tags have not been added to these endpoints/routers.",
    },
    {
        "name": "util",
        "description": "Utility functions, routes, & more. These utils are in the root of the app, and accessible by all sub-apps and routers.",
    },
]

garlic_metadata = {
    "name": "garlic",
    "description": "Interact with Garlic in the database.",
}
tags_metadata.append(garlic_metadata)

inventory_metadata = {
    "name": "inventory",
    "description": "Interact with the store's inventory.",
}

tags_metadata.append(inventory_metadata)

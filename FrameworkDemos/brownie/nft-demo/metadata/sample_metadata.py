import json


# METADATA_TEMPLATE = {
#     "name": "",
#     "description": "",
#     "image": "",
#     "attributes": [{"trait_type": "cuteness", "value": 100}],
# }


class Metadata():
    def __init__(self, name: str, description: str, image: str, attributes: list) -> None:
        self.name = name
        self.description = description
        self.image = image
        self.attributes = attributes

    def __repr__(self) -> str:
        return json.dumps(self.__dict__)
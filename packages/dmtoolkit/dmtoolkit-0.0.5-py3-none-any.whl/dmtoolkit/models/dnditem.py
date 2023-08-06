from dmtoolkit.models.dndobject import DnDObject
from autonomous import log
import markdown


class Item(DnDObject):
    attributes = {
        "name": "",
        "image": {"url": "", "asset_id": 0, "raw": None},
        "desc": "",
        "rarity": "",
        "cost": 0,
        "attunement": False,
        "duration": "",
        "damage_dice": "",
        "damage_type": "",
        "weight": 0,
        "ac_string": "",
        "strength_requirement": None,
        "properties": [],
        "tables": [],
    }

    def __init__(self, **kwargs):
        self.desc_md = markdown.markdown(self.desc)

    @classmethod
    def update_db(cls):
        cls._update_db(cls._api.Open5eItem)

    def get_image_prompt(self):
        description = self.__dict__.get("desc", "on display in the shop")
        return f"A full color Rusted Pixel style image of an item from Dungeons and Dragons 5e called {self.name}. Additional details:  {description}"

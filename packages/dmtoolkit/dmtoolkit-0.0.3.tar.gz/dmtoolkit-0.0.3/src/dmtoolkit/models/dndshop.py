from autonomous.model.automodel import AutoModel
from autonomous import log
import random
from autonomous.apis import OpenAI
from autonomous.storage.cloudinarystorage import CloudinaryStorage


class Shop(AutoModel):
    attributes = {
        "name": "",
        "image": {"url": "", "asset_id": 0, "raw": None},
        "shoptype": "",
        "owner": None,
        "inventory": {},
        "location": "",
        "desc": "",
    }

    def generate_image(self):
        resp = OpenAI().generate_image(
            self.get_image_prompt(),
            n=1,
        )
        folder = f"dnd/{self.__class__.__name__.lower()}s"
        self.image = CloudinaryStorage().save(resp[0], folder=folder)
        self.save()

    def get_image_prompt(self):
        description = self.desc or "A simple shop with wooden counters and shelves."
        style = random.choice(
            ["pixar style 3d image", "colored pencil sketch", "watercolor"]
        )
        return f"A full color {style} of a fantasy world merchant shop called {self.name} with the following description: {description}"

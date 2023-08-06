from dmtoolkit.apis import open5eapi

from autonomous.apis import OpenAI
from autonomous.storage.cloudinarystorage import CloudinaryStorage
from autonomous.model.automodel import AutoModel
from autonomous import log

from slugify import slugify


class DnDObject(AutoModel):
    _api = open5eapi
    _storage = CloudinaryStorage()

    @property
    def slug(self):
        return slugify(self.name)

    def save(self):
        if self.image.get("raw"):
            folder = f"dnd/{self.__class__.__name__.lower()}s/{self.slug}"
            self.image = self._storage.save(self.image["raw"], folder=folder)
        return super().save()

    def generate_image(self):
        resp = OpenAI().generate_image(
            self.get_image_prompt(),
            n=1,
        )
        folder = f"dnd/{self.__class__.__name__.lower()}s"
        self.image = self._storage.save(resp[0], folder=folder)
        return self.save()

    def get_image_prompt(self):
        return f"A full color portrait of a {self.name} from Dungeons and Dragons 5e - {self.desc}"

    @classmethod
    def _update_db(cls, api=None):
        if api:
            for updated_record in api.all():
                if record := cls.find(slug=slugify(updated_record["name"])):
                    record.__dict__.update(updated_record)
                else:
                    record = cls(**updated_record)

                if not record.save():
                    raise Exception(f"Failed to save {record}")

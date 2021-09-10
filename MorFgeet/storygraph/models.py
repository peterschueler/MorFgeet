import uuid

from django.core.exceptions import ValidationError
from django.db import models


# from https://stackoverflow.com/questions/49735906/how-to-implement-singleton-in-django
class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        self.id = 1
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls


class DataBlock(models.Model):
    text = models.TextField()
    link = models.OneToOneField(
        "Link", on_delete=models.CASCADE, related_name="data_block"
    )

    class Meta:
        verbose_name = "Data Block"
        verbose_name_plural = "Data Block"


class NodeManager(models.Manager):
    def get_initial(self) -> "Node":
        return Node.objects.get(position=0)


class Node(models.Model):
    objects = NodeManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position = models.IntegerField(default=0, unique=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    corruption_value = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Node"
        verbose_name_plural = "Nodes"

    def add_link(self, link: "Link"):
        self.links.add(link)

    @property
    def previous_node(self):
        if self.previous_choice.count() != 0:
            return self.previous_choice.first().node


class Link(models.Model):
    node = models.ForeignKey(
        "Node", on_delete=models.CASCADE, related_name="choices"
    )
    next_node = models.ForeignKey(
        "Node",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="previous_choice",
    )

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"

    def add_text(self, text: str):
        data_block = DataBlock.objects.get_or_create(link=self)
        data_block[0].text = text
        data_block[0].save()

    @property
    def text(self):
        return self.data_block.text


class CorruptionManager(models.Manager):
    def increase(self, value):
        c = Corruption.objects.first()
        proposed_level = c.level + value
        c.level = min(proposed_level, Corruption.MAX_LEVEL)
        c.save()

    def decrease(self, value):
        c = Corruption.objects.first()
        proposed_level = c.level - value
        c.level = max(proposed_level, Corruption.MIN_LEVEL)
        c.save()

    def current_level(self):
        return Corruption.objects.first().level

    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        # bulk_create should just not work on this object,
        # because there can only be be one.
        raise ValidationError(
            "You can't use bulk_create, because there can be only one!"
        )


class Corruption(SingletonModel):
    MIN_LEVEL = 0
    MAX_LEVEL = 10

    objects = CorruptionManager()

    level = models.IntegerField()

    class Meta:
        verbose_name = "Corruption"


class Sound(models.Model):
    title = models.CharField(max_length=150, unique=True)
    file = models.FileField(upload_to="uploads/sounds")

    def delete(self):
        # Yes, if someone has access to the database, they can delete it.
        # I'm not worried about that, I just want to make sure that *I* don't
        # accidentally call `delete()` on the static sound in the shell.
        if self.title == "__static__":
            return
        super().delete()

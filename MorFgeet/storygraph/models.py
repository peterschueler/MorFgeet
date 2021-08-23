import uuid

from django.db import models


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

    class Meta:
        verbose_name = "Node"
        verbose_name_plural = "Nodes"

    def add_link(self, link: "Link"):
        self.links.add(link)


class Link(models.Model):
    node = models.ForeignKey(
        "Node", on_delete=models.CASCADE, related_name="links"
    )
    nextNode = models.ForeignKey(
        "Node", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"

    @property
    def text(self):
        return self.data_block.text

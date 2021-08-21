import uuid

from django.db import models


class DataBlock(models.Model):
    text = models.TextField()
    link = models.ForeignKey("Link", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Data Block"
        verbose_name_plural = "Data Block"


class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Node"
        verbose_name_plural = "Nodes"


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

import factory
from storygraph.models import Link, Node, Sound


class NodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Node


class LinkFactory(factory.django.DjangoModelFactory):
    node = factory.SubFactory(NodeFactory)

    class Meta:
        model = Link


class SoundFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sound

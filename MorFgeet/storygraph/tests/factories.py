import factory
from storygraph.models import Sound


class SoundFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sound

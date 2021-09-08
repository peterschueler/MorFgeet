import pytest
from django.core.exceptions import ValidationError
from storygraph.models import Corruption, DataBlock, Sound
from storygraph.tests.factories import LinkFactory, SoundFactory


@pytest.mark.django_db
def test__link_add_text():
    link = LinkFactory()
    text = "We have to get back, Kate!"

    assert DataBlock.objects.count() == 0

    link.add_text(text)

    assert DataBlock.objects.count() == 1
    assert DataBlock.objects.first().link == link
    assert DataBlock.objects.first().text == text


@pytest.mark.parametrize(
    "proposed_increase, expected_level", [(5, 6), (108, 10)]
)
@pytest.mark.django_db
def test__increase_corruption(proposed_increase, expected_level):
    Corruption.objects.create(level=1)

    # sanity check
    assert Corruption.objects.current_level() == 1

    Corruption.objects.increase(proposed_increase)

    assert Corruption.objects.current_level() == expected_level


@pytest.mark.parametrize(
    "proposed_decrease, expected_level", [(5, 5), (108, 0)]
)
@pytest.mark.django_db
def test__decrease_corruption(proposed_decrease, expected_level):
    Corruption.objects.create(level=10)

    # sanity check
    assert Corruption.objects.current_level() == 10

    Corruption.objects.decrease(proposed_decrease)

    assert Corruption.objects.current_level() == expected_level


@pytest.mark.django_db
def test__single_corruption():
    """
    Ensure that there is only one corruption level for the entire story.
    """
    c = Corruption.objects.create(level=1)

    assert c.id == 1
    assert c.level == 1
    assert Corruption.objects.count() == 1

    c = Corruption.objects.create(level=5)
    assert c.id == 1
    assert c.level == 5
    assert Corruption.objects.count() == 1

    with pytest.raises(ValidationError):
        Corruption.objects.bulk_create(
            [Corruption(level=7), Corruption(level=67), Corruption(level=8)]
        )

    assert Corruption.objects.count() == 1


@pytest.mark.django_db
def test__sound_static_is_undeletable():
    """
    Ensure that the static sound exists and is undeleteable
    """
    sound_01 = Sound.objects.get_or_create(title="__static__")[0]
    assert Sound.objects.count() == 1

    sound_01.delete()

    assert Sound.objects.first().title == "__static__"
    assert Sound.objects.count() == 1

    sound_02 = SoundFactory(title="whatever")

    assert Sound.objects.count() == 2

    sound_02.delete()

    assert Sound.objects.count() == 1

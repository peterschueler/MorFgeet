import pytest
from storygraph.importer import import_story
from storygraph.models import Link, Node


@pytest.mark.parametrize(
    "node, link",
    [
        (
            [("this is a text", "node", "04", "", "", "")],
            [("link me up", "link", "", "04", "", "")],
        ),
        (
            [("this is another text", "node", "08", "", "", "5")],
            [("link me up", "link", "", "08", "", "")],
        ),
    ],
)
@pytest.mark.django_db
def test__import_story_with_valid_input(node, link):
    assert Node.objects.count() == 0
    assert Link.objects.count() == 0

    import_story(node, link)

    assert Node.objects.count() == 1
    assert Node.objects.first().body == node[0][0]
    assert Node.objects.first().position == int(node[0][2])
    assert Node.objects.first().corruption_value == 0 or int(node[0][5])

    assert Link.objects.count() == 1
    assert Link.objects.first().text == link[0][0]
    assert Link.objects.first().node == Node.objects.first()

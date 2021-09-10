import csv
from pathlib import Path

from storygraph.models import DataBlock, Link, Node

from MorFgeet.settings import MEDIA_ROOT


def parse_story(name: str) -> tuple[list[str], list[str]]:
    """
    Iterate over outline to create graph
    this is a very simple, naive implementation.
    Definitely room for improvement here!
    """

    # check media directory for outline with story
    story_path = Path(MEDIA_ROOT).joinpath(name)
    if not story_path.exists():
        return "Oh boy, no story found!"

    with open(story_path, "r") as story_file:
        data_reader = csv.reader(story_file)
        nodes = []
        links = []
        for row in data_reader:
            if row[1] == "node":
                nodes.append(row)
            elif row[1] == "link":
                links.append(row)

    return (nodes, links)


def import_story(nodes, links):
    for row in nodes:
        node = Node.objects.create(body=row[0], position=int(row[2]))
        if row[5] != "" and row[5] is not None:
            node.corruption_value = int(row[5])
            node.save()
        if row[6] != "" and row[6] is not None:
            node.title = row[6]
            node.save()

    for row in links:
        node = Node.objects.get(position=int(row[3]))
        link = Link.objects.create(node=node)
        if row[4] != "" and row[4] is not None:
            next_node = Node.objects.get(position=row[4])
            link.next_node = next_node
        link.add_text(row[0])

        link.save()

import random

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from storygraph.models import Corruption, Node, Sound


def main_view(request):
    node = Node.objects.get_initial()
    Corruption.objects.update(level=0)

    context = {"node": node}

    return render(request, "storygraph/main.html", context)


def node_display(request, id):
    try:
        node = Node.objects.get(id=id)
    except Node.DoesNotExist:
        context = {"errors": f"Can't find Node object with id {id}"}
        return render(request, "errors/dead_end.html", context)

    try:
        sound = Sound.objects.get(title=node.title)
    except Sound.DoesNotExist:
        sound = Sound.objects.get(title="__static__")

    context = {
        "node": node,
        "sound": sound,
        "global_corruption": Corruption.objects.current_level(),
    }

    template = "storygraph/node.html"

    if node.position == 99:
        template = "storygraph/the_end.html"

    return render(request, template, context)


def get_random_node(request, current_node):
    Corruption.objects.increase(1)
    node = Node.objects.get(id=current_node)
    node_list = Node.objects.filter(
        Q(position__lte=node.position) & ~Q(choices=None)
    )
    random_node = random.choice(node_list)
    return HttpResponseRedirect(random_node.get_absolute_url())

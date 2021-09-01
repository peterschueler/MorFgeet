from django.shortcuts import render
from storygraph.models import Node, Sound


def main_view(request):
    node = Node.objects.get_initial()

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
        # TODO: make sure this *always* exists!
        sound = Sound.objects.get(title="__static__")

    context = {"node": node, "sound": sound}

    return render(request, "storygraph/node.html", context)

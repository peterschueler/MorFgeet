from django.shortcuts import render
from storygraph.models import Node


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

    context = {"node": node}

    return render(request, "storygraph/node.html", context)

from django.shortcuts import render
from webservice.models import User, Site, Cluster, Host, Software, Script, Event
from webservice.serializers import UserSerializer, SiteSerializer, ClusterSerializer, HostSerializer, SoftwareSerializer, ScriptSerializer, EventSerializer

from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response


def index(request):
    clusters = Cluster.objects.all()
    return render(request, "index.html", {"clusters": clusters})


# Methods related to User
@api_view(['GET', 'POST'])
@csrf_exempt
def user_list(request):
    """
    List all users, or create a new user.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        for result in serializer.data:
            result["password"] = "*" * len(result["password"])
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def user_detail(request, pk):
    """
    Retrieve, update or delete an user.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        user.password = "*" * len(user.password)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            user.password = "*" * len(user.password)
            serializer = UserSerializer(user, data=data)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)


# Methods related to Site
@api_view(['GET', 'POST'])
@csrf_exempt
def site_list(request):
    """
    List all code snippets, or create a new site.
    """
    if request.method == 'GET':
        sites = Site.objects.all()
        serializer = SiteSerializer(sites, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SiteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def site_detail(request, pk):
    """
    Retrieve, update or delete a site.
    """
    try:
        site = Site.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SiteSerializer(site)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SiteSerializer(site, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        site.delete()
        return HttpResponse(status=204)


# Methods related to Cluster
@api_view(['GET', 'POST'])
@csrf_exempt
def cluster_list(request):
    """
    List all clusters, or create a new cluster.
    """
    if request.method == 'GET':
        clusters = Cluster.objects.all()
        serializer = ClusterSerializer(clusters, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        required_fields = ["site_id", "software_id", "user_id", "name"]
        missing_fields = []

        for required_field in required_fields:
            if required_field not in data:
                missing_fields += [required_field]

        if len(missing_fields) == 0:
            from webservice import models
            cluster = models.Cluster()
            for field in data:
                setattr(cluster, field, data[field])
            cluster.save()
            return Response({"cluster_id": cluster.id}, status=201)

        return Response({"missing_fields": missing_fields}, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def cluster_detail(request, pk):
    """
    Retrieve, update or delete a cluster.
    """
    try:
        cluster = Cluster.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ClusterSerializer(cluster)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ClusterSerializer(cluster, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        cluster.delete()
        return HttpResponse(status=204)


# Methods related to Host
@api_view(['GET', 'POST'])
@csrf_exempt
def host_list(request):
    """
    List all code snippets, or create a new host.
    """
    if request.method == 'GET':
        hosts = Host.objects.all()
        serializer = HostSerializer(hosts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        from core.mister_cluster import MisterCluster
        data = JSONParser().parse(request)
        required_fields = ["cluster_id"]
        missing_fields = []

        for required_field in required_fields:
            if required_field not in data:
                missing_fields += [required_field]

        if len(missing_fields) == 0:
            from webservice import models
            host = models.Host()
            for field in data:
                setattr(host, field, data[field])
            host.save()
            mister_cluster = MisterCluster()
            # cluster_id = data["cluster_id"]
            mister_cluster.add_node_to_cluster(host)
            return Response({"host_id": host.id}, status=201)

        return Response({"missing_fields": missing_fields}, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def host_detail(request, pk):
    """
    Retrieve, update or delete an host.
    """
    try:
        host = Host.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = HostSerializer(host)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = HostSerializer(host, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        host.delete()
        return HttpResponse(status=204)


# Methods related to Software
@api_view(['GET', 'POST'])
@csrf_exempt
def software_list(request):
    """
    List all softwares, or create a new software.
    """
    if request.method == 'GET':
        softwares = Software.objects.all()
        serializer = SoftwareSerializer(softwares, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SoftwareSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def software_detail(request, pk):
    """
    Retrieve, update or delete a software.
    """
    try:
        software = Software.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SoftwareSerializer(software)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SoftwareSerializer(software, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        software.delete()
        return HttpResponse(status=204)


# Methods related to Script
@api_view(['GET', 'POST'])
@csrf_exempt
def script_list(request):
    """
    List all code snippets, or create a new script.
    """
    if request.method == 'GET':
        scripts = Script.objects.all()
        serializer = ScriptSerializer(scripts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ScriptSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def script_detail(request, pk):
    """
    Retrieve, update or delete a script.
    """
    try:
        script = Script.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ScriptSerializer(script)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ScriptSerializer(script, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        script.delete()
        return HttpResponse(status=204)


# Methods related to Script
@api_view(['GET', 'POST'])
@csrf_exempt
def event_list(request):
    """
    List all events, or create a new event.
    """
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def event_detail(request, pk):
    """
    Retrieve, update or delete an event.
    """
    try:
        event = Event.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EventSerializer(event, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        event.delete()
        return HttpResponse(status=204)

if len(Cluster.objects.all()) == 0 and len(User.objects.all()) == 0:
    from webservice.fixtures import create_infrastructure
    create_infrastructure()
from django.shortcuts import render
from webservice.models import File, Job
from webservice.serializers import FileSerializer, JobSerializer

from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.mister_hadoop import MisterHadoop
from core.mister_fs import MisterFs
from core.mister_hdfs import MisterHdfs

from django.utils.encoding import smart_str


def index(request):
    files = File.objects.all()
    return render(request, "index.html", {"files": files})


mister_hadoop = MisterHadoop()
mister_fs = MisterFs()
mister_hdfs = MisterHdfs()

# Methods related to File
@api_view(['GET', 'POST'])
@csrf_exempt
def file_list(request):
    """
    List all files, or create a new file.
    """
    if request.method == 'GET':
        users = File.objects.all()
        serializer = FileSerializer(users, many=True)
        # for result in serializer.data:
        #     result["password"] = "*" * len(result["password"])
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = FileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
@csrf_exempt
def set_file_content(request, pk):
    if request.method == 'POST':
        # Read content of the file
        file_content = request.data['data'].read()
        # Find the DB file
        file = File.objects.filter(id=pk).first()
        # Update the local file
        mister_fs.create_file(file.local_file_path, file_content)
        return Response({"status": "ok"}, status=201)


@api_view(['POST'])
@csrf_exempt
def put_local_file_to_hdfs(request, pk, hn):
    if request.method == 'POST' or True:
        # Find the DB file
        file = File.objects.filter(id=pk).first()
        file.hdfs_name = hn
        file.save()
        # Put the file on HDFS
        mister_hadoop.add_local_file_to_hdfs(file.hdfs_name, file.local_file_path)
        return Response({"status": "ok"}, status=201)


@api_view(['GET'])
@csrf_exempt
def pull_from_hdfs(request, pk):
    if request.method == 'GET' or True:
        # Find the DB file
        file = File.objects.filter(id=pk).first()
        # Pull from HDFS to local_path
        mister_hadoop.collect_file_from_hdfs(file.hdfs_name, file.local_file_path)
        return Response({"status": "ok"}, status=201)


@api_view(['GET'])
@csrf_exempt
def download_file(request, pk):
    if request.method == 'GET' or True:
        # Find the DB file
        file = File.objects.filter(id=pk).first()
        data = mister_fs.load_file(file.local_file_path)
        response = HttpResponse(data)
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file.name)
        response['X-Sendfile'] = smart_str(file.local_file_path)
        return response


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def file_detail(request, pk):
    """
    Retrieve, update or delete an user.
    """
    try:
        file = File.objects.get(pk=pk)
    except File.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        file.password = "*" * len(file.password)
        serializer = FileSerializer(file)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = FileSerializer(file, data=data)
        if serializer.is_valid():
            serializer.save()
            # user.password = "*" * len(user.password)
            serializer = FileSerializer(file, data=data)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        file.delete()
        return HttpResponse(status=204)


# Methods related to Jobs
@api_view(['GET', 'POST'])
@csrf_exempt
def job_list(request):
    """
    List all code snippets, or create a new site.
    """
    if request.method == 'GET':
        sites = Job.objects.all()
        serializer = JobSerializer(sites, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = JobSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def job_detail(request, pk):
    """
    Retrieve, update or delete a site.
    """
    try:
        site = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = JobSerializer(site)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = JobSerializer(site, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        site.delete()
        return HttpResponse(status=204)


@api_view(['GET', 'DELETE'])
@csrf_exempt
def hdfs_file_detail(request, path=None):
    """
    Retrieve, update or delete an HDFS file.
    """

    if path is None:
        path = ""

    if request.method == 'GET':
        files = mister_hdfs.list_files(path)["FileStatuses"]["FileStatus"]
        if len(files) == 1:
            filename = path.split("/")[-1]
            files[0]["pathSuffix"] = filename
        return Response(files)

    if request.method == 'DELETE':
        files = mister_hdfs.delete_file(path)
        return Response(files)

    elif request.method == 'DELETE':
        file.delete()
        return HttpResponse(status=204)


@api_view(['GET'])
@csrf_exempt
def create_hdfs_folder(request, path):
    """
    Create an HDFS folder.
    """

    if request.method == 'GET':
        mister_hadoop.create_hdfs_folder(path)
        return Response({"status": "ok"})


@api_view(['GET'])
@csrf_exempt
def download_hdfs_file(request, hdfspath):
    """
    Retrieve, update or delete an user.
    """

    if request.method == 'GET':
        import uuid
        random_filename = str(uuid.uuid4())
        filename = hdfspath.split("/")[-1]

        mister_hadoop.collect_file_from_hdfs(hdfspath, random_filename)

        data = mister_fs.load_file(random_filename)
        response = HttpResponse(data)
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
        response['X-Sendfile'] = smart_str(random_filename)
        return response

        return mister_hdfs.list_files(hdfspath)


@api_view(['POST'])
@csrf_exempt
def upload_hdfs_file(request, hdfspath):
    """
    Retrieve, update or delete an user.
    """

    if request.method == 'POST':

        # Read content of the file
        file_content = request.data['data'].read()
        import uuid
        tmp_filename = str(uuid.uuid4())
        # Update the local file
        mister_fs.create_file(tmp_filename, file_content)

        # Put the file on HDFS
        mister_hadoop.add_local_file_to_hdfs(file.hdfs_name, tmp_filename)
        return Response({"status": "ok"}, status=201)


@api_view(['GET'])
@csrf_exempt
def run_hadoop_job(request, pk):
    if request.method == 'GET' or True:
        # Find the Hadoop job
        job = Job.objects.filter(id=pk).first()
        # Get the corresponding file
        jar_path = job.file.local_file_path

        mister_hadoop.run_job(jar_path, job.parameters)

        return Response({"status": "ok"}, status=200)


if len(File.objects.all()) == 0 and len(Job.objects.all()) == 0:
    from webservice.fixtures import create_data
    create_data()

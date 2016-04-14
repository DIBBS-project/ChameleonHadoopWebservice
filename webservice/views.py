from django.shortcuts import render
from webservice.models import File, Job
from webservice.serializers import JobSerializer

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


##############################
# FS
##############################


@api_view(['GET', 'DELETE'])
@csrf_exempt
def fs_file_detail(request, path=None):
    """
    Retrieve, update or delete an HDFS file.
    """

    if path is None:
        path = ""

    if request.method == 'GET':
        response = mister_fs.list_files(path)
        # files = response["FileStatuses"]["FileStatus"] if len(response) > 0 else []
        # if len(files) == 1:
        #     filename = path.split("/")[-1]
        #     files[0]["pathSuffix"] = filename
        files = response
        return Response(files)

    if request.method == 'DELETE':
        files = mister_fs.delete_file(path)
        return Response(files)


@api_view(['GET'])
@csrf_exempt
def fs_delete_file(request, path):
    """
    Delete an FS file.
    """

    if request.method == 'GET':
        status = mister_fs.delete_file(path)
        return Response(status)


@api_view(['GET'])
@csrf_exempt
def fs_delete_folder(request, path):
    """
    Delete an HDFS folder.
    """

    if request.method == 'GET':
        status = mister_fs.delete_file(path, is_folder=True)
        return Response(status)


@api_view(['GET'])
@csrf_exempt
def create_fs_folder(request, path):
    """
    Create an FS folder.
    """

    if request.method == 'GET':
        status = mister_fs.create_folder(path)
        return Response(status)


@api_view(['GET'])
@csrf_exempt
def download_fs_file(request, path):
    """
    Download a FS file
    """

    if request.method == 'GET':
        filename = path.split("/")[-1]
        data = mister_fs.load_file(filename)
        response = HttpResponse(data)
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(path)
        response['X-Sendfile'] = smart_str(filename)
        return response

        return mister_hdfs.list_files(path)


@api_view(['POST'])
@csrf_exempt
def upload_fs_file(request, path):
    """
    Retrieve, update or delete an user.
    """

    if request.method == 'POST':
        filename = path.split("/")[-1]

        # Read content of the file
        file_content = request.data['data'].read()
        # import uuid
        # tmp_filename = str(uuid.uuid4())
        # Update the local file
        mister_fs.create_file(path, file_content)

        # Put the file on FS
        mister_hadoop.add_local_file_to_hdfs(path, filename)
        return Response({"status": "ok"}, status=201)


##############################
# HDFS
##############################


@api_view(['GET', 'DELETE'])
@csrf_exempt
def hdfs_file_detail(request, path=None):
    """
    Retrieve, update or delete an HDFS file.
    """

    if path is None:
        path = ""

    if request.method == 'GET':
        response = mister_hdfs.list_files(path)
        files = response["FileStatuses"]["FileStatus"] if len(response) > 0 else []
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
def hdfs_delete_file(request, path):
    """
    Delete an HDFS file.
    """

    if request.method == 'GET':
        files = mister_hdfs.delete_file(path)
        return Response(files)


@api_view(['GET'])
@csrf_exempt
def hdfs_delete_folder(request, path):
    """
    Delete an HDFS folder.
    """

    if request.method == 'GET':
        files = mister_hdfs.delete_file(path, is_folder=True)
        return Response(files)


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
        mister_hadoop.add_local_file_to_hdfs(hdfspath, tmp_filename)
        return Response({"status": "ok"}, status=201)


@api_view(['GET'])
@csrf_exempt
def run_hadoop_job(request, pk):
    if request.method == 'GET' or True:
        # Find the Hadoop job
        job = Job.objects.filter(id=pk).first()
        mister_hadoop.run_job(job.command)

        return Response({"status": "ok"}, status=200)


@api_view(['GET'])
@csrf_exempt
def get_running_jobs(request):
    """
    Get runnin hadoop jobs.
    """

    if request.method == 'GET':
        response = mister_hadoop.get_running_jobs()
        jobs = response["apps"]["app"] if len(response) > 0 else []
        return Response(jobs)


if len(File.objects.all()) == 0 and len(Job.objects.all()) == 0:
    from webservice.fixtures import create_data
    create_data()

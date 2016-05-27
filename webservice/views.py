from django.shortcuts import render
from webservice.models import Job, Execution, Token
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


from rest_framework import exceptions

from functools import wraps

import logging


def expect_username(view_func):
    """Check that the user has provided a username.
    """

    def wrapped_view(*args, **kwargs):
        if len(args) < 1:
            raise Exception("No request was provided :(")
        request = args[0]
        username = None
        # check if api_token is included in URL
        if "username" in request.query_params:
            username = str(request.query_params["username"])
        # check if api_token in included in request's META field
        if "HTTP_USERNAME" in request.META:
            username = request.META.get('HTTP_USERNAME')
        if username is None:
            raise exceptions.AuthenticationFailed('No USER has been provided')
        # Set an "api_token" field to ease its usage by view methods
        request.username = username
        return view_func(*args, **kwargs)

    return wraps(view_func)(wrapped_view)


def expect_apitoken(view_func):
    """Check that the user has provided an api token.
    """

    def wrapped_view(*args, **kwargs):
        if len(args) < 1:
            raise Exception("No request was provided :(")
        request = args[0]
        token = None
        # check if api_token is included in URL
        if "token" in request.query_params:
            token = str(request.query_params["token"])
        # check if api_token in included in request's META field
        if "HTTP_TOKEN" in request.META:
            token = request.META.get('HTTP_TOKEN')
        if token is None:
            raise exceptions.AuthenticationFailed('No TOKEN has been provided')
        # Set an "api_token" field to ease its usage by view methods
        request.token = token
        return view_func(*args, **kwargs)

    return wraps(view_func)(wrapped_view)


def expect_password(view_func):
    """Check that the user has provided a password.
    """

    def wrapped_view(*args, **kwargs):
        if len(args) < 1:
            raise Exception("No request was provided :(")
        request = args[0]
        password = None
        # check if api_token is included in URL
        if "password" in request.query_params:
            password = str(request.query_params["password"])
        # check if api_token in included in request's META field
        if "HTTP_PASSWORD" in request.META:
            password = request.META.get('HTTP_PASSWORD')
        if password is None:
            raise exceptions.AuthenticationFailed('No PASSWORD has been provided')
        # Set an "api_token" field to ease its usage by view methods
        request.password = password
        return view_func(*args, **kwargs)

    return wraps(view_func)(wrapped_view)


def token_authentication(view_func):
    """Check that a valid token has been provided.
    """

    def wrapped_view(*args, **kwargs):
        if len(args) < 1:
            raise Exception("No request was provided :(")
        request = args[0]
        if not hasattr(request, "token"):
            raise exceptions.AuthenticationFailed('no token has been provided :(')
        token = request.token
        tokens = Token.objects.filter(token=token).all()
        if len(tokens) == 0:
            raise exceptions.AuthenticationFailed('token not valid :(')
        request.username = tokens[0].username
        return view_func(*args, **kwargs)

    return wraps(view_func)(wrapped_view)


def user_authentication(view_func):
    """Check that a valid user has been provided.
    """

    def wrapped_view(*args, **kwargs):
        if len(args) < 1:
            raise Exception("No request was provided :(")
        request = args[0]
        if not hasattr(request, "username") or not hasattr(request, "password"):
            raise exceptions.AuthenticationFailed('need a username and a password :(')
        username = request.username
        password = request.password
        from django.contrib.auth.models import User
        users = User.objects.filter(username=username).all()
        if len(users) == 0:
            raise exceptions.AuthenticationFailed('user not valid :(')
        user = User.objects.filter(username=username).first()
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('user not valid :(')
        return view_func(*args, **kwargs)

    return wraps(view_func)(wrapped_view)


def index(request):
    files = []
    return render(request, "index.html", {"files": files})


mister_hadoop = MisterHadoop()
mister_fs = MisterFs()
mister_hdfs = MisterHdfs()

# Get an instance of a logger
logger = logging.getLogger(__name__)


##############################
# User management
##############################


@api_view(['POST'])
@csrf_exempt
def register_new_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    logger.debug("will create user (%s, %s)" % (username, password))

    from django.contrib.auth.models import User
    try:
        user = User.objects.create_user(username=username, password=password)
        user.save()
    except:
        return Response({"status": "failed"})

    return Response({"status": "ok"})


@api_view(['GET'])
@expect_username
@expect_password
@user_authentication
@csrf_exempt
def generate_new_token(request):
    import uuid
    from django.contrib.auth.models import User

    try:
        user = User.objects.filter(username=request.username).first()

        token = Token()
        token.token = uuid.uuid4()
        token.username = request.username
        token.user_id = user.id
        token.save()

        return Response({"status": "ok", "token": token.token})
    except:
        return Response({"status": "failed"})


##############################
# Hadoop
##############################


@api_view(['GET', 'POST'])
@expect_apitoken
@token_authentication
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
@expect_apitoken
@token_authentication
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


@api_view(['GET'])
@expect_apitoken
@token_authentication
@csrf_exempt
def run_hadoop_job(request, pk):
    if request.method == 'GET' or True:
        # Find the Hadoop job
        job = Job.objects.filter(id=pk).first()
        response = mister_hadoop.run_job(job.command, request.username)
        execution = Execution()
        execution.job = job
        execution.application_hadoop_id = response["application_hadoop_id"]
        execution.save()

        if job.callback_url:
            mister_hadoop.watch_for_end_jobs_and_callback(execution.application_hadoop_id, job.callback_url)

        return Response(
            {"status": "ok",
             "application_hadoop_id": execution.application_hadoop_id},
            status=200)


@api_view(['GET'])
@expect_apitoken
@token_authentication
@csrf_exempt
def get_running_jobs(request):
    """
    Get runnin hadoop jobs.
    """

    if request.method == 'GET':
        jobs = mister_hadoop.get_running_jobs()
        return Response(jobs)


##############################
# FS
##############################


@api_view(['GET', 'DELETE'])
@expect_apitoken
@token_authentication
@csrf_exempt
def fs_file_detail(request, path=None):
    """
    Retrieve, update or delete an HDFS file.
    """

    # By default, a non-set path refers to the root path
    if path is None:
        path = ""

    if request.method == 'GET':
        response = mister_fs.list_files(path)
        files = response
        return Response(files)

    if request.method == 'DELETE':
        files = mister_fs.delete_file(path)
        return Response(files)


@api_view(['GET'])
@expect_apitoken
@token_authentication
@csrf_exempt
def fs_delete_file(request, path):
    """
    Delete an FS file.
    """

    if request.method == 'GET':
        status = mister_fs.delete_file(path)
        return Response(status)


@api_view(['GET'])
@expect_apitoken
@token_authentication
@csrf_exempt
def fs_delete_folder(request, path):
    """
    Delete an HDFS folder.
    """

    if request.method == 'GET':
        status = mister_fs.delete_file(path, is_folder=True)
        return Response(status)


@api_view(['GET'])
@expect_apitoken
@token_authentication
@csrf_exempt
def create_fs_folder(request, path):
    """
    Create an FS folder.
    """

    if request.method == 'GET':
        status = mister_fs.create_folder(path)
        return Response(status)


@api_view(['GET'])
@expect_apitoken
@token_authentication
@csrf_exempt
def download_fs_file(request, path):
    """
    Download a FS file
    """

    if request.method == 'GET':
        filename = path.split("/")[-1]
        data = mister_fs.load_file(filename)
        response = HttpResponse(data)
        response[
            'Content-Disposition'] = 'attachment; filename=%s' % smart_str(
                path)
        response['X-Sendfile'] = smart_str(filename)
        return response

        return mister_hdfs.list_files(path)


@api_view(['POST'])
@expect_apitoken
@token_authentication
@csrf_exempt
def upload_fs_file(request, path):
    """
    Retrieve, update or delete an user.
    """

    if request.method == 'POST':
        filename = path.split("/")[-1]

        # Read content of the file
        file_content = request.data['data'].read()
        mister_fs.create_file(path, file_content)

        # Put the file on FS
        mister_hadoop.add_local_file_to_hdfs(path, filename, request.username)
        return Response({"status": "ok"}, status=201)


##############################
# HDFS
##############################


@api_view(['GET', 'DELETE'])
@expect_apitoken
@token_authentication
@csrf_exempt
def hdfs_file_detail(request, path=None):
    """
    Retrieve, update or delete an HDFS file.
    """

    # By default, a non-set path refers to the root path
    if path is None:
        path = ""

    if request.method == 'GET':
        response = mister_hdfs.list_files(path)

        # Check if the path contains anything
        if not "FileStatuses" in response:
            return Response(
                {"result": "error",
                 "type": "hdfs_error",
                 "msg": "file '/%s' does not exists" % (path)},
                status=404)

        # Check if the results contains files
        files = response["FileStatuses"]["FileStatus"] if len(
            response) > 0 else []

        # Send the response
        return Response(files)

    if request.method == 'DELETE':
        files = mister_hdfs.delete_file(path)
        return Response(files)

    elif request.method == 'DELETE':
        file.delete()
        return HttpResponse(status=204)


@api_view(['GET'])
@expect_apitoken
@token_authentication
@csrf_exempt
def hdfs_delete_file(request, path):
    """
    Delete an HDFS file.
    """

    if request.method == 'GET':
        files = mister_hdfs.delete_file(path)
        return Response(files)


@api_view(['GET'])
@expect_apitoken
@token_authentication
@csrf_exempt
def hdfs_delete_folder(request, path):
    """
    Delete an HDFS folder.
    """

    if request.method == 'GET':
        files = mister_hdfs.delete_file(path, is_folder=True)
        return Response(files)


@api_view(['GET'])
@expect_apitoken
@token_authentication
@csrf_exempt
def create_hdfs_folder(request, path):
    """
    Create an HDFS folder.
    """

    if request.method == 'GET':
        mister_hadoop.create_hdfs_folder(path, request.username)
        return Response({"status": "ok"})


@api_view(['GET'])
@expect_apitoken
@token_authentication
@csrf_exempt
def download_hdfs_file(request, hdfspath):
    """
    Download an HDFS file.
    """

    if request.method == 'GET':
        import uuid
        random_filename = str(uuid.uuid4())
        filename = hdfspath.split("/")[-1]

        mister_hadoop.collect_file_from_hdfs(hdfspath, random_filename)

        data = mister_fs.load_file(random_filename)
        response = HttpResponse(data)
        response[
            'Content-Disposition'] = 'attachment; filename=%s' % smart_str(
                filename)
        response['X-Sendfile'] = smart_str(random_filename)
        return response

        return mister_hdfs.list_files(hdfspath)


@api_view(['POST'])
@expect_apitoken
@token_authentication
@csrf_exempt
def upload_hdfs_file(request, hdfspath):
    """
    Upload an HDFS file.
    """

    if request.method == 'POST':

        # Read content of the file
        file_content = request.data['data'].read()
        import uuid
        tmp_filename = str(uuid.uuid4())
        # Update the local file
        mister_fs.create_file(tmp_filename, file_content)

        # Put the file on HDFS
        mister_hadoop.add_local_file_to_hdfs(hdfspath, tmp_filename, request.username)
        return Response({"status": "ok"}, status=201)


@api_view(['GET'])
@expect_apitoken
@token_authentication
@csrf_exempt
def hdfs_copy_to_local(request, hdfspath, localpath):
    """
    Copy an HDFS file to a local path.
    """

    if request.method == 'GET':
        try:
            mister_hadoop.collect_file_from_hdfs(hdfspath, localpath, request.username)
        except:
            return Response({"status": "bad"}, status=404)

        return Response({"status": "ok"}, status=201)


@api_view(['GET'])
@expect_apitoken
@token_authentication
@csrf_exempt
def hdfs_merge_directory(request, hdfspath, localpath):
    """
    Merge files of an HDFS folder into a single local file.
    """

    if request.method == 'GET':
        try:
            mister_hdfs.merge_directory(hdfspath, localpath, request.username)
        except Exception as e:
            print(e)
            return Response({"status": "bad"}, status=404)

        return Response({"status": "ok"}, status=201)

#!/usr/bin/env python

import logging
import os
import pycurl
import json
from io import BytesIO
import uuid

logging.basicConfig(level=logging.INFO)
import subprocess
from subprocess import check_output

parameters = {}
from jinja2 import Environment, FileSystemLoader

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, '../templates')),
    trim_blocks=False)

client = None


def generate_template(input_file, context):
    output = TEMPLATE_ENVIRONMENT.get_template(input_file).render(context)
    return output


def generate_template_file(input_file, output_file, context):
    output = generate_template(input_file, context)
    with open(output_file, "w") as f:
        f.write(output)
    return True


def call_rest(url, method="GET"):
    """ Inspired by:
    http://stackoverflow.com/questions/15453608/extract-data-from-a-dictionary-returned-by-pycurl
    """
    c = pycurl.Curl()
    data = BytesIO()

    if method == "GET":
        c.setopt(c.HTTPGET, 1)
    elif method == "POST":
        c.setopt(c.HTTPPOST, 1)
    elif method == "PUT":
        c.setopt(c.HTTPPUT, 1)
    elif method == "DELETE":
        c.setopt(pycurl.CUSTOMREQUEST, "DELETE")
    elif method == "PATCH":
        c.setopt(c.HTTPPATCH, 1)

    print("c.setopt(c.URL, %s)" % (url))

    c.setopt(c.URL, str(url))
    c.setopt(c.WRITEFUNCTION, data.write)
    c.perform()

    return json.loads(data.getvalue())


class MisterHadoop:

    def __init__(self, parameters=None):
        self.server_ip = "127.0.0.1"
        self.url_postfix = "http://%s:8088/ws/v1" % (self.server_ip)

    def call_whdfs(self, action, http_method):
        return call_rest("%s/%s" % (self.url_postfix, action), http_method)

    def add_local_file_to_hdfs(self, hdfs_path, local_path):
        input_file = "hadoop/add_local_file_to_hdfs.sh.jinja2"
        output_file = "tmp/add_local_file_to_hdfs.sh"
        context = {
            "hdfs_path": hdfs_path,
            "local_path": local_path
        }
        generate_template_file(input_file, output_file, context)
        subprocess.call("bash %s" % (output_file), shell=True)
        pass

    def create_hdfs_folder(self, hdfs_path):
        input_file = "hadoop/create_hdfs_folder.sh.jinja2"
        output_file = "tmp/create_hdfs_folder.sh"
        context = {
            "hdfs_path": hdfs_path
        }
        generate_template_file(input_file, output_file, context)
        subprocess.call("bash %s" % (output_file), shell=True)
        pass

    def run_job(self, command):
        input_file = "hadoop/run_job.sh.jinja2"
        output_file = "tmp/run_job.sh"

        job_id = uuid.uuid4()
        stdout_file = "tmp/output_%s" % (job_id)

        context = {
            "command": command,
            "suffix": " > %s &" % (stdout_file)
        }
        generate_template_file(input_file, output_file, context)

        subprocess.call("bash %s" % (output_file), shell=True)

        # with open(stdout_file, 'w') as f:
        #     subprocess.Popen(["bash", output_file], stdout=f)

        application_hadoop_id = None
        pattern = "Submitted application"
        while application_hadoop_id is None:
            try:
                out = check_output("grep '%s' %s | sed 's/.*Submitted application //g'" % (pattern, stdout_file))
                if out != "":
                    application_hadoop_id = out
            except:
                pass

        return {"application_hadoop_id": application_hadoop_id}

    def collect_file_from_hdfs(self, hdfs_name, local_path):
        input_file = "hadoop/collect_file_from_hdfs.sh.jinja2"
        output_file = "tmp/collect_file_from_hdfs.sh"
        context = {
            "hdfs_path": hdfs_name,
            "output_file": local_path
        }
        generate_template_file(input_file, output_file, context)
        subprocess.call("bash %s" % (output_file), shell=True)

    def get_running_jobs(self):
        return self.call_whdfs("cluster/apps", "GET")


if __name__ == "__main__":
    pass

#!/usr/bin/env python

import logging
import os
import pycurl
import pprint
import json
from io import BytesIO

logging.basicConfig(level=logging.INFO)

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
        c.setopt(c.HTTPDELETE, 1)
    elif method == "PATCH":
        c.setopt(c.HTTPPATCH, 1)

    print("c.setopt(c.URL, %s)" % (url))

    c.setopt(c.URL, str(url))
    c.setopt(c.WRITEFUNCTION, data.write)
    c.perform()

    return json.loads(data.getvalue())


class MisterHdfs:

    def __init__(self, path=None):
        self.server_ip = "129.114.111.66"
        self.url_postfix = "http://%s:50070/webhdfs/v1" % (self.server_ip)

    def call_whdfs(self, hdfs_path, operation, http_method):
        return call_rest("%s/%s?op=%s" % (self.url_postfix, hdfs_path, operation), http_method)

    def list_files(self, hdfs_path):
        return self.call_whdfs(hdfs_path, "LISTSTATUS", "GET")

    def delete_file(self, hdfs_path, is_folder=False):
        operation = "DELETE"
        if is_folder:
            operation += "&recursive=true"
        return self.call_whdfs(hdfs_path, operation, "DELETE")


if __name__ == "__main__":
    pass

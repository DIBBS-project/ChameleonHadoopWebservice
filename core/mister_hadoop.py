#!/usr/bin/env python

import logging
import os

logging.basicConfig(level=logging.INFO)
import subprocess

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


class MisterHadoop:

    def __init__(self, parameters=None):
        pass

    def add_local_file_to_hdfs(self, hdfs_name, local_path):
        input_file = "hadoop/add_local_file_to_hdfs.sh.jinja2"
        output_file = "tmp/add_local_file_to_hdfs.sh"
        context = {
            "hdfs_name": hdfs_name,
            "local_path": local_path
        }
        generate_template_file(input_file, output_file, context)
        subprocess.call("bash %s" % (output_file), shell=True)
        pass

    def run_job(self, jar_file, parameters):
        input_file = "hadoop/run_job.sh.jinja2"
        output_file = "tmp/run_job.sh"
        context = {
            "jar_file": jar_file,
            "parameters": parameters
        }
        generate_template_file(input_file, output_file, context)
        subprocess.call("bash %s" % (output_file), shell=True)
        pass

    def collect_file_from_hdfs(self, hdfs_name, local_path):
        input_file = "hadoop/collect_file_from_hdfs.sh.jinja2"
        output_file = "tmp/collect_file_from_hdfs.sh"
        context = {
            "hdfs_name": hdfs_name,
            "output_file": output_file
        }
        generate_template_file(input_file, output_file, context)
        subprocess.call("bash %s" % (output_file), shell=True)



        pass

if __name__ == "__main__":
    pass

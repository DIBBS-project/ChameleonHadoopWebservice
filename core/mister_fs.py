#!/usr/bin/env python

import logging
import os

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


class MisterFs:

    def __init__(self, path=None):
        self.path = "tmp" if not path else path
        self._init_folder()
        pass

    def _init_folder(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def list_files(self):
        return os.listdir(self.path)

    def create_file(self, name, data):
        # Delete file if it already exists
        if self.file_exist(name):
            self.delete_file(name)
        # Write data in a new file
        file_path = "%s/%s" % (self.path, name)
        with open(file_path, "a") as f:
            f.write(data)
        return True

    def load_file(self, name):
        file_path = "%s/%s" % (self.path, name)
        with open(file_path, "r") as content_file:
            content = content_file.read()
        return content

    def file_exist(self, name):
        return name in self.list_files()

    def delete_file(self, name):
        file_path = "%s/%s" % (self.path, name)
        os.remove(file_path)
        pass

    def clean_folder(self):
        for name in self.list_files():
            self.delete_file(name)

if __name__ == "__main__":
    fs_manager = MisterFs()
    print(fs_manager.list_files())
    fs_manager.clean_folder()
    print(fs_manager.list_files())
    fs_manager.create_file("toto", "foo")
    fs_manager.create_file("tata", "bar")
    print(fs_manager.list_files())
    for file_name in fs_manager.list_files():
        print(fs_manager.load_file(file_name))

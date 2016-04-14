from rest_framework import serializers
from webservice.models import Job
import uuid


def generate_uuid():
    return "%s" % (uuid.uuid4())


# class FileSerializer(serializers.Serializer):
#     id = serializers.IntegerField(label='ID', read_only=True)
#     name = serializers.CharField(max_length=100, allow_blank=False, default=generate_uuid)
#     hdfs_name = serializers.CharField(max_length=100, allow_blank=False, default=generate_uuid)
#     local_file_path = serializers.CharField(max_length=100, allow_blank=False, default=generate_uuid)
#
#     def create(self, validated_data):
#         """
#         Create and return a new `File` instance, given the validated data.
#         """
#         return File.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `File` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.local_file_path = validated_data.get('local_file_path', instance.local_file_path)
#         instance.hdfs_name = validated_data.get('hdfs_name', instance.hdfs_name)
#
#         return instance


class JobSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(max_length=100, allow_blank=False, default='')
    status = serializers.CharField(max_length=100, allow_blank=False, default='')
    command = serializers.CharField(allow_blank=True, default='')

    def create(self, validated_data):
        """
        Create and return a new `Job` instance, given the validated data.
        """
        return Job.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Job` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)
        instance.parameters = validated_data.get('parameters', instance.status)

        if instance.file_id:
            instance.save()
        return instance

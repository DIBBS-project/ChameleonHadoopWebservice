from rest_framework import serializers
from webservice.models import File, Job
import uuid


class FileSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(max_length=100, allow_blank=False, default="%s" % (uuid.uuid4()))
    hdfs_name = serializers.CharField(max_length=100, allow_blank=False, default="%s" % (uuid.uuid4()))
    local_file_path = serializers.CharField(max_length=100, allow_blank=False, default="%s" % (uuid.uuid4()))

    def create(self, validated_data):
        """
        Create and return a new `File` instance, given the validated data.
        """
        return File.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `File` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.local_file_path = validated_data.get('local_file_path', instance.local_file_path)
        instance.hdfs_name = validated_data.get('hdfs_name', instance.hdfs_name)

        return instance


class JobSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(max_length=100, allow_blank=False, default='')
    # start_date = serializers.DateField()
    file_id = serializers.IntegerField()
    status = serializers.CharField(max_length=100, allow_blank=False, default='')

    def create(self, validated_data):
        """
        Create and return a new `Site` instance, given the validated data.
        """
        return Job.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Site` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        # instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.file_id = validated_data.get('file_id', instance.file_id)
        instance.status = validated_data.get('status', instance.status)

        if instance.file_id:
            instance.save()
        return instance

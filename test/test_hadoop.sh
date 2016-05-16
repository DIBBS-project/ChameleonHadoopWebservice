#!/usr/bin/env bash

set -x

REMOTE_HADOOP_WEBSERVICE_HOST="http://129.114.111.39:8000"

function extract_id {

    RESULT=$(echo $1 | sed 's/.*"id"://g' | sed 's/,.*//g')

    echo "$RESULT"
}

# Clean output file in FS folder to prevent interference between tests
curl -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/fs/rm/output.txt/

# Clean HDFS folder used by this example
curl -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/hdfs/rmdir/user/root/

# Upload local files to the application
curl -i -X POST -F 'data=@test.jar' $REMOTE_HADOOP_WEBSERVICE_HOST/fs/upload/test.jar/

# Copy test.txt to HDFS in the "input" file
curl -i -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/hdfs/mkdir/user/root/
curl -i -X POST -F 'data=@test.txt' $REMOTE_HADOOP_WEBSERVICE_HOST/hdfs/upload/user/root/input/

# Create Hadoop job
CALLBACK_URL="http://requestb.in/139dsv41"
HADOOP_JOB_CREATION_OUTPUT=$(curl -H "Content-Type: application/json" -X POST -d "{\"name\": \"test\", \"command\": \"test.jar input output dummyparameter\", \"callback_url\": \"$CALLBACK_URL\"}" $REMOTE_HADOOP_WEBSERVICE_HOST/jobs/)
HADOOP_JOB_ID=$(extract_id $HADOOP_JOB_CREATION_OUTPUT)

# Run "test.jar" with hadoop
curl -i -X GET  $REMOTE_HADOOP_WEBSERVICE_HOST/run_hadoop_job/$HADOOP_JOB_ID/

sleep 30

# Merge content of the "output" folder located in HDFS: the content will be copied to the "output.txt" file
curl -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/hdfs/mergedir/user/root/output/_/output.txt/

# Download the "output.txt" file
curl -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/fs/download/output.txt/


exit 0

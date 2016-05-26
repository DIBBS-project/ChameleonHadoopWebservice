#!/usr/bin/env bash

set -x

#REMOTE_HADOOP_WEBSERVICE_HOST="http://127.0.0.1:8000"
REMOTE_HADOOP_WEBSERVICE_HOST="http://129.114.111.66:8000"
CALLBACK_URL="http://requestb.in/t9tni2t9"
USER="cc"

function extract_id {

    RESULT=$(echo $1 | sed 's/.*"id"://g' | sed 's/,.*//g')

    echo "$RESULT"
}

# Clean output file in FS folder to prevent interference between tests
curl --header "username: root" -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/fs/rm/output.txt/

# Clean HDFS jar files and folders used by this example
curl --header "username: root" -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/hdfs/rm/test.jar/
curl --header "username: root" -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/hdfs/rmdir/user/root/
curl --header "username: root" -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/hdfs/rmdir/user/$USER/
curl --header "username: root" -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/hdfs/rmdir/user/

# Upload local files to the application
curl --header "username: $USER" -i -X POST -F 'data=@test.jar' $REMOTE_HADOOP_WEBSERVICE_HOST/fs/upload/test.jar/

# Copy test.txt to HDFS in the "input" file
curl --header "username: $USER" -i -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/hdfs/mkdir/user/$USER/
curl --header "username: $USER" -i -X POST -F 'data=@test.txt' $REMOTE_HADOOP_WEBSERVICE_HOST/hdfs/upload/user/$USER/input/

# Create Hadoop job
HADOOP_JOB_CREATION_OUTPUT=$(curl --header "username: jpastor" -H "Content-Type: application/json" -X POST -d "{\"name\": \"test\", \"command\": \"test.jar input output dummyparameter\", \"callback_url\": \"$CALLBACK_URL\"}" $REMOTE_HADOOP_WEBSERVICE_HOST/jobs/)
HADOOP_JOB_ID=$(extract_id $HADOOP_JOB_CREATION_OUTPUT)

# Run "test.jar" with hadoop
curl --header "username: $USER" -i -X GET  $REMOTE_HADOOP_WEBSERVICE_HOST/run_hadoop_job/$HADOOP_JOB_ID/

sleep 30

# Merge content of the "output" folder located in HDFS: the content will be copied to the "output.txt" file
curl --header "username: $USER" -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/hdfs/mergedir/user/$USER/output/_/output.txt/

# Download the "output.txt" file
curl --header "username: $USER" -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/fs/download/output.txt/


exit 0

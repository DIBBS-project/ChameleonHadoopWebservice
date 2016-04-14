#!/usr/bin/env bash

REMOTE_HADOOP_WEBSERVICE_HOST="http://129.114.111.66:8000"

function extract_id {

    RESULT=$(echo $1 | sed 's/.*"id"://g' | sed 's/,.*//g')

    echo "$RESULT"
}

# Clean HDFS folder used by this example
curl -H "Content-Type: application/json" -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/hdfs/rmdir/user/root/

# Upload local files to the application
curl -i -X POST -F 'data=@test.jar' $REMOTE_HADOOP_WEBSERVICE_HOST/fs/upload/test.jar/

# Copy test.txt to HDFS in the "input" file
curl -i -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/hdfs/mkdir/user/root/
curl -i -X POST -F 'data=@test.txt' $REMOTE_HADOOP_WEBSERVICE_HOST/hdfs/upload/user/root/input/

# Create Hadoop job
HADOOP_JOB_CREATION_OUTPUT=$(curl -H "Content-Type: application/json" -X POST -d "{\"name\": \"test\", \"command\": \"test.jar input output dummyparameter\"}" $REMOTE_HADOOP_WEBSERVICE_HOST/jobs/)
HADOOP_JOB_ID=$(extract_id $HADOOP_JOB_CREATION_OUTPUT)

# Run "test.jar" with hadoop
curl -i -X GET  $REMOTE_HADOOP_WEBSERVICE_HOST/run_hadoop_job/$HADOOP_JOB_ID/

sleep 30

# Collect result files: "output" located in HDFS will be copied to the "output.txt" file
curl -H "Content-Type: application/json" -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/hdfs/download/user/root/output/part-r-00000/

exit 0

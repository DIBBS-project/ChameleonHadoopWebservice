#!/usr/bin/env bash

REMOTE_HADOOP_WEBSERVICE_HOST="http://129.114.111.66:8000"

function extract_id {

    RESULT=$(echo $1 | sed 's/.*"id"://g' | sed 's/,.*//g')

    echo "$RESULT"
}

# We clean remote repository
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/1/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/2/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/3/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/4/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/5/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/6/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/7/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/8/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/9/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/10/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/11/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/12/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/13/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/14/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/15/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/16/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/17/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/18/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/19/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/20/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/21/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/22/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/23/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/24/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/25/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/26/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/27/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/28/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/29/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/30/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/31/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/32/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/33/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/34/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/35/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/36/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/37/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/38
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/files/39/


curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/jobs/1/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/jobs/2/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/jobs/3/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/jobs/4/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/jobs/5/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/jobs/6/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/jobs/7/
curl -H "Content-Type: application/json" -X DELETE $REMOTE_HADOOP_WEBSERVICE_HOST/jobs/8/


# Clean HDFS folder used by this example
curl -H "Content-Type: application/json" -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/delete_hdfs_folder/user/root/

# Upload test.jar and input.txt
TEST_JAR_CREATION_OUTPUT=$(curl -H "Content-Type: application/json" -X POST -d '{"name": "test.jar"}' $REMOTE_HADOOP_WEBSERVICE_HOST/files)
TEST_JAR_ID=$(extract_id $TEST_JAR_CREATION_OUTPUT)

TEST_TXT_CREATION_OUTPUT=$(curl -H "Content-Type: application/json" -X POST $REMOTE_HADOOP_WEBSERVICE_HOST/user/root/)
TEST_TXT_ID=$(extract_id $TEST_TXT_CREATION_OUTPUT)

echo $TEST_JAR_ID

# Upload local files to the application
curl -i -X POST -F 'data=@test.jar' $REMOTE_HADOOP_WEBSERVICE_HOST/set_file_content/$TEST_JAR_ID/

# Copy test.txt to HDFS in the "input" file
curl -i -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/create_hdfs_folder/user/root/
curl -i -X POST -F 'data=@test.txt' $REMOTE_HADOOP_WEBSERVICE_HOST/upload_hdfs_file/user/root/input/

# Create Hadoop job
HADOOP_JOB_CREATION_OUTPUT=$(curl -H "Content-Type: application/json" -X POST -d "{\"name\": \"test\", \"file_id\": $TEST_JAR_ID, \"parameters\": \"input output dummyparameter\"}" $REMOTE_HADOOP_WEBSERVICE_HOST/jobs)
HADOOP_JOB_ID=$(extract_id $HADOOP_JOB_CREATION_OUTPUT)
echo "HADOOP_JOB_ID: $HADOOP_JOB_ID"

# Run "test.jar" with hadoop
curl -i -X GET  $REMOTE_HADOOP_WEBSERVICE_HOST/run_hadoop_job/$HADOOP_JOB_ID/

sleep 30

# Collect result files: "output" located in HDFS will be copied to the "output.txt" file
curl -H "Content-Type: application/json" -X GET $REMOTE_HADOOP_WEBSERVICE_HOST/download_hdfs_file/user/root/output/part-r-00000/

exit 0

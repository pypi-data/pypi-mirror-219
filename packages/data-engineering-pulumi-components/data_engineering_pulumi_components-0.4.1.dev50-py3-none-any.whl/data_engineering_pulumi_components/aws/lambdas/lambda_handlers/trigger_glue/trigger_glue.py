import boto3
import os


def handler(event, context):
    print(event)
    glue = boto3.client("glue", region_name=os.environ["JOB_REGION"])
    gluejobname = os.environ["GLUE_JOB_NAME"]

    try:
        runId = glue.start_job_run(
            JobName=gluejobname, Arguments={"--key": event["object"]["key"]}
        )

        status = glue.get_job_run(JobName=gluejobname, RunId=runId["JobRunId"])
        print("Job Status : ", status["JobRun"]["JobRunState"])

    except Exception as e:
        print(e)

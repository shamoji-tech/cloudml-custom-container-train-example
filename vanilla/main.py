import argparse
import sys
import os
import logging
import google.cloud.logging_v2
from google.cloud import storage
from google.cloud.logging_v2.handlers import CloudLoggingHandler
from google.cloud.logging_v2.resource import Resource

def get_args():
    parser = argparse.ArgumentParser(description='カスタムコンテナテスト')
    parser.add_argument('--job-dir', metavar="gs://..", type=str, nargs=1,
                        help='モデル出力するGCSのURI',required=True)
    return parser
    
args = get_args().parse_args()

STORAGE_DIR = args.job_dir[0]
BUCKET_NAME = STORAGE_DIR.split("/")[2]
PREFIX_NAME = "/".join(STORAGE_DIR.split("/")[3:])
PROJECT_ID  = os.environ["PROJECT_ID"]
JOB_ID      = os.environ["CLOUD_ML_JOB_ID"]
print(PROJECT_ID)
#----logging----#

client = google.cloud.logging_v2.Client(project=PROJECT_ID)
handler = CloudLoggingHandler(client,resource=Resource("ml_job", {"task_name":"docker_test","project_id":PROJECT_ID,"job_id":JOB_ID}))
cloud_logger = logging.getLogger('cloudLogger')
cloud_logger.setLevel(logging.INFO)
cloud_logger.addHandler(handler)
cloud_logger.info('this is info message.')


#----logging----#

if PREFIX_NAME[-1]!="/":
    cloud_logger.critical("job_dir is must be end with /.")
    sys.exit("job_dir is must be end with /.")

#----upload----#
gcs = storage.Client()
bucket = gcs.get_bucket(BUCKET_NAME)
blob = bucket.blob(PREFIX_NAME+"tests")
blob.upload_from_filename("/root/tests")

#----GetAPIKey----#
# client = secretmanager.SecretManagerServiceClient()
# key = client.secret_version_path(PROJECT_ID, "docker_API_test", "1")
# value = client.access_secret_version(name=key)
# cloud_logger.info("取り出したKeyがこちら。↓")
# cloud_logger.info(value.payload.data.decode('UTF-8'))

cloud_logger.info("処理は正常に終了しました。")
sys.exit()

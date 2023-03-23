# 설명:
# CloudWatch Logs에 저장된 로그들을 S3로 보내는 Python 코드입니다.
#
# 사용 이유:
# AWS EKS의 ContainerInsights 로그는 오직 'CloudWatch Logs'에만 저장 가능합니다. 즉, S3에 바로 로그를 저장할 수 있는 방법이 없기 때문에
# AWS Lambda를 통하여 CloudWatch Logs에 저장된 로그를 S3에 옮겨 올 수 있도록 Python으로 구현합니다.

import boto3
import os
from pprint import pprint
import time
from datetime import datetime

logs = boto3.client('logs')
ssm = boto3.client('ssm')
now = datatime.now()
nowDate = now.strftime('%Y-%m-%d')

def lambda_handler(event, context):
  extra_args = {}
  log_groups = []
  log_groups_to_export = []
  
  if 'S3_BUCKET' not in os.environ:
    print("Error: S3_BUCKET not defined")
    return
  
  print("--> S3_BUCKET=%s" % os.environ["S3_BUCKET"])
  
  while True:
    response = logs.describe_log_groups(logGroupNamePrefix='/aws/containerinsights/{EKS-Cluster_Name}/application/{K8s-Namespace}', **extra_args)
    print("=====================================")
    print(response)
    print("=====================================")
    log_groups = log_groups + response['logGroups']
    print(log_groups)
    
    if not 'nextToken' in response:
      break
    extra_args['nextToken'] = response['nextToken']
    print(extra_args)
    
  for log_group in log_groups:
    response = logs.list_tags_log_group(logGroupName=log_group['logGroupName'])
    log_group_tags = response['tags']
    
    if 'ExportToS3' in log_group_tags and log_group_tags['ExportToS3'] == 'true':
      log_groups_to_export.append(log_group['logGroupName'])
     

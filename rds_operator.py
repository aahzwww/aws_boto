#!/usr/bin/env python

import botocore
import croniter
import datetime
import boto3
import string


# return true if the cron schedule falls between now and now+seconds
def time_to_action(sched, now, seconds):
  try:
    cron = croniter.croniter(sched, now)
    d1 = now + datetime.timedelta(0, seconds)
    if (seconds > 0):
      d2 = cron.get_next(datetime.datetime)
      ret = (now < d2 and d2 < d1)
    else:
      d2 = cron.get_prev(datetime.datetime)
      ret = (d1 < d2 and d2 < now)

  except:
    ret = False

  return ret

now = datetime.datetime.now()


for region in boto3.session.Session().get_available_regions('rds'):

 
    try:
        client = boto3.client('rds', region)
        response = client.describe_db_instances()
        start_list = []
        stop_list = []

        for resp in response['DBInstances']:
            db_instance_arn = resp['DBInstanceArn']
            tag_list = client.list_tags_for_resource(ResourceName=db_instance_arn)
            
            for tags in tag_list['TagList']:            
                
                if tags['Key'] == 'auto:stop':
                    tag_value = tags['Value']
                    stop_sched = str.replace(tag_value,"@","*",6)
                    
                    #check status is running
                    if resp['DBInstanceStatus'] == 'available' and time_to_action(stop_sched, now, 11 * -60):
                        instanceid = resp['DBInstanceIdentifier']
                        client.stop_db_instance(DBInstanceIdentifier=instanceid)

                elif tags['Key'] == 'auto:start':
                    tag_value = tags['Value']
                    start_sched = str.replace(tag_value,"@","*",6)

                    #check status is running
                    if resp['DBInstanceStatus'] == 'stopped' and time_to_action(start_sched, now, 11 * 60):
                        instanceid = resp['DBInstanceIdentifier']
                        client.start_db_instance(DBInstanceIdentifier=instanceid)

        #check for manual stopped instance that have been auto restarted and stop them
        db_events = client.describe_events(SourceType='db-instance')

        for db_event in db_events['Events']:


            sourcearn = db_event['SourceArn']
            while sourcearn.find(':') != -1:
                sourcearn = sourcearn.split(':', 1)[-1]

            response = client.describe_db_instances(DBInstanceIdentifier=sourcearn)

            if db_event['Message'] == 'DB instance is being started due to it exceeding the maximum allowed time being stopped.' and response['DBInstances'][0]['DBInstanceStatus'] == 'available':
                client.stop_db_instance(DBInstanceIdentifier=sourcearn)

 
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'AuthFailure':
            continue
        elif e.response['Error']['Code'] == 'InvalidClientTokenId':
            continue
        else:
            print ('Exception error in %s: %s' % (region, e))

    except Exception as e:
      print ('Exception error in %s: %s' % (region, e))


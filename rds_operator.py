#!/usr/bin/python3
import boto.rds
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


for region in boto.rds.regions():

    if region.name != 'cn-north-1' and region.name != 'us-gov-west-1' :
 

        try:
            client = boto3.client('rds', region.name)
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

 

        except Exception as e:
            print ('Exception error in %s: %s' % (region.name, e))

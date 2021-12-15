#!/usr/bin/env python

import croniter
import datetime
import time
import boto3
import botocore

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

# go through all regions
for region in boto3.session.Session().get_available_regions('ec2'):

  try:
    client = boto3.client('ec2', region)
    instances = client.describe_instances()

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            stop_sched = 'Bone'
            start_sched = 'None'
            
            
            state = instance['State']['Name']

            if 'Tags' in instance:
                for tag in instance['Tags']:

                    # check auto:start and auto:stop tags
                    if tag['Key'] == 'auto:start':
                        #start_sched = inst.tags['auto:start'] if 'auto:start' in inst.tags else None
                        start_sched = tag['Value']
                    if tag['Key'] == 'auto:stop':
                        #stop_sched = inst.tags['auto:stop'] if 'auto:stop' in inst.tags else None
                        stop_sched = tag['Value']
        #print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (region.name, name, inst.id, inst.instance_type, inst.launch_time, state, start_sched, stop_sched, inst.tags)
            # queue up instances that have the start time falls between now and the next 6 minutes
            if start_sched != None and state == "stopped" and time_to_action(start_sched, now, 6 * 60):
                client.start_instances(InstanceIds=[instance['InstanceId']])

			
            # queue up instances that have the stop time falls between 6 minutes ago and now
            if stop_sched != None and state == "running" and time_to_action(stop_sched, now, 6 * -60):
                client.stop_instances(InstanceIds=[instance['InstanceId']])
        

  except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'AuthFailure':
      continue
    elif e.response['Error']['Code'] == 'InvalidClientTokenId':
      continue
    else:
      print ('Exception error in %s: %s' % (region, e))

  except Exception as e:
      print ('Exception error in %s: %s' % (region, e))


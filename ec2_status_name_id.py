#!/usr/bin/env python

import botocore
import boto3
import sys
import croniter
import datetime
import time

Single = 'N'


if len(sys.argv) > 1:
  nameIn = sys.argv[1]
  Single = 'Y'

for region in boto3.session.Session().get_available_regions('ec2'):

    try:
        client = boto3.client('ec2', region)
        response = client.describe_instances()
        #print (response)
        for resp in response['Reservations']:
            for inst in resp['Instances']:

                block = client.describe_instance_attribute(InstanceId=inst['InstanceId'],Attribute='blockDeviceMapping')
                if Single == 'Y' :
                    if nameIn == name :  
                        try:
                            print (inst['State']['Name'])
                            print ('Region:',region)
                            print ('Instance ID:',inst['InstanceId'])
                            print ('============')
                        except Exception as e:
                            print ('============')
                            continue

                else :
                    try:
                        print (inst['State']['Name'])
                        print ('Region:',region)
                        print ('Instance ID:',inst['InstanceId'])
                        print ('============')
                    except Exception as e:
                        print ('============')
                        continue

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'AuthFailure':
            continue
        elif e.response['Error']['Code'] == 'InvalidClientTokenId':
            continue
        else:
            print ('Exception error in %s: %s' % (region, e))
    except Exception as e:
      print ('Exception error in %s: %s' % (region, e))



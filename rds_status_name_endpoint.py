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
      client=boto3.client('rds', region)
      response = client.describe_db_instances()

      for res in response['DBInstances']:
        name = res['DBInstanceIdentifier']
        print(res)
        if Single == 'Y' :
            if nameIn == name :  
                print(region)

                print(name)
                print(res['DBInstanceStatus'])
                print(res['Endpoint']['Address'])
                print('============')

        else :

            print(region)

            print(name)
            print(res['DBInstanceStatus'])
            print(res['Endpoint']['Address'])
            print()

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'AuthFailure':
            continue
        elif e.response['Error']['Code'] == 'InvalidClientTokenId':
            continue
        else:
            print ('Exception error in %s: %s' % (region, e))

    except Exception as e:
      print ('Exception error in %s: %s' % (region, e))



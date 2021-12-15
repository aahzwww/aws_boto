#!/usr/bin/env python

import botocore
import boto3

for region in boto3.session.Session().get_available_regions('ec2'):

    try:
        client = boto3.client('ec2', region)
        instances = client.describe_instances()

        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                if 'Tags' in instance:
                    for tag in instance['Tags']:
                        #if tag['Key'] == 'Name':
                        if tag['Key'] == 'auto:stop':
                            print ( instance['InstanceId'],tag['Value'])
                            print ('============')

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'AuthFailure':
            continue
        elif e.response['Error']['Code'] == 'InvalidClientTokenId':
            continue
        else:
            print ('Exception error in %s: %s' % (region, e))

    except Exception as e:
      print ('Exception error in %s: %s' % (region, e))



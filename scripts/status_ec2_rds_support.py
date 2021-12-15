#!/usr/bin/env python3
import botocore
import boto3


for region in boto3.session.Session().get_available_regions('ec2'):

    try:
        client = boto3.client('ec2', region)
        instances = client.describe_instances()

        for reservation in instances['Reservations']:
            for inst in reservation['Instances']:
                Support = 'False'
                if 'Tags' in inst:
                    for tag in inst['Tags']:
                        if tag['Key'] == 'Support' and tag['Value'] == 'active':
                            Support = 'True'
                            print('ec2 instances in ' + region)
                            #print('Instance region : ' + region)
                            print('Instance ID : ' + inst['InstanceId'])
                            print('Instance status : ' + inst['State']['Name'])
                        if tag['Key'] == 'Name' and Support == 'True':
                            print('Instance name : ' + tag['Value'])
                            print('==========')
                        elif Support == 'True':
                            print('==========')

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'AuthFailure':
            continue
        elif e.response['Error']['Code'] == 'InvalidClientTokenId':
            continue
        else:
            print ('Exception error in %s: %s' % (region, e))

    except Exception as e:
      print ('Exception error in %s: %s' % (region, e))
 

for region in boto3.session.Session().get_available_regions('rds'):
    try:
        client = boto3.client('rds', region)
        response = client.describe_db_instances()

        for resp in response['DBInstances']:
            db_instance_arn = resp['DBInstanceArn']
            tag_list = client.list_tags_for_resource(ResourceName=db_instance_arn)
            for tags in tag_list['TagList']:
                if tags['Key'] == 'Support' and tags['Value'] == 'active':
                    print('Support rds instances in ' + region)
                    #print('Instance region : ' +  region)
                    print('Instance ID : ' + resp['DBInstanceIdentifier'])
                    print('Instance status : ' + resp['DBInstanceStatus'])
                    print('==========')

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'AuthFailure':
            continue
        elif e.response['Error']['Code'] == 'InvalidClientTokenId':
            continue
        else:
            print ('Exception error in %s: %s' % (region, e))

    except Exception as e:
      print ('Exception error in %s: %s' % (region, e))


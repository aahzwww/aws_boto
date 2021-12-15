#!/usr/bin/env python3
import botocore
import boto3



instance_found = 'False'
for region in boto3.session.Session().get_available_regions('rds'):

    try:
        client = boto3.client('rds', region)
        response = client.describe_db_instances()

        for resp in response['DBInstances']:
            if resp['DBInstanceStatus'] == "stopped":
                db_instance_arn = resp['DBInstanceArn']
                tag_list = client.list_tags_for_resource(ResourceName=db_instance_arn)
                for tags in tag_list['TagList']:
                    if tags['Key'] == 'Support' and tags['Value'] == 'active':
                        instance_found = 'True'

                        print('Instance region : ' +  region)
                        print('Instance ID : ' + resp['DBInstanceIdentifier'])
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

if instance_found == 'True':
    instance_region = input('Enter region of the instance to start...:')
    instanceid = input('Enter ID of the instance to start...:')
    if instanceid and instance_region:
        try:
            client = boto3.client('rds', instance_region)
            response = client.describe_db_instances()

            client.start_db_instance(DBInstanceIdentifier=instanceid)
        except Exception as e:
            print( 'Exception error in %s: %s' % (instanceid, e))
    else:
        print("ID or region missing")
else:
    print("No stopped instances found")

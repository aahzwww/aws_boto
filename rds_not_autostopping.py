#!/usr/bin/env python

import botocore
import boto3

stopping="FALSE"


for region in boto3.session.Session().get_available_regions('rds'):

    try:
        client = boto3.client('rds', region)
        response = client.describe_db_instances()

        for resp in response['DBInstances']:
            db_instance_arn = resp['DBInstanceArn']
            tag_list = client.list_tags_for_resource(ResourceName=db_instance_arn)
            
            stopping="FALSE"
            for tags in tag_list['TagList']:
                                
                if tags['Key'] == 'auto:stop': 
                    stopping="TRUE"

            if stopping=="FALSE":
        

                print(region)
                print(resp['DBInstanceIdentifier'])
                print(resp['DBInstanceStatus'])
                print(resp['Endpoint']['Address'])
                print('============')

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'AuthFailure':
            continue
        elif e.response['Error']['Code'] == 'InvalidClientTokenId':
            continue
        else:
            print ('Exception error in %s: %s' % (region, e))

    except Exception as e:
      print ('Exception error in %s: %s' % (region, e))



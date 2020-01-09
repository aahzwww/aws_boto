#!/usr/bin/python

import boto.rds
import boto3


for region in boto.rds.regions():

  if region.name != 'cn-north-1' and region.name != 'us-gov-west-1' :


    try:
        client = boto3.client('rds', region.name)
        response = client.describe_db_instances()

        for resp in response['DBInstances']:
            db_instance_arn = resp['DBInstanceArn']
            tag_list = client.list_tags_for_resource(ResourceName=db_instance_arn)

            for tags in tag_list['TagList']:

                if tags['Key'] == 'auto:stop': 
                    print region.name
                    print resp['DBName']
                    print resp['DBInstanceIdentifier']
                    print resp['DBInstanceStatus']
                    print resp['Endpoint']['Address']
                    print

    except Exception as e:
        print 'Exception error in %s: %s' % (region.name, e.message)




#!/usr/bin/python3

import boto3



instance_found = 'False'
for region in (boto3.session.Session().get_available_regions('rds')):
  #if region != 'cn-north-1' and region != 'us-gov-west-1' :
  if region != 'us-gov-west-1' and region != 'me-south-1' and region != 'ap-east-1':
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

      except Exception as e:
        print( 'Exception error in %s: %s' % (region, e))


if instance_found == 'True':
    #raw_input will have to just input for version 3
    instance_region = raw_input('Enter region of the instance to start...:')
    instanceid = raw_input('Enter ID of the instance to start...:')
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

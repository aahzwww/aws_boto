#!/usr/bin/python3

import boto3



for region in (boto3.session.Session().get_available_regions('ec2')):
  #if region != 'cn-north-1' and region != 'us-gov-west-1' :
    if region != 'us-gov-west-1' and region != 'me-south-1' and region != 'ap-east-1':
        try:
            client = boto3.client('ec2', region)
            response = client.describe_instances()
            for resp in response['Reservations']:
                for inst in resp['Instances']:
                    Support = 'False'
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
    
        # most likely will get exception on new beta region and gov cloud
        except Exception as e:
            print 'Exception error in %s: %s' % (region, e.message)
    
    if region != 'us-gov-west-1' and region != 'me-south-1' and region != 'ap-east-1':
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
                        print('Instance status : ' + inst['State']['Name'])
                        print('==========')

        except Exception as e:
            print('Exception error in %s: %s' % (region, e))


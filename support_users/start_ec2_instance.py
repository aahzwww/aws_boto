#!/usr/bin/python

import boto3
import sys



instance_found = 'False'
for region in (boto3.session.Session().get_available_regions('ec2')):
  #if region != 'cn-north-1' and region != 'us-gov-west-1' :
    if region != 'us-gov-west-1' and region != 'me-south-1' and region != 'ap-east-1':
        try:
            client = boto3.client('ec2', region)
            response = client.describe_instances()
            
            for resp in response['Reservations']:
                for inst in resp['Instances']:
                    if inst['State']['Name'] == 'stopped':
                        if inst['Tags']:
                            for tag in inst['Tags']:
                                if tag['Key'] == 'Support' and tag['Value'] == 'active':
                                    instance_found = 'True'
                                    
                                    print('Instance region : ' + region)
                                    print('Instance ID : ' + inst['InstanceId'])
                                    #print('Instance status : ' + inst['State']['Name'])
                                    print('==========')
    

        # most likely will get exception on new beta region and gov cloud
        except Exception as e:
            print 'Exception error in %s: %s' % (region, e.message)

if instance_found == 'True':
    #raw_input will have to just input for version 3
    instance_region = raw_input('Enter region of the instance to start...:')
    instanceid = raw_input('Enter ID of the instance to start...:')

    if instanceid and instance_region:
        try:
            client = boto3.client('ec2', instance_region)

            client.start_instances(InstanceIds=[instanceid])
        except Exception as e:
            print( 'Exception error in %s: %s' % (instanceid, e.message))
    else:
        print("ID or region missing")
else:
    print("No stopped instances found")

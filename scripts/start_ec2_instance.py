#!/usr/bin/env python3
import botocore
import boto3



instance_found = 'False'
for region in boto3.session.Session().get_available_regions('ec2'):

    try:
        client = boto3.client('ec2', region)
        instances = client.describe_instances()

        for reservation in instances['Reservations']:
            for inst in reservation['Instances']:
                if inst['State']['Name'] == 'stopped':
                    if 'Tags' in inst:
                        for tag in inst['Tags']:
                            if tag['Key'] == 'Support' and tag['Value'] == 'active':
                                instance_found = 'True'
                                    
                                print('Instance region : ' + region)
                                print('Instance ID : ' + inst['InstanceId'])
                                #print('Instance status : ' + inst['State']['Name'])
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
            client = boto3.client('ec2', instance_region)

            client.start_instances(InstanceIds=[instanceid])
        except Exception as e:
            print( 'Exception error in %s: %s' % (instanceid, e))
    else:
        print("ID or region missing")
else:
    print("No stopped instances found")

#!/usr/bin/python3

import subprocess
import boto.ec2

p = subprocess.Popen("curl -s http://169.254.169.254/latest/meta-data/instance-id/", stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
thisid = output

for region in boto.ec2.regions():
  if region.name != 'cn-north-1' and region.name != 'us-gov-west-1' :

    try:
      conn=boto.ec2.connect_to_region(region.name)
      reservations = conn.get_all_instances()

      for res in reservations:
        for inst in res.instances:
          name = inst.tags['auto:stop'] if 'auto:stop' in inst.tags else None
          if inst.id != thisid and name == None:
            print(inst.id)
            print(inst.tags['Name'])
  # most likely will get exception on new beta region and gov cloud
    except Exception as e:
      print('Exception error in %s: %s' % (region.name, e))


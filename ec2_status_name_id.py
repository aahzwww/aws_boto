#!/usr/bin/python

import sys
import boto.ec2
import croniter
import datetime
import time

Single = 'N'


if len(sys.argv) > 1:
  nameIn = sys.argv[1]
  Single = 'Y'

for region in boto.ec2.regions():
  if region.name != 'cn-north-1' and region.name != 'us-gov-west-1' :
    try:
      conn=boto.ec2.connect_to_region(region.name)
      reservations = conn.get_all_instances()

      for res in reservations:
          for inst in res.instances:
            name = inst.tags['Name']
            if Single == 'Y' :
              if nameIn == name :  
                print region

                name = inst.tags['Name']
                print name
                print inst.state
                print inst.id
                print

            else :

              print region

              name = inst.tags['Name']
              print name
              print inst.state
              print inst.id
              print


  # most likely will get exception on new beta region and gov cloud
    except Exception as e:
      print 'Exception error in %s: %s' % (region.name, e.message)

#!/usr/bin/python3


import boto.rds
regions = boto.rds.regions()




for region in boto.rds.regions():
  if region.name != 'cn-north-1' and region.name != 'us-gov-west-1' :

      try:

          rds=boto.rds.connect_to_region(region.name)
          dbs = rds.get_all_dbinstances()

          for db in dbs:

            print(region.name)
            print(db.status)
            print(db.endpoint)
            print()
      except Exception as e:
        print('Exception error in %s: %s' % (region.name, e))

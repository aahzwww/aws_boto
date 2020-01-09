#!/usr/bin/python

import boto.ec2
import croniter
import datetime
import time

start_list = []

# return true if the cron schedule falls between now and now+seconds
def time_to_action(sched, now, seconds):
  try:
    cron = croniter.croniter(sched, now)
    d1 = now + datetime.timedelta(0, seconds)
    if (seconds > 0):
      d2 = cron.get_next(datetime.datetime)
      ret = (now < d2 and d2 < d1)
    else:
      d2 = cron.get_prev(datetime.datetime)
      ret = (d1 < d2 and d2 < now)

  except:
    ret = False

  return ret

now = datetime.datetime.now()

# go through all regions
for region in boto.ec2.regions():
  if region.name != 'cn-north-1' and region.name != 'us-gov-west-1' :

    try:
      conn=boto.ec2.connect_to_region(region.name)
      reservations = conn.get_all_instances()

      for res in reservations:
        for inst in res.instances:
          name = inst.tags['Name'] if 'Name' in inst.tags else 'Unknown'
          state = inst.state

          # check auto:start and auto:stop tags
          start_sched = inst.tags['auto:start'] if 'auto:start' in inst.tags else None
          stop_sched = inst.tags['auto:stop'] if 'auto:stop' in inst.tags else None

          #print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (region.name, name, inst.id, inst.instance_type, inst.launch_time, state, start_sched, stop_sched, inst.tags)

          # queue up instances that have the start time falls between now and the next 30 minutes
          if start_sched != None and state == "stopped" and time_to_action(start_sched, now, 31 * 60):
    	    conn.start_instances(inst.id, dry_run=False)
	    start_list.append(inst.id)		

			
        # queue up instances that have the stop time falls between 30 minutes ago and now
          if stop_sched != None and state == "running" and time_to_action(stop_sched, now, 31 * -60):
	    conn.stop_instances(instance_ids=inst.id, dry_run=False)



  # most likely will get exception on new beta region and gov cloud
    except Exception as e:
      print 'Exception error in %s: %s' % (region.name, e.message)


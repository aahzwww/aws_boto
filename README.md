# aws_boto




ec2_operator.py  rds_operator.py  - script called by cron to start/stop instances with the auto:start/stop tag, ran via cron. (these are the scripts installed by the steps bellow)

# optional scripts

ec2_list_autostop_instances.py  rds_list_autostop_instances.py  - lists all instance with auto:stop tag.

ec2_not_autostoping.py rds_not_autostopping.py - list all instance with out the auto:start/stop tag.
 
ec2_status_name_id.py  rds_status_name_endpoint.py - list name and status of the instances.

install_start-stop.sh - install script for auto:stop and cron job


auto start/stop install instructions [copied and expaneded on from Shing Chen's Blog https://schen1628.wordpress.com/2014/02/04/auto-start-and-stop-your-ec2-instances/ ]



- create an IAM role. On the IAM Management Console, go to Roles and click Create New Roles.
- Add a role name. (used when creating the ec2 instance)
- On the next screen, select AWS Service Roles and then Amazon EC2.
- On the next screen, select Custom Policy.
- Type an arbitrary name to the Policy Name field.
- Paste the following JSON block to the Policy Document field to indicate the IAM role is allowed to perform describe instances, start instances and stop instances action. 

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:StartInstances",
                "rds:ListTagsForResource",
                "rds:DescribeDBInstances",
                "ec2:StopInstances",
                "rds:StopDBInstance",
                "rds:StartDBInstance"
            ],
            "Resource": "*"
        }
    ]
}



- Review the role information and click Create Role to finish.
- Provision a micro EC2 Amazon Linux AMI setting the AMI role to the one created above
- wget https://raw.githubusercontent.com/aahzwww/aws_boto/master/install_start-stop.sh
- chmod +x install_start-stop.sh
- ./install_start-stop.sh

or manually do it with the steps below

//manual steps start

- create ec2_operator.py in /home/ec2-user/ 
wget https://raw.githubusercontent.com/aahzwww/aws_boto/master/ec2_operator.py
- create rds_operator.py in /home/ec2-user/
wget https://raw.githubusercontent.com/aahzwww/aws_boto/master/rds_operator.py
- sudo yum install -y gcc
- curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
- python get-pip.py --user
- export PATH=~/.local/bin/pip:$PATH
- pip install --user --upgrade awscli
- pip install croniter --user
- pip install boto --user
- pip install boto3 --user
- chown ec2-user:ec2-user /home/ec2-user/ec2_operator.py
- chmod 744 /home/ec2-user/ec2_operator.py
- add "*/5 * * * * ec2-user python /home/ec2-user/ec2_operator.py" to /etc/crontab or the users crontab
- chown ec2-user:ec2-user /home/ec2-user/rds_operator.py
- chmod 744 /home/ec2-user/rds_operator.py
- add "*/5 * * * * ec2-user python /home/ec2-user/rds_operator.py" to /etc/crontab or the users crontab

//manual steps end

- Tag the instance that you want to stop or start with name auto:start/auto:stop and value of when you want them to start/stop in cron format, 0 14 * * * is 2 pm everyday. rds does not allow * so replace them with @
- cron job time are in UTC 

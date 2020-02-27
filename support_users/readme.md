# Support Stop Start

//manual steps start

- sudo yum install -y gcc
- curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
- python get-pip.py --user
- export PATH=~/.local/bin/pip:$PATH
- pip install --user --upgrade awscli
- pip install croniter --user
- pip install boto --user
- pip install boto3 --user
- mkdir ~/scripts/
- cd scripts

- wget  https://raw.githubusercontent.com/aahzwww/aws_boto/master/support_users/start_db_instance.py 
- wget  https://raw.githubusercontent.com/aahzwww/aws_boto/master/support_users/start_ec2_instance.py
- wget  https://raw.githubusercontent.com/aahzwww/aws_boto/master/support_users/status_ec2_rds_support.py 
- wget  https://raw.githubusercontent.com/aahzwww/aws_boto/master/support_users/stop_db_instance.py
- wget  https://raw.githubusercontent.com/aahzwww/aws_boto/master/support_users/stop_ec2_instance.py

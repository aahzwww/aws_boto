# Support Stop Start

//manual steps start
//if you have already done the install from https://github.com/aahzwww/aws_boto jump to "mkdir ~/scripts
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

- wget  https://raw.githubusercontent.com/aahzwww/aws_boto/master/scripts/start_db_instance.py 
- wget  https://raw.githubusercontent.com/aahzwww/aws_boto/master/scripts/start_ec2_instance.py
- wget  https://raw.githubusercontent.com/aahzwww/aws_boto/master/scripts/status_ec2_rds_support.py 
- wget  https://raw.githubusercontent.com/aahzwww/aws_boto/master/scripts/stop_db_instance.py
- wget  https://raw.githubusercontent.com/aahzwww/aws_boto/master/scripts/stop_ec2_instance.py

- chmod +x *.py
- sudo adduser support
- sudo vi /etc/sudoers.d/support_access
- add the following 

support ALL=(ec2-user) NOPASSWD:/home/ec2-user/scripts/start_ec2_instance.py

support ALL=(ec2-user) NOPASSWD:/home/ec2-user/scripts/start_db_instance.py

support ALL=(ec2-user) NOPASSWD:/home/ec2-user/scripts/stop_ec2_instance.py

support ALL=(ec2-user) NOPASSWD:/home/ec2-user/scripts/stop_db_instance.py

support ALL=(ec2-user) NOPASSWD:/home/ec2-user/scripts/status_ec2_rds_support.py

- add tag to support instance Tag name = Support Tag value = active

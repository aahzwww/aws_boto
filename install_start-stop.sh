#!/bin/bash -v


sudo yum install -y gcc
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py --user
export PATH=~/.local/bin/pip:$PATH
pip install --user --upgrade awscli
pip install croniter --user
pip install boto --user
pip install boto3 --user
OPERATOR=/home/ec2-user/ec2_operator.py
OPERATOR2=/home/ec2-user/rds_operator.py
wget -O $OPERATOR https://raw.githubusercontent.com/aahzwww/aws_boto/master/ec2_operator.py
wget -O $OPERATOR2 https://raw.githubusercontent.com/aahzwww/aws_boto/master/rds_operator.py
chown ec2-user:ec2-user $OPERATOR
chown ec2-user:ec2-user $OPERATOR2
chmod 744 $OPERATOR
chmod 744 $OPERATOR2
echo "*/5 * * * * ec2-user python $OPERATOR" | sudo tee -a /etc/crontab
echo "*/5 * * * * ec2-user python $OPERATOR2" | sudo tee -a /etc/crontab

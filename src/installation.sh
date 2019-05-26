#!/bin/sh
apt-get install -y python3-pip
echo mysql-server-5.1 mysql-server/root_password password take5 | debconf-set-selections
echo mysql-server-5.1 mysql-server/root_password_again password take5 | debconf-set-selections
apt-get install -y mysql-server
apt-get install -y libmysqlclient-dev
apt-get install -y python-pip python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg8-dev zlib1g-dev
pip3 install pymysql==0.8.0
pip3 install Django==1.10.5
pip3 install django-crispy-forms==1.6.1
pip3 install django-datetime-widget==0.9.3
pip3 install dnspython3
pip3 install aiohttp==2.3.9
#pip3 install aiomysql==0.0.12
pip3 install mysqlclient==1.4.2.post1
pip3 install httplib2==0.9.1
pip3 install mysqlclient==1.3.10
pip3 install mysql-connector==2.1.4
mysql -u root -p'take5' < Databases_Backup/all_databases_populated.sql




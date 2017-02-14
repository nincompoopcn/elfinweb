#!/bin/sh

cd /root/app/db

name=$(date +%Y_%m_%d_%H_%M_%S)

if [ -d '$name' ]; then
    rm -rf $name
fi
mkdir $name

mysqldump maintenance -u'root' -p'!@mY0urF@th3r' | gzip > $name/maintenance.gz
scp -r $name ps_rel_ci@hzling45.china.nsn-net.net:~/maintenance/

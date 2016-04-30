#!/bin/sh

# copy uwsgi.conf to upstart
sudo cp uwsgi.conf /etc/init/
sudo ln -s /lib/init/upstart-job /etc/init.d/uwsgi

# copy celery.conf to upstart
sudo cp celery.conf /etc/init/
sudo ln -s /lib/init/upstart-job /etc/init.d/celery

# create necessary uwsgi folders
sudo mkdir -p /var/log/uwsgi
sudo mkdir -p /etc/uwsgi/apps-enabled
sudo mkdir -p /etc/uwsgi/apps-available

# necessary log folder for logging
sudo mkdir -p /var/log/traclist
sudo mkdir -p /var/log/nginx/traclist
sudo chown -R traclist.traclist /var/log/traclist
sudo chown -R traclist.traclist /var/log/nginx

# create necessary symbolic links for uwsgi
sudo ln -s /opt/Traclist/conf/uwsgi/main.ini /etc/uwsgi/apps-enabled
sudo ln -s /opt/Traclist/conf/uwsgi/admin.ini /etc/uwsgi/apps-enabled
sudo ln -s /opt/Traclist/conf/uwsgi/api.ini /etc/uwsgi/apps-enabled

# create necessary symbolic links for nginx
sudo ln -s /opt/Traclist/conf/nginx/traclist.com /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default


# necessary log folder for celery
sudo mkdir -p /var/log/celery
sudo chown -R traclist.traclist /var/log/celery
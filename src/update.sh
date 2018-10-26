#!/bin/bash
# Copy source files to netdata directories
echo "Copy plugin"
cp nanonode.chart.py /usr/libexec/netdata/python.d/
echo "Copy plugin config to default location"
cp nanonode.conf /usr/lib/netdata/conf.d/python.d
echo "Copy dashboard"
cp nano.html /usr/share/netdata/web
echo "Copy dashboard style"
cp nano.css /usr/share/netdata/web
echo "Set netdata read access for dashboard and style"
chown -R netdata:netdata /usr/share/netdata/web/nano.html
chown -R netdata:netdata /usr/share/netdata/web/nano.css

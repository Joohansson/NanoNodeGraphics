# NanoNodeGraphics
Nano Node Graphics is a simplified dashboard for your nano node based on netdata application and nano node monitor api.

* [Dark Theme Preview](https://i.imgur.com/2k5Qska.jpg)
* [Light Theme Preview](https://i.imgur.com/TPUdbLd.jpg)

## Current Version
Current version is 1.13. Check your nano.html if this one is newer, continue with **[Update procedure](#update-nanonodegraphics)** below.

## Requirements
* Netdata application [Source](https://github.com/netdata/netdata)
* Nano node [Source](https://github.com/nanocurrency/raiblocks/releases)
* Nano node monitor, preferrably connected to [mynano.ninja](https://mynano.ninja/) [Source](https://github.com/NanoTools/nanoNodeMonitor)

## Installation
1. Install netdata. Easiest with the one-liner. https://github.com/netdata/netdata/wiki/Installation - There is also a guide for DigitalOcean here: https://www.digitalocean.com/community/tutorials/how-to-set-up-real-time-performance-monitoring-with-netdata-on-ubuntu-16-04
2. Make sure it's running. Should be accessible at http://localhost:19999 or http://yourIP:19999 (how to configure firewall later). Test at least locally with `curl localhost:19999`
3. Clone this repo into your home directory: `git clone https://github.com/Joohansson/NanoNodeGraphics`
4. Go to source files: `cd NanoNodeGraphics/src/`
5. **If standard netdata folders use autocopy.sh and continue at 15 or do manually 6-14:** `sudo chmod +x autocopy.sh && sudo ./autocopy.sh`
6. Copy source file to netdata default plugin dir: `sudo cp nanonode.chart.py /usr/libexec/netdata/python.d/`
7. Copy config file to netdata default config dir: `sudo cp nanonode.conf /usr/lib/netdata/conf.d/python.d`
8. Copy simplified dashboard html to web dir: `sudo cp nano.html /usr/share/netdata/web`
9. Copy simplified dashboard style to web dir: `sudo cp nano.css /usr/share/netdata/web`
10. Set html read access for netdata user: `sudo chown -R netdata:netdata /usr/share/netdata/web/nano.html`
11. Set css read access for netdata user: `sudo chown -R netdata:netdata /usr/share/netdata/web/nano.css`
12. **Configure in order to match plugin with your nano installation:**
13. Go to netdata: `cd /etc/netdata/`
14. Copy default config to user folder: `sudo ./edit-config python.d/nanonode.conf` (save vim file with ctrl+c, :x, enter)
15. Edit file with nano editor `sudo nano /etc/netdata/python.d/nanonode.conf`
16. Go to bottom and check if the url to your nano node monitor json is correct. It will try all urls and select the first one that works if they have same name definition. One is enough but you can add as many nano node monitors as you like, local or remote (with different names). (Test any url if it loads node monitor json like so: `curl localhost/api.php`) - Save with ctrl+x.
17. Restart netdata: `sudo systemctl restart netdata.service`
18. Open a browser and load your netdata dashboard from step 2. The nanonode local and charts should show up after 10-60sec after service restart.
19. If charts are working load the simplified dashboard: http://yourIP:19999/nano.html (if no access, test locally with `curl localhost:19999/nano.html` - then check how to configure firewall below).

## Configuration / Troubleshooting
### -Nano node monitor
The NanoNodeGraphics need to access your **NanoNodeMonitor** API. Your node monitor is most likely accessible from the internet on some IP or DOMAIN. That means port 80 is open in your vps network which land on the node monitor web server. Internally that is most likely http://localhost/api.php and it uses ipv4 127.0.0.1 and/or ipv6 [::1]. In the json you have all three setup as default which means it will try all and use the first one that succeed. You can try this by running the curl command: curl localhost/api.php, curl 127.0.0.1/api.php and curl [::1]/api.php. If you get same response as http://yourNodeMonitorURL/api.php from a remote browser you are good to go!

### -Firewall
**Netmonitor** setup a second web server on your vps running on port 19999 as default and you can test that with curl localhost:19999 for example or if you followed my instructions: curl localhost:19999/nano.html should give the content of nano.html. What you probably need to do is to give access to inbound TCP port 19999 from outside your vps into your netdata server (often called port forward, NAT rule or firewall policy). Maybe you allow all ports or only port 80 (or no firewall at all), you have to check your vps network config. For DigitalOcean there is a guide in step 1 above and more specifically for firewall setup [Here](https://www.digitalocean.com/docs/networking/firewalls/how-to/configure-rules/). You might need to configure UFW internal firewall if you have any but do it last if nothing else works: `sudo ufw allow 19999/tcp`

### -Plugin
**The nano plugin** can also be configured. `sudo nano /usr/libexec/netdata/python.d/nanonode.chart.py`

You can change how often it updates the charts with "update_every = 5". Change where in the advanced dashboard it show up with "priority = 1000" or change what charts that should be visible with "ORDER". **This file will be overwritten if you follow the update procedure below.** [More Info](https://github.com/netdata/netdata/tree/master/collectors/plugins.d)

After configuring plugin you need to restart netdata and wait approx 15sec: `sudo systemctl restart netdata.service`

### -Custom Dashboard
**The dashboard** can also be configured to your own liking: `sudo nano /usr/share/netdata/web/nano.html`
For example changing the title, description theme, and url to your dashboard.js. This dashboard can be run on any web server or even locally from a pc folder. Don't need to be on the same machine as netdata. Just link to your dashboard.js and it should work. **This file will be overwritten if you follow the update procedure below.** [More Info](https://github.com/netdata/netdata/wiki/Custom-Dashboards)

### -Netdata
Finally, **the netdata itself** can be configured: `sudo nano /etc/netdata/netdata.conf`

You can uncomment stuff like "history = 18000" to save history for 5h (requires a bit more ram, approx 60MB), "update every = 5" to slow down the chart updates to once every 5sec, change default port from 19999, etc. [More Info](https://github.com/netdata/netdata/wiki/Configuration)

**You probably want netdata to start at boot** [More info](https://github.com/netdata/netdata/wiki/Installation):
- stop netdata
`killall netdata`

- copy netdata.service to systemd
`cp system/netdata.service /etc/systemd/system/`

- let systemd know there is a new service
`systemctl daemon-reload`

- enable netdata at boot
`systemctl enable netdata`

- start netdata
`systemctl start netdata`

## Update NanoNodeGraphics
1. Go to the NanoNodeGraphics dir and pull from github or remove and make a new clone if that doesn't work: `git pull` or `git clone`
2. Push files to netdata (excluding user config of plugin): `cd src && sudo chmod +x update.sh && sudo ./update.sh`
3. Restart netdata: `sudo systemctl restart netdata.service`

## Demo site (Odroid C2). PLEASE DON'T ABUSE, I WILL HAVE TO DISABLE THESE URLs.
* [Advanced dashboard](http://node.nanolinks.info:8080)
* [Simple dashboard](http://node.nanolinks.info:8080/nano.html)

## Donation
If you find this helpful, any small nano donation is greatly appreciated!
<figure>
	<img id="qrImage" src="https://raw.githubusercontent.com/Joohansson/nanolinks/master/src/qr_new.png" alt="Nano Donation" />
	<figcaption class="subtext">xrb_1gur37mt5cawjg5844bmpg8upo4hbgnbbuwcerdobqoeny4ewoqshowfakfo</figcaption>
</figure>

## Nano Related
Check out other awesome nano projects: [NanoLinks](https://nanolinks.info)

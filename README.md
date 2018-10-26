# NanoNodeGraphics
Nano Node Graphics is a simplified dashboard for your nano node based on netdata application and nano node monitor api.

* [Dark Theme Preview](https://i.imgur.com/2k5Qska.jpg)
* [Light Theme Preview](https://i.imgur.com/TPUdbLd.jpg)

## Requirements
* Netdata application [Source](https://github.com/netdata/netdata)
* Nano node [Source](https://github.com/nanocurrency/raiblocks/releases)
* Nano node monitor, preferrably connected to [mynano.ninja](https://mynano.ninja/) [Source](https://github.com/NanoTools/nanoNodeMonitor)

## Installation
1. Install netdata. Easiest with the one-liner. https://github.com/netdata/netdata/wiki/Installation
2. Make sure it's running. Should be accessible at http://localhost:19999
3. Clone this repo into your home directory: `git clone https://github.com/Joohansson/NanoNodeGraphics`
4. Go to source files: `cd NanoNodeGraphics/src/`
5. **If standard netdata folders use autocopy.sh and continue at 15 or do manually 6-14:** `sudo chmod +x autocopy.sh && sudo ./autocopy.sh`
6. Copy source file to netdata default plugin dir: `sudo cp nanonode.chart.py /usr/libexec/netdata/python.d/`
7. Copy config file to netdata default config dir: `sudo cp nanonode.conf /usr/lib/netdata/conf.d/python.d`
8. Copy simplified dashboard html to web dir: `sudo cp nano.html /usr/share/netdata/web`
9. Set read access for netdata user: `sudo chown -R netdata:netdata /usr/share/netdata/web/nano.html`
10. Copy simplified dashboard style to web dir: `sudo cp nano.css /usr/share/netdata/web`
11. Set read access for netdata user: `sudo chown -R netdata:netdata /usr/share/netdata/web/nano.html`
12. **Configure in order to match plugin with your nano installation:**
13. Go to netdata: `cd /etc/netdata/`
14. Copy default config to modified config: `sudo ./edit-config python.d/nanonode.conf` (save vim file with ctrl+c, :x, enter)
15. Edit file with nano editor `sudo /etc/netdata/nano python.d/nanonode.conf`
16. Go to bottom and check if the url to your nano node monitor json is correct. Loading it in browser should show the stats. You can add as many nano node monitors as you like, local or remote. Save with ctrl+x.
17. Restart netdata: `sudo systemctl restart netdata.service`
18. Open a browser and load your netdata dashboard. The nanonode local and charts should show up after 10-60sec after service restart.
19. If charts a working load the simplified dashboard: http://netdataURL/nano.html

## Configuration
Apart from step 11 above, **the plugin** can also be configured. `sudo nano /usr/libexec/netdata/python.d/nanonode.chart.py`

You can change how often it updates the charts with "update_every = 5". Change where in the advanced dashboard it show up with "priority = 1000" or change what charts that should be visible with "ORDER". [More Info](https://github.com/netdata/netdata/tree/master/collectors/plugins.d)

After configuring plugin you need to restart netdata: `sudo systemctl restart netdata.service`

**The dashboard** can also be configured to your own liking: `sudo nano /usr/share/netdata/web/nano.html`
For example changing the title, description theme, and url to your dashboard.js. This dashboard can be run on any web server or even locally from a pc folder. Don't need to be on the same machine as netdata. Just link to your dashboard.js and it should work. [More Info](https://github.com/netdata/netdata/wiki/Custom-Dashboards)

Finally, **the netdata itself** can be configured: `sudo nano /etc/netdata/netdata.conf`

You can uncomment stuff like "history = 18000" to save history for 5h (require a bit more ram), "update every = 5" to slow down the chart updates to once every 5sec, etc. [More Info](https://github.com/netdata/netdata/wiki/Configuration)

## Update
* Go to the NanoNodeGraphics dir and pull from github or make a new clone: `git pull`
* Redo step 4-10 and 16

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

## TODO
* I have yet to figure out how to show decimals on the dashboard from the plugin. Any help needed!

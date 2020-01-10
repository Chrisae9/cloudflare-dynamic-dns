# raindrop
Simple python script to enable dynamic updating of IP address in Cloudflare using Cloudflare's API

# Overview

This is a very simple Python script meant to allow for "Dynamic DNS" when using Cloudflare's name servers - a functionality which (at least as far as I could tell) did not appear to be built in to the web interface. It also appeared that `ddclient`'s Cloudflare DDNS functionality was broken as it was still using the V1 API.

# How it works

This script assumes you want to use DDNS to get DNS resolution to a device with a non-static IP, and possibly behind a home router or firewall. It obtains the server's external IP address by querying api.ipify.org, and then updates the DDNS record in Cloudflare with that address using their V4 API.

The credentials used to access Cloudflare's API are read from the JSON formatted file, uploaded in this repository as "example_credentials.json". The fields specified in the file are required for the script to work, but this credential file does not need to have a specific name or even be in the same directory as `raindrop.py`. See Usage, below.

# Usage

## Dependencies

This script depends on

  * Python3
  * Package: json
  * Package: sys
  * Package: requests

At least as of the version of Python3 that was installed when using `apt-get install python3` on `Debian Buster`, these packages were installed as part of the standard installation.

## Credentials

The `example_credentials.json` file is a simple JSON formatted file. There are four required fields:

* `zone`: This is the "Zone ID" that you'll see when you log in to Cloudflare and go to the domain you want DDNS for.
* `email`: This is your email address that you use to log in to cloudflare
* `key`: This is your API key to Cloudflare. Again, this is obtainable by logging in to your account and either going to "Get API Key" or your user settings page.
* `domain`: This is the full domain that you want to update the IP for when the script runs. For example, if you wanted to update the record for `subdomain` under `mycoolsite.tld`, your `domain` would be `subdomain.mycoolsite.tld`.

These parameters are all things required by the Cloudflare API. You can view their API [here](https://api.cloudflare.com/#dns-records-for-a-zone-properties) to see their definitions and an example for each parameter if you're unclear. The documentation for each API call used in this script are also available.

## Calling the script

This script is simply called using

`python3 /path/to/raindrop.py /path/to/credentials.json`

This script should complete in < 1 second, and it does not need to be run repeatedly. It is really only intended to be run no more than every ~10 minutes or so, and can even be less frequently than that (How often do you expect your IP to change, after all?). Cloudflare's API limits are substantially higher than this, but it's still good to be a nice user and not hammer their API.

This script can be added as a cron job on Linux systems to automate the update process. For example, to run every 30 minutes an entry to `/etc/crontab` might look like:

```
# Send an update of our IP to Cloudflare every 30 minutes
*/30 * * * * /usr/bin/python3 /path/to/raindrop.py /path/to/credentials.json
```

# Caveats/Gotchas

1) The DNS record to be updated is assumed to already exist. There is API support to allow the script to check if the domain to be created already exists and create it if it does not, but I did not implement that check.

2) There is no checking on the script to see if the current IP matches the one that is already listed. The IP is just pushed to Cloudflare regardless. As with (1), this is something that can be done - I just haven't, mostly since I expect that this will not get a large amount of traction.

Lastly: **This script is provided "as-is" - meaning that I take no responsibility if anything goes wrong from you using this.** I do not work for Cloudflare or any other software company - I'm just someone who has a keyboard and a bit of coding experience, and needed a DDNS updater for my domain and existing options were broken. I have done my best to write this script in a way that I am comfortable using it myself, but you can never predict every possible situation. 

As such - read and understand the script before running code a random stranger wrote on your computer. I've done my best to comment it to explain my thought process, and the actual work is done in less than 10 lines.

If you do find a bug, or see something you'd like to see updated, I happily accept pull requests.

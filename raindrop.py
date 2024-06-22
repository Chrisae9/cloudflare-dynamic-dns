##########
# NOTICE #
##########
#
# This script is provided "as-is". I do not work for Cloudflare.
# I don't even have a paid account - I simply use their free service and needed
#   DDNS capabilities which did not appear to be supported through other means.
# I have done my best to write this in a way that I am comfortable using it
#    myself, but I'm nothing more than someone with a keyboard and
#   some coding knowledge.
# As such, use this at your own risk. Read and understand the code below.
#   I've tried to comment this as best as I can to ensure it can be understood
#   what my intent was on each line
# Cloudflare API Reference: https://api.cloudflare.com
##########

import json
import sys
import requests

# Check to make sure only 2 arguments were passed to the command. The first (argv[0]) is the program name, argv[1] is the path to the credentials JSON file
if( len(sys.argv) > 2):
    raise AttributeError("Only 1 argument to this script is supported!")

# Open the JSON-formatted paramters file and load it in to a Dict
with open(sys.argv[1]) as f:
    params = json.load(f)

# These are headers we'll have to send along with any of our requests to get the API to respond.
# The zone and api keys also let Cloudflare know what account we're referring to.
headers = {"X-Auth-Key":params['key'],"X-Auth-Email":params["email"],"Content-Type":"application/json"}

# Get our external IP
# This website was chosen arbitrarily, mainly because it returns the IP in a very simple way that doesn't require any additional parsing.
myip = requests.get('https://api.ipify.org').text
print("Updating Cloudflare DDNS with IP: {0}".format(myip)) # Just printing the log message in case something goes wrong. This will show what IP it tried to update with.

for domain in params['domains']:
# Now get the id of the record we want to update. We need this ID to actually update the record, and there doesn't seem to be an easy way to get it manually (I.E from the cloudflare site)
# Reference: https://api.cloudflare.com/#dns-records-for-a-zone-list-dns-records
# We assume that the record already exists. We could add a "check if exists, update if it does, create it if it doesn't" check down the road.
    args = {"type":"A","name":domain['name']}
    r = requests.get("https://api.cloudflare.com/client/v4/zones/{0}/dns_records".format(params['zone']), headers=headers, params=args)
    # print(r.json())
    recordid = r.json()['result'][0]['id']

    # Now send our IP to cloudflare to update the IP.
    # Reference: https://api.cloudflare.com/#dns-records-for-a-zone-update-dns-record
    # Note - we do no checking on this end to see if the IP we want to update to is the same as what's already there.
    # The assumption is that this script runs infrequently - every 10+ minutes at most - so this isn't an issue and cloudflare hopefully does some checking on their end.
    # It would also be possible to add a check here that simply checks to see if the already set IP matches the one we want to update to, and only send if they don't match.
    print(f"Updating DNS record for {domain}")
    args = {"type":"A","name":domain['name'],"content":myip,"ttl":1,'proxied':domain['proxied']} # We use the default TTL value of 1 as specified in the cloudflare API for "auto".
    p = requests.put("https://api.cloudflare.com/client/v4/zones/{0}/dns_records/{1}".format(params['zone'],recordid),headers=headers, data=json.dumps(args))
    print("Got response")
    print(p)

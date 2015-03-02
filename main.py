from collections import OrderedDict

wlan = "wlan0"
ssid = "linkyfy"
password = "helloworld"

config = OrderedDict()
config['interface'] = wlan
config['driver'] = 'nl80211'
config['ssid'] = ssid
config['hw_mode'] = 'g'
config['channel'] = '6'
config['macaddr_acl'] = '0'
config['ignore_broadcast_ssid'] = '0'
config['auth_algs'] = '1'

config['wpa'] = '1'
config['wpa_passphrase'] = password
config['wpa_key_mgmt'] = 'WPA-PSK'
config['wpa_pairwise'] = 'TKIP'
config['rsn_pairwise'] = 'CCMP'

configFile = open('example.cfg',"w")
for key in config:
	line = key+"="+config[key]
	configFile.write(line+'\n')

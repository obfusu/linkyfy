from collections import OrderedDict
import os
import commands

from gi.repository import Gtk

start_script = """
killall hostapd
killall dnsmaq
nmcli radio wifi off
rfkill unblock wifi
hostapd $(pwd)/hostapd.conf  
echo hostapd started, now configuring masquerade..
#echo 1 > /proc/sys/net/ipv4/ip_forward
"""

stop_script = """
nmcli radio wifi on
echo hostapd stopped
killall hostapd
killall dnsmasq
"""

getwlan_bash_str = "nmcli dev | grep wifi | cut -d' ' -f1 | head -1"
getinet_bash_str = "nmcli dev | grep connected | cut -d' ' -f1 | head -1"

s = commands.getstatusoutput(getwlan_bash_str)
wlan = s[1]

def create_config():
	t = commands.getstatusoutput(getinet_bash_str)
	inet = t[1]
	ssid = ssid_object.get_text()
	key = key_object.get_text()	
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
	config['wpa_passphrase'] = key
	config['wpa_key_mgmt'] = 'WPA-PSK'
	config['wpa_pairwise'] = 'TKIP'
	config['rsn_pairwise'] = 'CCMP'

	configFile = open('hostapd.conf',"w")
	for key in config:
		line = key+"="+config[key]
		configFile.write(line+'\n')
	configFile.close()

	dnsConfigFile = open('dnsmasq.conf',"w")
	dnsConfigFile.write('no-resolv\n')
	dnsConfigFile.write('no-poll\n')
	dnsConfigFile.write('interface='+wlan+'\n')
	dnsConfigFile.write('dhcp-range=192.168.43.50,192.168.43.150,12h'+'\n')
	dnsConfigFile.write('server=8.8.8.8\n')
	dnsConfigFile.write('server=8.8.8.4\n')
	dnsConfigFile.close()


class Handler:
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)
	def linkyfy_start(self, button):
		print "Linkyfy will start"
		create_config()
		os.system("bash -c '%s'" %start_script)
		wlan_config_cmd = "ifconfig " + wlan  + " 192.168.43.1 netmask 255.255.255.0"
		print wlan_config_cmd
		os.system("bash -c '%s'" %wlan_config_cmd)
	def linkyfy_stop(self, button):
		print "Linkyfy will stop"
		os.system("bash -c '%s'" %stop_script)


builder = Gtk.Builder()
builder.add_from_file("linkyfy-ui.glade")
builder.connect_signals(Handler())
window = builder.get_object("window1")
window.show_all()

global ssid_object
ssid_object = builder.get_object('ssid_value')
global key_object
key_object = builder.get_object('key_value')

ssid_object.set_text('linkyfy')
key_object.set_text('password')
Gtk.main()

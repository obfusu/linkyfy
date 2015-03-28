# Linkyfy
# Copyright (C) 2015 C Ganesh Sundar
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from collections import OrderedDict
import os
import commands

from gi.repository import Gtk

start_script = """
killall hostapd
killall dhcpd
nmcli radio wifi off
nmcli nm wifi off
rfkill unblock wifi
sysctl net.ipv4.ip_forward=1
"""

ipforward_script = """	
iptables -t nat -F
iptables -t nat -A POSTROUTING -j MASQUERADE
"""

stop_script = """
nmcli radio wifi on
nmcli nm wifi on
killall hostapd
killall dhcpd
echo linkyfy: hostapd, dhcpd stopped
"""

getwlan_bash_str = "nmcli dev | grep -E 'wifi|wireless' | cut -d' ' -f1 | head -1"
getinet_bash_str = "nmcli dev | grep connected | cut -d' ' -f1 | head -1"

s = commands.getstatusoutput(getwlan_bash_str)
wlan = s[1]

def create_config():
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


class Handler:
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)
	def linkyfy_start(self, button):
		print "Linkyfy will start"
		create_config()
		cmd = "ifconfig " + wlan  + " 169.254.0.1 netmask 255.255.0.0"
		cmd = start_script + '\n' + cmd
		os.system("bash -c '%s'" %cmd)
		
		cmd = "hostapd $(pwd)/hostapd.conf -B"
		cmd += "\niptables -A FORWARD -i " + wlan + " -j ACCEPT"
		os.system("bash -c '%s'" %cmd)
		
		cmd = "dhcpd -cf $(pwd)/dhcpd.conf"
		os.system("bash -c '%s'" %cmd)

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

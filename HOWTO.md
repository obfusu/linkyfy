Linkyfy How-To: 
------------

First install the dependencies

For Ubuntu/Debian based

	sudo apt-get install hostapd isc-dhcp-server

For Fedora/CentOS based

	sudo yum install hostapd dhcp

For Arch based

    sudo pacman -S hostapd dhcp

Note: You also need GTK+ 3 Library

Usage:
------
	git clone https://github.com/77ganesh/linkyfy.git
	cd linkyfy
	sudo python2 main.py

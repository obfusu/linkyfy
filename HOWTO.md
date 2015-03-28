Linkyfy How-To: 
------------

First install the dependencies

For Ubuntu/Debian based

	sudo apt-get install hostapd isc-dhcp-server python-gobject

For Fedora/CentOS based

	sudo yum install hostapd dhcp pygobject3

For Arch based

    sudo pacman -S hostapd dhcp python-gobject

Note: You also need GTK+ 3 Library

Usage:
------
	git clone https://github.com/77ganesh/linkyfy.git
	cd linkyfy
	sudo python2 main.py

Procedure for internet Sharing:
------------------------------

* Connect to internet (ethernet) first
* Start Linkyfy
* Now the connection will be shared

Note: Working on Fedora 21, testing pending on other distros 

#!/bin/bash
if [ ! -f /tmp/rss_running ]; then
	cd /home/joshua/Scripts/RSS/cgi-bin
	touch /tmp/rss_running
	python RSSupdate.py
	rm /tmp/rss_running
fi

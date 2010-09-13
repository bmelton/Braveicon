#!/usr/bin/env python
#####################
# Icon.py
# Fetches a site's favicon URL.  Respects link rel="" declarations
# most importantly, per W3C spec, however, it favors 'shortcut icon' 
# over /favicon.ico, as many software packages explicitly declare
# via shortcut icon, and W3C snubs /favicon.ico, generally speaking

import sys
from BeautifulSoup import BeautifulSoup
import urllib


def get_favicon(url):
	# Quickly normalize the URL.  
	starts = False
	ends   = False
	if url.startswith("http://"):
		pass
	elif url.startswith("https://"):
		pass
	else:
		url = "http://%s" % url

	if url.endswith("/"):
		url = url[0:len(url)-1]

	# Open the page, get the contents, yadda yadda
	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html)
	head = soup.html.head

	head_links = head.findAll('link')
	for link in head_links:
		try: 
			# Likes this first
			if link['rel'] == "icon":
				if urllib.urlopen(link['href']).getcode() != 200:
					if link['href'].startswith("/"):
						link['href'] = link['href'][1:len(link['href'])]
					absolute_url = "http://%s/%s" % (url, link['href'])
				else:
					return link['href']

			# Will accept this as second.
			if link['rel'] == "shortcut icon":
				if urllib.urlopen(link['href']).getcode() != 200:
					if link['href'].startswith("/"):
						link['href'] = link['href'][1:len(link['href'])]
					absolute_url = "http://%s/%s" % (url, link['href'])
					return absolute_url
				else:
					return link['href']
		except:
			pass

	url = "%s/favicon.ico" % url
	if urllib.urlopen(url).getcode() == 200:
		return url 

	# You would probably change this on your site.
	# But it's my code, so yeah -- if I can't find
	# anything better, I'll just use my favicon.
	return "http://plumrss.com/favicon.ico"


# Example usage
#url = sys.argv[1]
#icon = get_favicon(url)
#print icon

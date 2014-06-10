import requests
import re
import os
import win32com.client
import time
import sys
from html.parser import HTMLParser


#class to parse the torrent sites and retrieve magnet links
class MyHTMLParser(HTMLParser):
    magnet = ""
    urls = []

    #function to retrieve magnet link by checking the a href tags
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    if value[0:7] == 'magnet:':
                        self.magnet = value
                    elif value.find('1337x') != -1:
                        self.urls.append(value)
                    elif value.find('kickass.to') != -1:
                        self.urls.append(value)
                    elif value.find('thepiratebay.org') != -1:
                        self.urls.append(value)
                    elif value.find('h33t.to') != -1:
                        self.urls.append(value)
                    elif value.find('torrentreactor.net') != -1:
                        self.urls.append(value)
#end of class


#function to get content from the websites as a text using 'requests'
def get_content(url):
    r = requests.get(url)
    return r.text


#general function for matching a pattern and returning the first match
def match_pattern(pattern, content):
    matches = re.search(pattern, content)
    return matches.group()

show_name = ""
parser = MyHTMLParser()

try:
    file = open("showname.txt", "r")
    file_content = file.readline()
    index = file_content.find(':')
    show_name = file_content[index+2:]
    file.close()

except FileNotFoundError:
    print('Please use user_input.py to specify the torrent you wish to download.')
    time.sleep(10)
    sys.exit()


search_url = "http://torrentz.in/search?f="+show_name

#get content of the torrent search results
main_content = get_content(search_url)
index = main_content.find('peers')

#all of the torrent links on the search results page for torrentz.in
#are in the for of '/40alphanumerics hence the regex to match
#and retrieve the first match as it is the one with highest peers
search_url = "http://torrentz.in/" + match_pattern("[a-zA-Z0-9]{40}",
                                                   main_content[index:-1])
#the main_content will now contain the page for torrent specific links i.e.
#links for a particular torrent such as 1337x h33t kickass etc
main_content = get_content(search_url)

#used the parser to find out if torrent is available at trusted sites
parser.feed(main_content)

#the main content will now contain the actual webpage where the magnet is found
main_content = get_content(parser.urls[0])

#feed the parser the webpage to find the magnet
parser.feed(main_content)

#start application associated with magnet eg bitcomet,utorrent
os.startfile(parser.magnet)
shell = win32com.client.Dispatch('WScript.Shell')
time.sleep(7)

#send an Enter key to the bitcomet to start the download
shell.SendKeys("{Enter}", 0)

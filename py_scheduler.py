import requests
import re
import os
import win32com.client
import time
from html.parser import HTMLParser


#Class to parse the torrent sites and retrieve magnet links
class MyHTMLParser(HTMLParser):
    torrents=[]
    
    #function to retrieve magnet link by checking the a href tags
    def handle_starttag(self, tag, attrs):
        if tag=='a':
            for name,value in attrs:
                if name=='href' and value[0:7]=='magnet:':
                    self.torrents.append(value)
#end of class


#function to get content from the websites as a text using 'requests'
def get_content(url):
    r = requests.get(url)
    return r.text

#general function for matching a pattern and returning the first match
def match_pattern(pattern,content):
    matches = re.search(pattern,content)
    return matches.group()


parser = MyHTMLParser()

#prompt the user for show name. show name should be as precise as possible with episode or season number. for example 'chuck season 1'
user_input = input("Please enter the show name you want to schedule a download for:") 
search_url = "http://torrentz.in/search?f="+user_input

#get content of the torrent search results
main_content = get_content(search_url)

#all of the torrent links on the search results page for torrentz.in are in the for of '/40alphanumerics hence the regex to match 
#and retrieve the first match as it is the one with highest peers
search_url = "http://torrentz.in/" + match_pattern("[a-zA-Z0-9]{40}",main_content)

#the main_content will now contain the page for torrent specific links i.e. links for a particular torrent such as 1337x h33t kickass etc
main_content = get_content(search_url)

#bunch of if-else-ifs to find whether the popular torrent sites are available. for the first match it redirects to that website
if main_content.find("1337x")!=-1:
    search_url = match_pattern("http://1337x.org/torrent/[0-9]{6}/0/",main_content)
elif main_content.find("kickass.to")!=-1:
    search_url = match_pattern("http://kickass.to/",main_content)
    
#the main content will now contain the actual webpage where the magnet is found
main_content = get_content(search_url)

#feed the parser the webpage to find the magnet
parser.feed(main_content)
magnet = parser.torrents[0]

#start application associated with magnet eg bitcomet,utorrent
os.startfile(magnet)
shell = win32com.client.Dispatch('WScript.Shell')
time.sleep(7)

#send an Enter key to the bitcomet to start the download
shell.SendKeys("{Enter}",0) 
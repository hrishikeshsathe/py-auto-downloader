import requests
import re
import os

def get_content(url):
    r = requests.get(url)
    return r.text


def match_pattern(pattern,content):
    matches = re.search(pattern,content)
    return matches.group()
    
user_input = input("Please enter the show name you want to schedule a download for:")
main_url = "http://torrentz.in/search?f="+user_input
main_content = get_content(main_url)
next_url = "http://torrentz.in/" + match_pattern("[a-zA-Z0-9]{40}",main_content)

main_content = get_content(next_url)
next_url = match_pattern("http://1337x.org/torrent/[0-9]{6}/0",main_content) + "/"

main_content = get_content(next_url)
magnet = match_pattern("magnet:[\W\w]*Fannounce",main_content)
os.startfile(magnet)
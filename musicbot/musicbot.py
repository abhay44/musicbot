#!/usr/bin/env python
import re
import json
import urllib
import os
import sys
import re
import requests
from bs4 import BeautifulSoup

url = 'http://cloud.dean.technology/api/top40/'

def extract_videos(html):
    """
    Parses given html and returns a list of (Title, Link) for
    every movie found.
    """
    soup = BeautifulSoup(html, 'html.parser')
    pattern = re.compile(r'/watch\?v=')
    found = soup.find_all('a', 'yt-uix-tile-link', href=pattern)
    return [(x.text.encode('utf-8'), x.get('href')) for x in found]

def get_request(url):

	req = requests.get(url)
	return req

def search_videos(query):
    """
    Searches for videos given a query
    """
    response = get_request('https://www.youtube.com/results?search_query=' + query)
    return extract_videos(response.content)

def fetch(url):
	"""
	fetch the top charts and print them
	"""
	req = get_request(url)
	req_var = req.json()
	for i in req_var['entries']:
		print(unicode(i['position'])+ unicode(' ') + i['title'] + unicode(' by ') + i['artist'])

def download(position):
	"""
	returns the title and artist name of the selected position

	"""
	request_download = requests.get(url)
	req = request_download.json()
	for i in req['entries']:
		if i['position'] == int(position):
			query = i['title'] + unicode(' by ') + i['artist']
			return query

def main():
    expected_arguments = ['yes','y','']
    print('Welcome to musicbot!! Do you want to fetch top40 charts?(y|n)')
    user_choice = raw_input()
    if user_choice not in expected_arguments:
        print('Exiting...')
        sys.exit()
    print('Fetching top40 charts...')
    fetch(url)
    song_choice = raw_input('Select one(give the position):')
    while not(song_choice.isdigit() or not(1 <= int(song_choice) <= 40)):
        print('Please try again!')
        song_choice = raw_input('Select one:')
    title = download(song_choice)
    print(title)
    result = search_videos(title)
    title_name,video_link = result[0]
    print(title_name,video_link)
    command_tokens = [
        'youtube-dl',
        '--continue '
        '--extract-audio',
        '--audio-format mp3',
        '--audio-quality 0',
        '--output \'%(title)s.%(ext)s\'',
        'https://www.youtube.com' + video_link]

    command = ' '.join(command_tokens)
    print('Downloading...')
    os.system(command)

if __name__ == '__main__':
    main()
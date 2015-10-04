#!/usr/bin/python

import requests
import re
import os.path
import datetime
import json

torrents_directory = './torrents/'
use_transmission = True
debug = True

movies_url = 'http://weburg.net/movies/new/?clever_title=1&template=0&last=0'
movie_id_regex = '\/movies\/info\/([0-9]+)'
torrent_regex = '(http?://\S+)\"'
torrent_file_regex = 'filename=\"(\S+)\"'
seeders_regex = '([0-9]+)\sseeders'
leechers_regeex = '([0-9]+)\sleechers'
torrent_format = 'http://weburg.net/ajax/download/movie?obj_id={0}'
transmission_show = '/usr/bin/transmission-show'
transmission_format = transmission_show + ' -s {0}'
settings_file = 'settings.json'

headers = {
    'Content-Type': 'text/html; charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0',
    'X-Requested-With': 'XMLHttpRequest'
}


def log(message):
    if not debug:
        return False

    print str(datetime.datetime.now()) + ': ' + message
    return True


def uniq(seq):
    seen = set()
    seen_add = seen.add

    return [x for x in seq if not (x in seen or seen_add(x))]


def load_settings():
    if not os.path.isfile(settings_file):
        log('Skip a loading settings from file. File does not exist')
        return False

    with open(settings_file) as data_file:
        try:
            data = json.load(data_file)
            return data
        except ValueError:
            log('Skip a loading settings from file. Incorrect file format')
            return False


def save_torrent(torrent):
    seeders, leechers = '0', '0'
    torrent_real = requests.get(torrent)

    torrent_file_re = re.compile(torrent_file_regex)
    disposition = torrent_real.headers['content-disposition']
    filename_header = torrent_file_re.findall(disposition)[0]
    filename = torrents_directory + filename_header

    if torrent_real.status_code != 200:
        log('Getting a torrent file. Wrong response code')
        return False

    if os.path.isfile(filename):
        log('Getting a torrent file. File "{0}" already exists'.format(filename))
        return False

    f = open(filename, 'wb')
    f.write(torrent_real.content)
    f.close()

    if use_transmission:
        tr_info = os.popen(transmission_format.format(filename)).read()
        seeders_ar = re.findall(seeders_regex, tr_info)
        if len(seeders_ar):
            seeders = seeders_ar[0]

        leechers_ar = re.findall(leechers_regeex, tr_info)
        if len(leechers_ar):
            leechers = leechers_ar[0]

    print filename + ';' + seeders + ';' + leechers

    return True


def save_torrents(torrents):
    total_saved = 0

    for torrent in torrents:
        if save_torrent(torrent):
            total_saved += 1

    return total_saved


def get_movie_ids():
    r = requests.get(movies_url, headers=headers)

    if r.status_code != 200:
        log('Getting a movie list. Wrong response code')
        return False

    data = r.json()
    if 'items' not in data:
        log('Getting a movie list. List not found')
        return False

    items = data['items']
    if not items:
        log('Getting a movie list. List is empty')
        return False

    ids = uniq(re.findall(movie_id_regex, items))
    return ids


def get_movie_torrents(movie_id):
    torrent_data_url = torrent_format.format(movie_id)
    torrent_data = requests.get(torrent_data_url)
    torrent_re = re.compile(torrent_regex)

    if torrent_data.status_code != 200:
        log('Getting a movie torrent list. Wrong response code')
        return False

    torrent_list = torrent_re.findall(torrent_data.text)

    if not torrent_list:
        log('Getting a movie torrent list. List is empty')
        return False

    return torrent_list


def main():
    if not os.path.isdir(torrents_directory):
        log('The destination directory does not exist')
        return 0

    if not os.access(torrents_directory, os.W_OK):
        log('The destination directory is not writable')
        return 0

    movie_ids = get_movie_ids()
    if not movie_ids:
        return 0

    total_saved = 0
    for movie_id in movie_ids:
        torrent_list = get_movie_torrents(movie_id)
        if not torrent_list:
            break

        total_saved += save_torrents(torrent_list)

    return total_saved

settings = load_settings()

if settings:
    torrents_directory = settings['torrents_directory']
    debug = settings['debug']
    use_transmission = settings['use_transmission']
    transmission_show = settings['transmission_show']
    headers['User-Agent'] = settings['user_agent']

if not os.path.isfile(transmission_show) and use_transmission:
    log('Switch use_transmission to False')
    use_transmission = False

torrents_saved = main()
log('Total saved torrents: ' + str(torrents_saved))

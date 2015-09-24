#!/usr/bin/python

import requests
import re
import os.path
import datetime

torrent_file_format = './torrents/{0}'
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
transmission_format = '{0} -s {1}'

headers = {
    'Content-Type': 'text/html; charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0',
    'X-Requested-With': 'XMLHttpRequest'
}


def log(message):
    if debug:
        print str(datetime.datetime.now()) + ': ' + message


def uniq(seq):
    seen = set()
    seen_add = seen.add

    return [x for x in seq if not (x in seen or seen_add(x))]


def save_torrent(torrent):
    seeders, leechers = '0', '0'
    torrent_real = requests.get(torrent)

    torrent_file_re = re.compile(torrent_file_regex)
    disposition = torrent_real.headers['content-disposition']
    filename_header = torrent_file_re.findall(disposition)[0]
    filename = torrent_file_format.format(filename_header)

    if torrent_real.status_code != 200:
        log('save_torrent. Wrong response code')
        return False

    if os.path.isfile(filename):
        log('save_torrent. File "{0}" already exists'.format(filename))
        log('save_torrent. Stopped')
        return False

    f = open(filename, 'wb')
    f.write(torrent_real.content)
    f.close()

    if use_transmission:
        tr_info = os.popen(transmission_format.format(transmission_show, filename)).read()
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
        if not save_torrent(torrent):
            break
        total_saved += 1

    return total_saved


def get_movie_ids():
    r = requests.get(movies_url, headers=headers)

    if r.status_code != 200:
        log('get_movie_ids. Wrong response code')
        return False

    data = r.json()
    if 'items' not in data:
        log('get_movie_ids. Movie list not found')
        return False

    items = data['items']
    if not items:
        log('get_movie_ids. Movie list is empty')
        return False

    ids = uniq(re.findall(movie_id_regex, items))
    return ids


def get_movie_torrents(movie_id):
    torrent_data_url = torrent_format.format(movie_id)
    torrent_data = requests.get(torrent_data_url)
    torrent_re = re.compile(torrent_regex)

    if torrent_data.status_code != 200:
        log('get_movie_torrents. Wrong response code')
        return False

    torrent_list = torrent_re.findall(torrent_data.text)

    if not torrent_list:
        log('get_movie_torrents. Torrent list is empty')
        return False

    return torrent_list


def main():
    total_saved = 0
    movie_ids = get_movie_ids()

    if not movie_ids:
        return 0

    for movie_id in movie_ids:
        torrent_list = get_movie_torrents(movie_id)
        if not torrent_list:
            break

        total_saved_by_movie = save_torrents(torrent_list)
        if not total_saved_by_movie:
            break

        total_saved += total_saved_by_movie

    return total_saved

if not os.path.isfile(transmission_show) and use_transmission:
    log('Switch use_transmission to False')
    use_transmission = False

torrents_saved = main()
log('Total saved torrents: ' + str(torrents_saved))

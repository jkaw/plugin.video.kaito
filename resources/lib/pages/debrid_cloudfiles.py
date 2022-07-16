# -*- coding: utf-8 -*-
from __future__ import division
from past.utils import old_div
import re
from ..common import source_utils
from ..modules.BrowserBase import BrowserBase
from ..debrid import real_debrid, premiumize, all_debrid
import requests
import threading

class sources(BrowserBase):
    def __init__(self):
        self.cloud_files = []
        self.threads = []

    def get_sources(self, debrid, query, episode, anilist_id):
        if debrid.get('real_debrid'):
            self.threads.append(
                threading.Thread(target=self.rd_cloud_inspection, args=(query, episode, anilist_id)))

        if debrid.get('premiumize'):
            self.threads.append(
                threading.Thread(target=self.premiumize_cloud_inspection, args=(query, episode, anilist_id)))

        if debrid.get('all_debrid'):
            self.threads.append(
                threading.Thread(target=self.alldebrid_cloud_inspection, args=(query, episode, anilist_id)))

        for i in self.threads:
            i.start()

        for i in self.threads:
            i.join()

        return self.cloud_files

    def rd_cloud_inspection(self, query, episode, anilist_id):
        api = real_debrid.RealDebrid()
        torrents = api.list_torrents()
        query = re.sub('[^A-Za-z0-9 ()]', ' ', query)
        episode = str(episode)
        show = requests.get("https://kaito-title.firebaseio.com/%s.json" % anilist_id).json()
        if show:
            if 'general_title' in show:
                show = show['general_title']
            query += ' (' + show + ')'
        filenames = [re.sub('[^A-Za-z0-9 ()]', '', i['filename']) for i in torrents]
        filenames_query = ','.join(filenames)
        resp = requests.get('https://armkai.vercel.app/api/fuzzypacks?dict={}&match={}'.format(filenames_query, query)).json()

        for i in resp:
            torrent = torrents[i]
            filename = re.sub(r'\[.*?\]', '', torrent['filename']).lower()

            if source_utils.is_file_ext_valid(filename) and not episode in filename.rsplit('-', 1)[1]:
                continue

            torrent_info = api.torrentInfo(torrent['id'])

            if not any(source_utils.is_file_ext_valid(tor_file['path'].lower()) for tor_file in
                       [selected for selected in torrent_info['files'] if selected['selected'] == 1]):
                continue

            for f_index, torrent_file in enumerate([cloud_file for cloud_file in torrent_info['files']
                                                    if cloud_file['selected'] == 1]):

                if source_utils.get_best_match('path', [torrent_file], episode):
                    self.cloud_files.append(
                        {
                            'quality': source_utils.getQuality(torrent['filename']),
                            'lang': source_utils.getAudio_lang(torrent['filename']),
                            'hash': torrent_info['links'][f_index],
                            'provider': 'Cloud',
                            'type': 'cloud',
                            'release_title': torrent['filename'],
                            'info': source_utils.getInfo(torrent['filename']),
                            'debrid_provider': 'real_debrid',
                            'size': '.%d GB' % (old_div((old_div(torrent_file['bytes'], 1024)), 1024))
                        }
                    )
                    break

    def premiumize_cloud_inspection(self, query, episode, anilist_id):
        cloud_items = premiumize.Premiumize().list_folder('')
        query = re.sub('[^A-Za-z0-9 ()]', ' ', query)
        episode = str(episode)
        show = requests.get("https://kaito-title.firebaseio.com/%s.json" % anilist_id).json()
        if show:
            if 'general_title' in show:
                show = show['general_title']
            query += ' (' + show + ')'
        filenames = [re.sub('[^A-Za-z0-9 ()]', '', i['name']) for i in cloud_items]
        filenames_query = ','.join(filenames)
        resp = requests.get('https://armkai.vercel.app/api/fuzzypacks?dict={}&match={}'.format(filenames_query, query)).json()

        for i in resp:
            torrent = cloud_items[i]
            filename = re.sub(r'\[.*?\]', '', torrent['name']).lower()

            if torrent['type'] == 'file' and source_utils.is_file_ext_valid(filename):
                if episode in filename.rsplit('-', 1)[1]:
                    self._add_premiumize_cloud_item(torrent)
                else:
                    continue

            torrent_folder = premiumize.Premiumize().list_folder(torrent['id'])
            identified_file = source_utils.get_best_match('name', torrent_folder, episode)
            self._add_premiumize_cloud_item(identified_file)

    def alldebrid_cloud_inspection(self, query, episode, anilist_id):
        api = all_debrid.AllDebrid()
        magnets = [m for m in api.saved_magnets() if m['status'] == "Ready"]
        cloud_items = [i for link_list in magnets for i in link_list['links']] + self.api_adapter.saved_links()['links']
        query = re.sub('[^A-Za-z0-9 ()]', ' ', query)
        episode = str(episode)
        show = requests.get("https://kaito-title.firebaseio.com/%s.json" % anilist_id).json()
        if show:
            if 'general_title' in show:
                show = show['general_title']
            query += ' (' + show + ')'
        filenames = [re.sub('[^A-Za-z0-9 ()]', '', i['filename']) for i in cloud_items]
        filenames_query = ','.join(filenames)
        resp = requests.get('https://armkai.vercel.app/api/fuzzypacks?dict={}&match={}'.format(filenames_query, query)).json()
        ## finish up


    def _add_premiumize_cloud_item(self, item):
        self.cloud_files.append({
            'quality': source_utils.getQuality(item['name']),
            'lang': source_utils.getAudio_lang(item['name']),
            'hash': premiumize.Premiumize()._fetch_transcode_or_standard(item),
            'provider': 'Cloud',
            'type': 'cloud',
            'release_title': item['name'],
            'info': source_utils.getInfo(item['name']),
            'debrid_provider': 'premiumize',
            'size': '.%d GB' %(old_div((old_div(int(item['size']), 1024)), 1024))
        })

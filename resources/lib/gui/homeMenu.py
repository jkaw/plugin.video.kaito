# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.modules.globals import g


class Menus:

    @staticmethod
    def home():
        if g.anilist_enabled():
            g.add_directory_item('Anilist',
                                 action='watchlist',
                                 action_args={"flavor": 'anilist'},
                                 description='Open Anilist Watchlists')

        if g.myanimelist_enabled():
            g.add_directory_item('MyAnimeList',
                                 action='watchlist',
                                 action_args={"flavor": 'mal'},
                                 description='Open MyAnimeList Watchlists')
        if g.kitsu_enabled():
            g.add_directory_item('Kitsu',
                                 action='watchlist',
                                 action_args={"flavor": 'kitsu'},
                                 description='Open Kitsu Watchlists')
        g.add_directory_item(g.get_language_string(30001),
                             action='anilist_airing',
                             description=g.get_language_string(30364))
        g.add_directory_item(g.get_language_string(30002),
                             action='airing_dub',
                             description=g.get_language_string(30365))
        g.add_directory_item(g.get_language_string(30003),
                             action='latest',
                             description=g.get_language_string(30369))
        g.add_directory_item(g.get_language_string(30004),
                             action='latest_dub',
                             description=g.get_language_string(30370))
        g.add_directory_item(g.get_language_string(30005),
                             action='anilist_trending',
                             description=g.get_language_string(30370))
        g.add_directory_item(g.get_language_string(30006),
                             action='anilist_popular',
                             description=g.get_language_string(30370))
        g.add_directory_item(g.get_language_string(30007),
                             action='anilist_upcoming',
                             description=g.get_language_string(30370))
        g.add_directory_item(g.get_language_string(30008),
                             action='anilist_all_time_popular',
                             description=g.get_language_string(30370))
        g.add_directory_item(g.get_language_string(30009),
                             action='anilist_genres',
                             description=g.get_language_string(30370))
        g.add_directory_item(g.get_language_string(30010),
                             action='search_history',
                             description=g.get_language_string(30370))
        if g.debrid_available():
            g.add_directory_item(g.get_language_string(30173),
                                 action='myFiles',
                                 description=g.get_language_string(30368))
        g.add_directory_item(g.get_language_string(30011),
                             action='tools',
                             description=g.get_language_string(30370))
        g.close_directory(g.CONTENT_MENU)

    @staticmethod
    def tools_menu():
        g.add_directory_item(g.get_language_string(30040),
                             action='settings',
                             description=g.get_language_string(30377))
        g.add_directory_item(g.get_language_string(30028),
                             action='clearCache',
                             is_folder=False,
                             description=g.get_language_string(30379))
        g.add_directory_item(g.get_language_string(30039),
                             action='clearTorrentCache',
                             is_folder=False,
                             description=g.get_language_string(30380))
        g.add_directory_item(g.get_language_string(30180),
                             action='clear_history',
                             is_folder=False,
                             description=g.get_language_string(30381))
        g.add_directory_item(g.get_language_string(30218),
                             action='rebuild_database',
                             is_folder=False,
                             description=g.get_language_string(30382))
        g.add_directory_item(g.get_language_string(30041),
                             action='wipe_addon_data',
                             is_folder=False,
                             description=g.get_language_string(30383))
        g.close_directory(g.CONTENT_MENU)

    @staticmethod
    def test_windows():
        g.add_directory_item(g.get_language_string(30462),
                             action='testPlayingNext',
                             is_folder=False,
                             description=g.get_language_string(30391))
        g.add_directory_item(g.get_language_string(30463),
                             action='testStillWatching',
                             is_folder=False,
                             description=g.get_language_string(30392))
        g.add_directory_item(g.get_language_string(30613),
                             action='testGetSourcesWindow',
                             is_folder=False,
                             description=g.get_language_string(30614))
        g.add_directory_item(g.get_language_string(30464),
                             action='testResolverWindow',
                             is_folder=False,
                             description=g.get_language_string(30393))
        g.add_directory_item(g.get_language_string(30465),
                             action='testSourceSelectWindow',
                             is_folder=False,
                             description=g.get_language_string(30394))
        g.add_directory_item(g.get_language_string(30466),
                             action='testManualCacheWindow',
                             is_folder=False,
                             description=g.get_language_string(30460))
        g.add_directory_item(g.get_language_string(30626),
                             action='testDownloadManagerWindow',
                             is_folder=False,
                             description=g.get_language_string(30625))
        g.close_directory(g.CONTENT_MENU)

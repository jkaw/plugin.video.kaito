# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import xbmc
import xbmcgui

"""
    Dispatch module
"""
from resources.lib.modules.globals import g
from resources.lib.modules.exceptions import NoPlayableSourcesException


def dispatch(params):
    url = params.get("url")
    action = params.get("action")
    action_args = params.get("action_args")
    pack_select = params.get("packSelect")
    source_select = params.get("source_select") == "true"
    overwrite_cache = params.get("kaito_reload") == "true"
    resume = params.get("resume")
    force_resume_check = params.get("forceresumecheck") == "true"
    force_resume_off = params.get("forceresumeoff") == "true"
    force_resume_on = params.get("forceresumeon") == "true"
    smart_url_arg = params.get("smartPlay") == "true"
    mediatype = params.get("mediatype")
    endpoint = params.get("endpoint")

    g.log("Kaito, Running Path - {}".format(g.REQUEST_PARAMS))

    if action is None:
        from resources.lib.gui import homeMenu

        homeMenu.Menus().home()

        from resources.lib.modules.WatchlistIntegration import WATCHLIST_WATCHED_UPDATE
        WATCHLIST_WATCHED_UPDATE('', {'modal': 'false'})

    elif action == "forceResumeShow":
        from resources.lib.modules import smartPlay
        from resources.lib.common import tools

        smartPlay.SmartPlay(tools.get_item_information(action_args)).resume_show()

    elif action == "colorPicker":
        g.color_picker()

    elif action == "anilist_airing":
        from resources.lib.modules.AniListBrowser import AniListBrowser
        from resources.lib.modules.KaitoBrowser import KaitoBrowser
        from resources.lib.gui.windows.anichart import Anichart

        _TITLE_LANG = g.get_setting("titlelanguage")
        _ANILIST_BROWSER = AniListBrowser(_TITLE_LANG)
        airing = _ANILIST_BROWSER.get_airing()

        anime = Anichart(*('anichart.xml', g.ADDON_DATA_PATH),
                         get_anime=KaitoBrowser().get_anime_init, anime_items=airing).doModal()
        return

    elif action == "airing_dub":
        from resources.lib.modules.KaitoBrowser import KaitoBrowser
        KaitoBrowser().get_airing_dub()

    elif action == "latest":
        from resources.lib.modules.KaitoBrowser import KaitoBrowser
        KaitoBrowser().get_latest(g.real_debrid_enabled(), g.premiumize_enabled())

    elif action == "latest_dub":
        from resources.lib.modules.KaitoBrowser import KaitoBrowser
        KaitoBrowser().get_latest_dub(g.real_debrid_enabled(), g.premiumize_enabled())

    elif action == "anilist_trending":
        from resources.lib.modules.AniListBrowser import AniListBrowser
        _TITLE_LANG = g.get_setting("titlelanguage")
        _ANILIST_BROWSER = AniListBrowser(_TITLE_LANG)
        _ANILIST_BROWSER.get_trending()

    elif action == "anilist_popular":
        from resources.lib.modules.AniListBrowser import AniListBrowser
        _TITLE_LANG = g.get_setting("titlelanguage")
        _ANILIST_BROWSER = AniListBrowser(_TITLE_LANG)
        _ANILIST_BROWSER.get_popular()

    elif action == "anilist_upcoming":
        from resources.lib.modules.AniListBrowser import AniListBrowser
        _TITLE_LANG = g.get_setting("titlelanguage")
        _ANILIST_BROWSER = AniListBrowser(_TITLE_LANG)
        _ANILIST_BROWSER.get_upcoming()

    elif action == "anilist_all_time_popular":
        from resources.lib.modules.AniListBrowser import AniListBrowser
        _TITLE_LANG = g.get_setting("titlelanguage")
        _ANILIST_BROWSER = AniListBrowser(_TITLE_LANG)
        _ANILIST_BROWSER.get_all_time_popular()

    elif action == "anilist_genres":
        from resources.lib.modules.AniListBrowser import AniListBrowser
        _TITLE_LANG = g.get_setting("titlelanguage")
        _ANILIST_BROWSER = AniListBrowser(_TITLE_LANG)
        _ANILIST_BROWSER.get_genres()

    elif action == "anilist_genres_page":
        from resources.lib.modules.AniListBrowser import AniListBrowser
        from resources.lib.common import tools
        _TITLE_LANG = g.get_setting("titlelanguage")
        _ANILIST_BROWSER = AniListBrowser(_TITLE_LANG)
        genres_tags = params.get('action_args')
        _ANILIST_BROWSER.select_genres(xbmcgui.Dialog().multiselect('Genres & Tags', genres_tags))

    elif action == "search_history":
        from resources.lib.database.searchHistory import SearchHistory
        history = SearchHistory().get_search_history("show")
        if "Yes" in g.get_setting('searchhistory'):
            from resources.lib.modules.KaitoBrowser import KaitoBrowser
            KaitoBrowser().search_history(history)
        else:
            from resources.lib.modules.AniListBrowser import AniListBrowser
            _TITLE_LANG = g.get_setting("titlelanguage")
            _ANILIST_BROWSER = AniListBrowser(_TITLE_LANG)
            if isinstance(action_args, dict):
                query = action_args['query']
            else:
                query = g.get_keyboard_input()
            if not query:
                return False

            if "Yes" in g.get_setting('searchhistory'):
                SearchHistory().add_search_history("show", query)

            _ANILIST_BROWSER.get_search(query)

    elif action == "search":
        if isinstance(action_args, dict):
            query = action_args['query']
        else:
            query = g.get_keyboard_input()
        if not query:
            return False

        if "Yes" in g.get_setting('searchhistory'):
            from resources.lib.database.searchHistory import SearchHistory
            SearchHistory().add_search_history("show", query)
        from resources.lib.modules.AniListBrowser import AniListBrowser
        _TITLE_LANG = g.get_setting("titlelanguage")
        _ANILIST_BROWSER = AniListBrowser(_TITLE_LANG)
        if g.get_bool_setting("general.menus"):
            action_args = params.get('action_args')
            if isinstance(action_args, dict):
                g.draw_items(_ANILIST_BROWSER.get_search(query, (int(action_args['page']))))
            else:
                g.draw_items(_ANILIST_BROWSER.get_search(query))
        else:
            _ANILIST_BROWSER.get_search(query)

    elif action == "tools":
        from resources.lib.gui import homeMenu
        homeMenu.Menus().tools_menu()

    elif action == "showEpisodes":
        from resources.lib.modules.KaitoBrowser import KaitoBrowser
        KaitoBrowser().show_seasons(action_args)

    elif action == "malSeasonEpisodes":
        from resources.lib.modules.KaitoBrowser import KaitoBrowser
        KaitoBrowser().mal_season_episodes(action_args)

    #elif action == "showSeasons":
        # From Kitsu - movie
     #  from resources.lib.modules.KaitoBrowser import KaitoBrowser
     #  KaitoBrowser().show_seasons(action_args)

    elif action == "getSources":
        from resources.lib.modules.smartPlay import SmartPlay
        from resources.lib.common import tools

        anilist_id = action_args['anilist_id']
        item_information = tools.get_episode_information(anilist_id, action_args["episode"])
        item_information['info']['mediatype'] = g.MEDIA_EPISODE
        smart_play = SmartPlay(item_information)
        background = None
        resolver_window = None

        try:
            # Check to confirm user has a debrid provider authenticated and enabled
            if not g.premium_check():
                xbmcgui.Dialog().ok(
                    g.ADDON_NAME,
                    tools.create_multiline_message(
                        line1=g.get_language_string(30186),
                        line2=g.get_language_string(30187),
                    ),
                )
                return None

            # workaround for widgets not generating a playlist on playback request
            play_list = smart_play.playlist_present_check(smart_url_arg)

            if play_list:
                g.log("Cancelling non playlist playback", "warning")
                xbmc.Player().play(g.PLAYLIST)
                return

            resume_time = smart_play.handle_resume_prompt(
                resume, force_resume_off, force_resume_on, force_resume_check
            )
            #background = helpers.show_persistent_window_if_required(item_information)
            # Clear out last resolved title for a show if we are doing a rescrape
            if overwrite_cache and item_information['info']['mediatype'] == g.MEDIA_EPISODE:
                g.clear_runtime_setting(
                    "last_resolved_release_title.{}".format(item_information['info']['trakt_show_id'])
                )

            # Get Sources
            from resources.lib.modules.KaitoBrowser import KaitoBrowser
            sources = KaitoBrowser().get_sources(anilist_id, action_args["episode"], "", 'show')
            if background:
                background.set_process_started()
            item_information['episode'] = action_args["episode"]
            # Sort sources
            # sources = sources_helper.sort_sources(ii, sources_list)
            if sources is None:
                return

            # Select and resolve source
            if item_information['info']['mediatype'] == g.MEDIA_EPISODE:
                source_select_style = "Episodes"
            else:
                source_select_style = "Movie"

            if (
                g.get_int_setting("general.playstyle{}".format(source_select_style))
                == 1
                or source_select
            ):

                if background:
                    background.set_text(g.get_language_string(30178))
                from resources.lib.gui.windows.source_select import SourceSelect

                _mock_args = {"anilist_id": anilist_id}
                stream_link = SourceSelect(*('source_select.xml', g.ADDON_DATA_PATH),
                            actionArgs=_mock_args, sources=sources).doModal()
            else:
                if background:
                    background.set_text(g.get_language_string(30031))
                from resources.lib.gui.windows.resolver import Resolver
                _mock_args = {"anilist_id": anilist_id}
                resolver = Resolver(*('resolver.xml', g.ADDON_DATA_PATH),
                                    actionArgs=_mock_args)
                stream_link = resolver.doModal(sources, {}, False)

                if stream_link is None:
                    g.close_busy_dialog()
                    g.notification(
                        g.ADDON_NAME, g.get_language_string(30032), time=5000
                    )

            g.show_busy_dialog()

            if background:
                try:
                    background.close()
                finally:
                    del background

            if not stream_link:
                raise NoPlayableSourcesException

            from resources.lib.modules import player

            try:
                kaito_player = player.KaitoPlayer()
                kaito_player.play_source(
                    stream_link, item_information, resume_time=resume_time
                )
            finally:
                del kaito_player

        except NoPlayableSourcesException:
            try:
                background.close()
                del background
            except (UnboundLocalError, AttributeError):
                pass
            try:
                resolver_window.close()
                del resolver_window
            except (UnboundLocalError, AttributeError):
                pass

            g.cancel_playback()

    elif action == "playMovie":
        from resources.lib.modules.smartPlay import SmartPlay
        from resources.lib.common import tools

        if action_args.get("mal_id"):
            item_information = tools.get_item_information_mal(action_args["mal_id"])
            anilist_id = item_information["anilist_id"]
            item_information = tools.get_item_information(anilist_id)
        else:
            anilist_id = action_args['anilist_id']
            item_information = tools.get_item_information(anilist_id)
        item_information['info']['mediatype'] = g.MEDIA_MOVIE
        action_args["episode"] = 1
        smart_play = SmartPlay(item_information)
        background = None
        resolver_window = None

        try:
            # Check to confirm user has a debrid provider authenticated and enabled
            if not g.premium_check():
                xbmcgui.Dialog().ok(
                    g.ADDON_NAME,
                    tools.create_multiline_message(
                        line1=g.get_language_string(30186),
                        line2=g.get_language_string(30187),
                    ),
                )
                return None

            # workaround for widgets not generating a playlist on playback request
            play_list = smart_play.playlist_present_check(smart_url_arg)

            if play_list:
                g.log("Cancelling non playlist playback", "warning")
                xbmc.Player().play(g.PLAYLIST)
                return

            resume_time = smart_play.handle_resume_prompt(
                resume, force_resume_off, force_resume_on, force_resume_check
            )
            #background = helpers.show_persistent_window_if_required(item_information)

            # Get Sources
            from resources.lib.modules.KaitoBrowser import KaitoBrowser
            sources = KaitoBrowser().get_sources(anilist_id, '1', "", 'movie')
            if background:
                background.set_process_started()

            # Sort sources
            # sources = sources_helper.sort_sources(ii, sources_list)
            if sources is None:
                return

            # Select and resolve source
            if item_information['info']['mediatype'] == g.MEDIA_EPISODE:
                source_select_style = "Episodes"
            else:
                source_select_style = "Movie"

            if (
                g.get_int_setting("general.playstyle{}".format(source_select_style))
                == 1
                or source_select
            ):

                if background:
                    background.set_text(g.get_language_string(30178))
                from resources.lib.gui.windows.source_select import SourceSelect

                xbmc.sleep(750)
                _mock_args = {"anilist_id": anilist_id}
                stream_link = SourceSelect(*('source_select.xml', g.ADDON_DATA_PATH),
                            actionArgs=_mock_args, sources=sources).doModal()
            else:
                if background:
                    background.set_text(g.get_language_string(30031))
                from resources.lib.gui.windows.resolver import Resolver
                _mock_args = {"anilist_id": anilist_id}
                resolver = Resolver(*('resolver.xml', g.ADDON_DATA_PATH),
                                    actionArgs=_mock_args)
                stream_link = resolver.doModal(sources, {}, False)

                if stream_link is None:
                    g.close_busy_dialog()
                    g.notification(
                        g.ADDON_NAME, g.get_language_string(30032), time=5000
                    )

            g.show_busy_dialog()

            if background:
                try:
                    background.close()
                finally:
                    del background

            if not stream_link:
                raise NoPlayableSourcesException

            from resources.lib.modules import player

            try:
                kaito_player = player.KaitoPlayer()
                kaito_player.play_source(
                    stream_link, item_information, resume_time=resume_time
                )
            finally:
                del kaito_player

        except NoPlayableSourcesException:
            try:
                background.close()
                del background
            except (UnboundLocalError, AttributeError):
                pass
            try:
                resolver_window.close()
                del resolver_window
            except (UnboundLocalError, AttributeError):
                pass

            g.cancel_playback()

    elif action == "preScrape":

        from resources.lib.database.skinManager import SkinManager
        from resources.lib.modules import helpers

        try:
            from resources.lib.common import tools

            item_information = tools.get_item_information(action_args)

            # Get Sources
            sources_helper = helpers.SourcesHelper()
            uncached, sources_list, ii = sources_helper.get_sources(action_args)

            # Sort sources
            sources = sources_helper.sort_sources(ii, sources_list)
            if sources is None:
                return

            if item_information["info"]["mediatype"] == g.MEDIA_EPISODE:
                source_select_style = "Episodes"
            else:
                source_select_style = "Movie"
            if (
                g.get_int_setting("general.playstyle{}".format(source_select_style))
                == 0
                and sources
            ):
                from resources.lib.modules import resolver

                helpers.Resolverhelper().resolve_silent_or_visible(
                    sources, ii, pack_select
                )
        finally:
            g.set_runtime_setting("tempSilent", False)

        g.log("Pre-scraping completed")

    elif action == "authRealDebrid":
        from resources.lib.debrid import real_debrid

        real_debrid.RealDebrid().auth()
        g.open_addon_settings(3, 27)

    elif action == "searchMenu":
        from resources.lib.gui import homeMenu

        homeMenu.Menus().search_menu()

    elif action == "toolsMenu":
        from resources.lib.gui import homeMenu

        homeMenu.Menus().tools_menu()

    elif action == "clearCache":
        from resources.lib.common import tools

        g.clear_cache()

    elif action == "cacheAssist":
        from resources.lib.modules.cacheAssist import CacheAssistHelper

        CacheAssistHelper().auto_cache(action_args)

    elif action == "clearTorrentCache":
        from resources.lib.database.torrentCache import TorrentCache

        TorrentCache().clear_all()

    elif action == "settings":
        xbmc.executebuiltin("Addon.OpenSettings({})".format(g.ADDON_ID))

    elif action == "myTraktLists":
        from resources.lib.modules.listsHelper import ListsHelper

        ListsHelper().my_trakt_lists(mediatype)

    elif action == "myLikedLists":
        from resources.lib.modules.listsHelper import ListsHelper

        ListsHelper().my_liked_lists(mediatype)

    elif action == "TrendingLists":
        from resources.lib.modules.listsHelper import ListsHelper

        ListsHelper().trending_lists(mediatype)

    elif action == "PopularLists":
        from resources.lib.modules.listsHelper import ListsHelper

        ListsHelper().popular_lists(mediatype)

    elif action == "traktList":
        from resources.lib.modules.listsHelper import ListsHelper

        ListsHelper().get_list_items()

    elif action == "nonActiveAssistClear":
        from resources.lib.gui import debridServices

        debridServices.Menus().assist_non_active_clear()

    elif action == "debridServices":
        from resources.lib.gui import debridServices

        debridServices.Menus().home()

    elif action == "cacheAssistStatus":
        from resources.lib.gui import debridServices

        debridServices.Menus().get_assist_torrents()

    elif action == "premiumize_transfers":
        from resources.lib.gui import debridServices

        debridServices.Menus().list_premiumize_transfers()

    elif action == "showsNextUp":
        from resources.lib.gui import tvshowMenus

        tvshowMenus.Menus().my_next_up()

    elif action == "showsNew":
        from resources.lib.gui import tvshowMenus

        tvshowMenus.Menus().shows_new()

    elif action == "realdebridTransfers":
        from resources.lib.gui import debridServices

        debridServices.Menus().list_rd_transfers()

    elif action == "cleanInstall":
        from resources.lib.common import maintenance

        maintenance.wipe_install()

    elif action == "removeSearchHistory":
        from resources.lib.database.searchHistory import SearchHistory

        SearchHistory().remove_search_history(mediatype, endpoint)
        g.container_refresh()

    elif action == "clear_history":
        from resources.lib.database.searchHistory import SearchHistory

        SearchHistory().clear_search_history(mediatype)

    elif action == "myFiles":
        from resources.lib.gui import myFiles

        myFiles.Menus().home()

    elif action == "myFilesFolder":
        from resources.lib.gui import myFiles

        myFiles.Menus().my_files_folder(action_args)

    elif action == "myFilesPlay":
        from resources.lib.gui import myFiles

        myFiles.Menus().my_files_play(action_args)

    elif action == "rebuild_database":
        from resources.lib.database.trakt_sync import TraktSyncDatabase
        from resources.lib.database.anilist_sync import AnilistSyncDatabase

        TraktSyncDatabase().re_build_database()
        AnilistSyncDatabase().re_build_database()

    elif action == "cleanOrphanedMetadata":
        from resources.lib.database.trakt_sync import TraktSyncDatabase

        trakt_db = TraktSyncDatabase()
        trakt_db.clean_orphaned_metadata()

    elif action == "myUpcomingEpisodes":
        from resources.lib.gui import tvshowMenus

        tvshowMenus.Menus().my_upcoming_episodes()

    elif action == "myWatchedEpisodes":
        from resources.lib.gui import tvshowMenus

        tvshowMenus.Menus().my_watched_episode()

    elif action == "myWatchedMovies":
        from resources.lib.gui import movieMenus

        movieMenus.Menus().my_watched_movies()

    elif action == "showsByActor":
        from resources.lib.gui import tvshowMenus

        tvshowMenus.Menus().shows_by_actor(action_args)

    elif action == "movieByActor":
        from resources.lib.gui import movieMenus

        movieMenus.Menus().movies_by_actor(action_args)

    elif action == "flatEpisodes":
        from resources.lib.gui.tvshowMenus import Menus

        Menus().flat_episode_list(action_args)

    elif action == "runPlayerDialogs":
        from resources.lib.modules.player import PlayerDialogs

        player_dialogs = PlayerDialogs()
        player_dialogs.display_dialog()
        del player_dialogs

    elif action == "runPlayerSkipIntro":
        from resources.lib.modules.player import PlayerDialogs

        player_dialogs = PlayerDialogs()
        player_dialogs.display_skip_intro()
        del player_dialogs

    elif action == "authAllDebrid":
        from resources.lib.debrid.all_debrid import AllDebrid

        AllDebrid().auth()
        g.open_addon_settings(3, 36)

    elif action == "authPremiumize":
        from resources.lib.debrid.premiumize import Premiumize

        Premiumize().auth()
        g.open_addon_settings(3, 13)

    elif action == "watchlist_login_anilist":
        from resources.lib.modules import WatchlistIntegration
        return WatchlistIntegration.WL_LOGIN_ANILIST(None, None)

    elif action == "watchlist_login_mal":
        from resources.lib.modules import WatchlistIntegration
        return WatchlistIntegration.WL_LOGIN_MAL(None, None)

    elif action == "watchlist_login_kitsu":
        from resources.lib.modules import WatchlistIntegration
        return WatchlistIntegration.WL_LOGIN_KITSU(None, None)

    elif action == "watchlist_logout":
        from resources.lib.modules import WatchlistIntegration
        return WatchlistIntegration.WL_LOGOUT(None, params)

    elif action == "watchlist":
        from resources.lib.modules import WatchlistIntegration
        return WatchlistIntegration.WATCHLIST(None, params)

    elif action == "watchlist_status_type":
        from resources.lib.modules import WatchlistIntegration
        return WatchlistIntegration.WATCHLIST_STATUS_TYPE(None, params)

    elif action == "watchlist_status_type_pages":
        from resources.lib.modules import WatchlistIntegration
        return WatchlistIntegration.WATCHLIST_STATUS_TYPE_PAGES(None, params)

    elif action == "watchlist_watched_update":
        from resources.lib.modules import WatchlistIntegration
        return WatchlistIntegration.WATCHLIST_WATCHED_UPDATE(None, params)

    elif action == "testWindows":
        from resources.lib.gui.homeMenu import Menus

        Menus().test_windows()

    elif action == "testPlayingNext":
        from resources.lib.gui import mock_windows

        mock_windows.mock_playing_next()

    elif action == "testStillWatching":
        from resources.lib.gui import mock_windows

        mock_windows.mock_still_watching()

    elif action == "testGetSourcesWindow":
        from resources.lib.gui import mock_windows

        mock_windows.mock_get_sources()

    elif action == "testResolverWindow":
        from resources.lib.gui import mock_windows

        mock_windows.mock_resolver()

    elif action == "testSourceSelectWindow":
        from resources.lib.gui import mock_windows

        mock_windows.mock_source_select()

    elif action == "testManualCacheWindow":
        from resources.lib.gui import mock_windows

        mock_windows.mock_cache_assist()

    elif action == "showsRecentlyWatched":
        from resources.lib.gui.tvshowMenus import Menus

        Menus().shows_recently_watched()

    elif action == "toggleLanguageInvoker":
        from resources.lib.common.maintenance import toggle_reuselanguageinvoker
        toggle_reuselanguageinvoker()

    elif action == "runMaintenance":
        from resources.lib.common.maintenance import run_maintenance
        run_maintenance()

    elif action == "torrentCacheCleanup":
        from resources.lib.database import torrentCache
        torrentCache.TorrentCache().do_cleanup()

    elif action == "chooseTimeZone":
        from resources.lib.modules.manual_timezone import choose_timezone
        choose_timezone()

    elif action == "widgetRefresh":
        if_playing = params.get('playing')
        if if_playing is not None:
            if_playing = False if if_playing.lower() == "false" else True if if_playing.lower() == "true" else None
        if if_playing is not None:
            g.trigger_widget_refresh(if_playing=if_playing)
        else:
            g.trigger_widget_refresh()

    elif action == "updateLocalTimezone":
        g.init_local_timezone()

    elif action == "chooseFilters":
        import resources.lib.gui.windows.filter_select as filter_select

        try:
            window = filter_select.FilterSelect("filter_select.xml", g.ADDON_PATH)
            window.doModal()
        finally:
            del window

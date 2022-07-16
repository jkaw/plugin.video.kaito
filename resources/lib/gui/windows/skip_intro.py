# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from resources.lib.gui.windows.smartplay_window_skip_intro import SmartPlayWindowSkipIntro


class SkipIntro(SmartPlayWindowSkipIntro):

    def __init__(self, xml_file, xml_location):

        try:
            super(SkipIntro, self).__init__(xml_file, xml_location)
            self.default_action = 1
        except:
            import traceback
            traceback.print_exc()

    def smart_play_action(self):
        if (
            self.default_action == 1
            and self.playing_file == self.getPlayingFile()
            and not self.closed
        ):
            self.pause()

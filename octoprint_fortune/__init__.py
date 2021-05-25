"""
# Introduction

`fortune` is a stripped-down implementation of the classic BSD Unix
`fortune` command. It combines the capabilities of the `strfile` command
(which produces the fortune index file) and the `fortune` command (which
displays a random fortune). It reads the traditional `fortune` program's
text file format.

"""
# from __future__ import absolute_import

import codecs
import os
import random
import re
import sys
from optparse import OptionParser

import flask
import octoprint.plugin


class FortunePlugin(
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
):
    def _random_int(self, start, end):
        try:
            # Use SystemRandom, if it's available, since it's likely to have
            # more entropy.
            r = random.SystemRandom()
        except:
            r = random

        return r.randint(start, end)

    def _read_fortunes(self, fortune_file):
        """ Yield fortunes as lists of lines """
        with codecs.open(fortune_file, mode="r", encoding="utf-8") as f:
            contents = f.read()

        lines = [line.rstrip() for line in contents.split("\n")]

        delim = re.compile(r"^%$")

        fortunes = []
        cur = []

        def save_if_nonempty(buf):
            fortune = "\n".join(buf)
            if fortune.strip():
                fortunes.append(fortune)

        for line in lines:
            if delim.match(line):
                save_if_nonempty(cur)
                cur = []
                continue

            cur.append(line)

        if cur:
            save_if_nonempty(cur)

        return fortunes

    def get_random_fortune(self, fortune_file):
        """
        Get a random fortune from the specified file.

        :Parameters:
            fortune_file : str
                path to file containing fortune cookies

        :rtype:  str
        :return: the random fortune
        """
        fortunes = list(self._read_fortunes(fortune_file))
        randomRecord = self._random_int(0, len(fortunes) - 1)
        return fortunes[randomRecord]

    def fortune(self):

        fortune_file = self._basefolder + "/fortunes"
        fortune = self.get_random_fortune(fortune_file)
        # self._logger.info(f"fortune: {fortune}")
        return fortune

    def on_api_get(self, request):

        self._logger.debug("The fortune button was pressed...")
        self._logger.debug(f"request = {request}")

        your_fortune = self.fortune()

        self._logger.debug(f"Your fortune: {your_fortune}")

        return flask.make_response(
            flask.jsonify(result=True, error=None, data=your_fortune)
        )

    def get_template_configs(self):
        return [
            {"type": "navbar", "custom_bindings": True},
        ]

    def on_after_startup(self):

        self._logger.info("--------------------------------------------")
        self._logger.info(f"Fortune started: {self._plugin_version}")
        self._logger.info("--------------------------------------------")

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            "push_message": None,
            "show_navbar_button": True,
            # put your plugin's default settings here
        }

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/fortune.js"], css=["css/fortune.css"], less=["less/fortune.less"]
        )

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return dict(
            fortune=dict(
                displayName="Fortune Plugin",
                displayVersion=self._plugin_version,
                # version check: github repository
                type="github_release",
                user="berrystephenw",
                repo="OctoPrint-Fortune",
                current=self._plugin_version,
                # update method: pip
                pip="https://github.com/berrystephenw/OctoPrint-Fortune/archive/{target_version}.zip",
            )
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Fortune Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
# __plugin_pythoncompat__ = ">=2.7,<3" # only python 2
__plugin_pythoncompat__ = ">=3,<4"  # only python 3
# __plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = FortunePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

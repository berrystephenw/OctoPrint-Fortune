# coding=utf-8

"""
# Introduction

`fortune` is a stripped-down implementation of the classic BSD Unix
`fortune` command. It combines the capabilities of the `strfile` command
(which produces the fortune index file) and the `fortune` command (which
displays a random fortune). It reads the traditional `fortune` program's
text file format.

"""
from __future__ import absolute_import

import octoprint.plugin
import random
import os
import sys
import codecs
import re

from optparse import OptionParser


class FortunePlugin(octoprint.plugin.SettingsPlugin,
                    octoprint.plugin.AssetPlugin,
                    octoprint.plugin.TemplatePlugin):

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
        with codecs.open(fortune_file, mode='r', encoding='utf-8') as f:
            contents = f.read()

        lines = [line.rstrip() for line in contents.split('\n')]

        delim = re.compile(r'^%$')

        fortunes = []
        cur = []

        def save_if_nonempty(buf):
            fortune = '\n'.join(buf)
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
        Get a random fortune from the specified file. Barfs if the corresponding
        `.dat` file isn't present.

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
        """
        Main program.

        usage = 'Usage: %prog [OPTIONS] [fortune_file]'
        arg_parser = OptionParser(usage=usage)
        arg_parser.add_option('-V', '--version', action='store_true',
                              dest='show_version', help='Show version and exit.')
        arg_parser.epilog = 'If fortune_file is omitted, fortune looks at the ' \
                            'FORTUNE_FILE environment variable for the path.'

        options, args = arg_parser.parse_args(sys.argv)
        if len(args) == 2:
            fortune_file = args[1]

        else:

        try:
            fortune_file = os.environ['FORTUNE_FILE']
        except KeyError:
            print('Missing fortune file.', file=sys.stderr)
            sys.exit(1)

        try:
            if options.show_version:
                print('fortune, version {}'.format(__version__))
            else:
        """
        fortune_file = self.get_plugin_data_folder() + "/fortunes/fortunes.dat"
        self._logger.info("fortune: {}".format(self.get_random_fortune(fortune_file)))
        # except ValueError as msg:
        #    print(msg, file=sys.stderr)
        #   sys.exit(1)

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            # put your plugin's default settings here
        )

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/fortune.js"],
            css=["css/fortune.css"],
            less=["less/fortune.less"]
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
                pip="https://github.com/berrystephenw/OctoPrint-Fortune/archive/{target_version}.zip"
            )
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Fortune Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = FortunePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }


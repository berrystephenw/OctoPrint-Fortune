# OctoPrint-Fortune

This is an adaptation of the original UNIX fortune program. Fortune will 
run on OctoPrint login and popup a quote or saying from a database of stored quotes.

I have not created these quotes or sayings, they are simply provided from the
source given by Brian M. Clapper as a sample set of fortunes.

http://software.clapper.org/fortune/

There is an icon that looks like a book on the navigation bar for those that 
would like a more frequent fortune. This can be turned off in the settings page.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/berrystephenw/OctoPrint-Fortune/archive/main.zip

This is a Python 3 or greater plugin!

## Configuration

The configuration available are:
* to enable or disable the icon on the navigation bar 
* optionally enable sending your fortune to OctoText. [OctoText](https://plugins.octoprint.org/plugins/OctoText/) must be enabled and configured for
this feature to work.
* option to use a fixed delay on the fortune popups. The default is based on
the number of characters in the fortune.
## Copyright
Copyright © 2008-2019 Brian M. Clapper. All rights reserved.

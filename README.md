# OctoPrint-Fortune

This is an adaptation of the original UNIX fortune program. Fortune will 
run on OctoPrint login and popup a quote or saying from a database of stored quotes.

I have not created these quotes or sayings, they are simply provided from the
source given by Brian M. Clapper as a sample set of fortunes, and Joel Kirchartz for the additional fortune files:

http://software.clapper.org/fortune/

https://github.com/JKirchartz/fortunes

There is an icon that looks like a book on the navigation bar for those that 
would like a more frequent fortune. This can be turned off in the settings page.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/berrystephenw/OctoPrint-Fortune/archive/main.zip

This is a Python 3 or greater plugin!

## Configuration

The configuration options available are:
* to enable or disable the icon on the navigation bar 
* optionally enable sending your fortune to OctoText. [OctoText](https://plugins.octoprint.org/plugins/OctoText/) must be enabled and configured for
this feature to work.

<img width="320" alt="Fortune" src="octoprint_fortune/assets/img/fortune-text.png">

* option to use a fixed delay on the fortune popups. The default delay is based on
the number of characters in the fortune.
* select the fortune file out of the following list:
  * authors
  * Chuck Norris facts (chuckfacts)
  * Ferengi Rules of Acquisition (it's a Star Trek thing)
  * fortunes (the original)
  * Jung
  * Paine (Thomas)
  * Scooter (not my idea)
  * showerthoughts

<img width="480" alt="Fortune" src="octoprint_fortune/assets/img/fortune-settings.png">
## Copyright
Copyright © 2008-2019 Brian M. Clapper. All rights reserved.

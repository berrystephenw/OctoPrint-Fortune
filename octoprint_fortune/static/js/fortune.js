/*
 * View model for OctoPrint-Fortune
 *
 * Author: Stephen Berry
 * License: AGPLv3
 */

$(document).ready(function(){
    $('[tool-tip-toggle="tooltip"]').tooltip({
        placement : 'bottom'
    });
});

$(function() {
    function FortuneViewModel(parameters) {
        var self = this;
        self.settings = parameters[0];

        self.yourFortune = function () {
            $.ajax({
                url: API_BASEURL + "plugin/fortune",
                type: "GET",
                dataType: "json",
                data: {
                    command: "test",
                    /* token: self.settings.settings.plugins.OctoText.access_token(), */
                    channel: 1
                },
                contentType: "application/json; charset=UTF-8",
                success: function (response) {
                    if (response.result) {
                        new PNotify({
                            title: gettext("Your Fortune!"),
                            text: gettext(response.data),
                            type: "success"
                        });
                    } else {
                        var text;

                        text = gettext("");

                        new PNotify({
                            title: gettext("Sorry, no fortune for you today!"),
                            text: text,
                            type: "error"
                        });
                    }
                },
                error: function () {
                }
            });
        };
        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: FortuneViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ "navigationViewModel" /* "loginStateViewModel", "settingsViewModel" */ ],
        // Elements to bind to, e.g. #settings_plugin_fortune, #tab_plugin_fortune, ...
        elements: [ "#navbar_plugin_fortune"  ]
    });
});
